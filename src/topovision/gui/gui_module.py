import tkinter as tk
from tkinter import Canvas, Tk, ttk
from typing import Optional

import cv2
from PIL import Image, ImageTk

from topovision.core.interfaces import Camera


class MainWindow(Tk):
    """Main application window for TopoVision."""

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
            self.pause_capture()  # First, pause the stream
        self.camera.stop()
        print("Camera capture stopped and resources released.")

    def _update_frame(self) -> None:
        """
        Fetches a frame, resizes it to fit the canvas, and displays it.
        """
        if not self.is_camera_running:
            return

        frame = self.camera.get_frame()
        if frame is not None:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Ensure canvas is ready and has a valid size before resizing
            if canvas_width > 1 and canvas_height > 1:
                # Resize frame to fit canvas using an efficient interpolation
                resized_frame = cv2.resize(
                    frame, (canvas_width, canvas_height), interpolation=cv2.INTER_AREA
                )
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(resized_frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.after(15, self._update_frame)  # Schedule the next update

    def on_exit(self) -> None:
        """Handles window closing and ensures safe camera teardown."""
        print("Exiting application...")
        self.stop_capture()
        self.destroy()

    def run(self) -> None:
        """Starts the Tkinter main loop."""
        self.mainloop()
