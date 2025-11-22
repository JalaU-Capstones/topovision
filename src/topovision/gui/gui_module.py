import tkinter as tk
from tkinter import Canvas, Tk, ttk
from typing import Optional, Tuple

import cv2
from PIL import Image, ImageTk

from topovision.core.interfaces import Camera


class MainWindow(Tk):
    """Main application window for TopoVision with interactive region selection."""

    def __init__(self, camera: Camera) -> None:
        """
        Initializes the main window.

        Args:
            camera (Camera): The camera instance to be used for video capture.
        """
        super().__init__()
        self.title("TopoVision - Camera Module")
        self.geometry("800x800")

        self.camera: Camera = camera
        self.is_camera_running: bool = False
        self.photo: Optional[ImageTk.PhotoImage] = None

        # --- UI Elements ---
        self.buttons_frame: ttk.Frame = ttk.Frame(self)
        self.buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=50, pady=10)

        self.btn_toggle_camera: ttk.Button = ttk.Button(
            self.buttons_frame, text="Open Camera", command=self.toggle_camera
        )
        self.btn_toggle_camera.pack(side=tk.LEFT, padx=5)

        self.btn_exit: ttk.Button = ttk.Button(
            self.buttons_frame, text="Exit", command=self.on_exit
        )
        self.btn_exit.pack(side=tk.RIGHT, padx=5)

        self.canvas: Canvas = tk.Canvas(self, width=700, height=750, bg="gray")
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # --- Selection variables ---
        self.selection_start: Optional[Tuple[int, int]] = None
        self.selection_rect_id: Optional[int] = None
        self.selected_region: Optional[Tuple[int, int, int, int]] = None  # x1, y1, x2, y2

        # --- Bind mouse events ---
        self.canvas.bind("<ButtonPress-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

    # --- Camera controls ---
    def toggle_camera(self) -> None:
        """Toggles the camera state between running and paused."""
        if not self.is_camera_running:
            self.start_capture()
        else:
            self.pause_capture()

    def start_capture(self) -> None:
        """Starts the camera capture and begins updating the canvas."""
        if not self.is_camera_running:
            try:
                self.camera.start()
                self.is_camera_running = True
                self.btn_toggle_camera.config(text="Pause Camera")
                self._update_frame()
                print("Camera capture started.")
            except IOError as e:
                print(f"Error starting camera: {e}")

    def pause_capture(self) -> None:
        """Pauses the camera capture."""
        if self.is_camera_running:
            self.camera.pause()
            self.is_camera_running = False
            self.btn_toggle_camera.config(text="Resume Camera")
            print("Camera capture paused.")

    def stop_capture(self) -> None:
        """Stops the camera capture permanently and releases resources."""
        if self.is_camera_running:
            self.pause_capture()
        self.camera.stop()
        print("Camera capture stopped and resources released.")

    def _update_frame(self) -> None:
        """Fetches a frame, resizes it to fit the canvas, and displays it."""
        if not self.is_camera_running:
            return

        frame = self.camera.get_frame()
        if frame is not None:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if canvas_width > 1 and canvas_height > 1:
                resized_frame = cv2.resize(
                    frame, (canvas_width, canvas_height), interpolation=cv2.INTER_AREA
                )
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(resized_frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

                # Redraw selection rectangle if it exists
                if self.selected_region:
                    x1, y1, x2, y2 = self.selected_region
                    self.selection_rect_id = self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline="yellow", width=2, dash=(4, 2), fill="", tags="selection"
                    )

        self.after(15, self._update_frame)

    # --- Mouse event handlers ---
    def _on_click(self, event):
        """Start region selection."""
        self.selection_start = (event.x, event.y)
        # Remove previous rectangle
        if self.selection_rect_id:
            self.canvas.delete(self.selection_rect_id)
            self.selection_rect_id = None
        print(f"Selection started at ({event.x}, {event.y})")

    def _on_drag(self, event):
        """Update the selection rectangle while dragging."""
        if self.selection_start:
            x1, y1 = self.selection_start
            x2, y2 = event.x, event.y
            # Remove previous rectangle
            if self.selection_rect_id:
                self.canvas.delete(self.selection_rect_id)
            # Draw new rectangle
            self.selection_rect_id = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="yellow", width=2, dash=(4, 2), fill="", tags="selection"
            )

    def _on_release(self, event):
        """Finalize selection and store region coordinates."""
        if self.selection_start:
            x1, y1 = self.selection_start
            x2, y2 = event.x, event.y
            # Normalize coordinates
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])
            self.selected_region = (x1, y1, x2, y2)
            self.selection_start = None
            print(f"Selection finalized: {self.selected_region}")
            # TODO: send coordinates to calculation module
            # e.g., self.camera.calculate_region(x1, y1, x2, y2)

    # --- Exit & run ---
    def on_exit(self) -> None:
        """Handles window closing and ensures safe camera teardown."""
        print("Exiting application...")
        self.stop_capture()
        self.destroy()

    def run(self) -> None:
        """Starts the Tkinter main loop."""
        self.mainloop()
