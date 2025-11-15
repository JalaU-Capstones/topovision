import tkinter as tk
from tkinter import Tk, ttk

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("topovision - camera module")
        self.geometry("800x800")

        self.cap = None
        self.is_camera_running = False

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=50, pady=10)

        self.btn_open_camera = ttk.Button(
            self.buttons_frame, text="Open Camera", command=self.toggle_camera
        )
        self.btn_open_camera.pack(side=tk.LEFT, padx=5)

        self.btn_exit = ttk.Button(
            self.buttons_frame, text="Exit", command=self.on_exit
        )
        self.btn_exit.pack(side=tk.RIGHT, padx=5)

        self.canvas = tk.Canvas(
            self, width=700, height=750, bg="gray", highlightthickness=1
        )
        self.canvas.pack(padx=10, pady=10)

        self.canvas.create_text(
            350, 350, text="Video Canvas", fill="white"
        )

    def toggle_camera(self):
        print("'toggle_camera' no implemented yet")

    def start_camera(self):
        print("'start_camera' no implemented yet")

    def stop_camera(self):
        print("'stop_camera' no implemented yet")

    def on_exit(self):
        self.destroy()

    def run(self):
        self.mainloop()
