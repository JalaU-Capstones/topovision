"""
This module defines the main window of the TopoVision application,
which orchestrates the GUI and the core application logic.
"""

import json
import logging
import os
import tkinter as tk
from tkinter import Tk, messagebox, ttk
from typing import Any, Callable, Dict, Optional, Tuple, Union, cast

import cv2
import numpy as np
from PIL import Image, ImageTk

from topovision.calculus.calculus_module import AnalysisContext
from topovision.capture.preprocessing import ImagePreprocessor
from topovision.core.interfaces import ICamera  # Keep this import
from topovision.core.models import (
    AnalysisResult,
    ArcLengthResult,
    FrameData,
    GradientResult,
    RegionOfInterest,
    VolumeResult,
)
from topovision.gui.analysis_panel import AnalysisPanel
from topovision.gui.camera_controller import CameraController
from topovision.gui.canvas_panel import CanvasPanel
from topovision.gui.plot3d_window import Plot3DWindow
from topovision.gui.theme import ThemeManager
from topovision.services.task_queue import TaskQueue
from topovision.visualization.visualizers import HeatmapVisualizer

from .i18n import get_translator

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define the path for user settings file
USER_SETTINGS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "user_settings.json"
)


class MainWindow(Tk):
    """The main window of the TopoVision application."""

    def __init__(
        self,
        camera: ICamera,
        calculus_module: AnalysisContext,
        task_queue: TaskQueue,
        preprocessor: ImagePreprocessor,
        lang: str = "en",
    ) -> None:
        """
        Initializes the MainWindow.

        Args:
            camera (ICamera): The camera instance for video capture.
            calculus_module (AnalysisContext): The module for performing calculations.
            task_queue (TaskQueue): The queue for background tasks.
            preprocessor (ImagePreprocessor): The preprocessor for denoising images.
            lang (str): The language for the UI.
        """
        super().__init__()

        self.translator = get_translator(lang)
        self._ = self.translator
        self._lang = lang

        self.title(self._("app_title"))
        self.geometry("1200x800")
        self.minsize(1000, 700)

        self.calculus_module = calculus_module
        self.visualizer = HeatmapVisualizer()
        self.task_queue = task_queue
        self.preprocessor = preprocessor

        # ---- State Management ----
        self.camera_controller = CameraController(camera, self._update_canvas_image)
        self.photo: Optional[ImageTk.PhotoImage] = None
        self._analysis_result_photo: Optional[ImageTk.PhotoImage] = None
        self.is_showing_analysis: bool = False
        self.selected_region: Optional[Tuple[int, int, int, int]] = None
        self._last_frame: Optional[np.ndarray] = None
        self._canvas_image_id: Optional[int] = None
        self.plot3d_window: Optional[Plot3DWindow] = None

        self.user_settings = self._load_user_settings()

        self._setup_styles()
        self._setup_ui()

        self.protocol("WM_DELETE_WINDOW", self._on_exit)
        self.after(100, self._process_results)
        self.after(15, self._update_frame)

    def _load_user_settings(self) -> Dict[str, Any]:
        """
        Loads user settings from a JSON file,
        or returns defaults if not found/invalid.
        """
        default_settings: Dict[str, Any] = {
            "tutorial_shown": {
                "gradient": False,
                "volume": False,
                "arc_length": False,
                "plot3d": False,
            }
        }
        try:
            if os.path.exists(USER_SETTINGS_FILE):
                with open(USER_SETTINGS_FILE, "r") as f:
                    settings: Dict[str, Any] = json.load(f)
                # Merge with defaults to ensure new tutorial flags are added
                for key, value in default_settings["tutorial_shown"].items():
                    if key not in settings.get("tutorial_shown", {}):
                        settings.setdefault("tutorial_shown", {})[key] = value
                return settings
        except (json.JSONDecodeError, IOError) as e:
            logging.warning(
                f"Could not load user settings from {USER_SETTINGS_FILE}: {e}. "
                "Using default settings."
            )
        return default_settings

    def _save_user_settings(self) -> None:
        """Saves current user settings to a JSON file."""
        try:
            with open(USER_SETTINGS_FILE, "w") as f:
                json.dump(self.user_settings, f, indent=4)
        except IOError as e:
            logging.error(f"Could not save user settings to {USER_SETTINGS_FILE}: {e}")

    def _show_tutorial(self, method: str) -> None:
        """Displays a tutorial message for a given analysis method."""
        tutorial_title_key = f"tutorial_{method}_title"
        tutorial_message_key = f"tutorial_{method}"

        title = self._(tutorial_title_key)
        message = self._(tutorial_message_key)

        messagebox.showinfo(title, message)

        # Mark tutorial as shown and save settings
        self.user_settings["tutorial_shown"][method] = True
        self._save_user_settings()

    def _setup_styles(self) -> None:
        """Configures the Ttk styles for the application."""
        style = ttk.Style(self)
        theme_manager = ThemeManager(style)
        theme_manager.apply("dark")

    def _setup_ui(self) -> None:
        """Initializes and places all UI components."""
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        main_container.grid_columnconfigure(0, weight=3)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        # --- Left Panel: Canvas ---
        self.canvas = CanvasPanel(main_container, bg="#0E0F11", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        # The type of on_selection_made is
        # Optional[Callable[[Optional[Tuple[int, int, int, int]], str, Any], None]]
        self.canvas.on_selection_made = self._handle_selection

        # --- Right Panel: Analysis ---
        self.analysis_panel = AnalysisPanel(
            main_container, self._trigger_analysis, self.translator
        )  # Pass main_container as master
        self.analysis_panel.grid(row=0, column=1, sticky="nsew")
        self.analysis_panel.toggle_btn.config(command=self.toggle_view)
        self.analysis_panel.clear_btn.config(command=self.clear_selection)

        # --- Bottom Buttons ---
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=50, pady=15)

        self.btn_toggle_camera = ttk.Button(
            buttons_frame, text=self._("open_camera_button"), command=self.toggle_camera
        )
        self.btn_toggle_camera.pack(side=tk.LEFT, padx=10, pady=5)

        # Button to open 3D Plot Window (now the only 3D entry point)
        self.btn_open_3d_plot = ttk.Button(
            buttons_frame,
            text=self._("open_3d_plot_button"),
            command=self._open_3d_plot_window,
        )
        self.btn_open_3d_plot.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_exit = ttk.Button(
            buttons_frame, text=self._("exit_button"), command=self._on_exit
        )
        self.btn_exit.pack(side=tk.RIGHT, padx=10, pady=5)

        self._update_initial_canvas_message()

    def _open_3d_plot_window(self) -> None:
        """Opens or brings to front the 3D plot window."""
        if self.plot3d_window is None or not self.plot3d_window.winfo_exists():
            self.plot3d_window = Plot3DWindow(self, lang=self._lang)
            self.plot3d_window.start_live_update()
            if not self.user_settings["tutorial_shown"].get("plot3d", False):
                logging.info("Showing 3D plot tutorial.")
                self._show_tutorial("plot3d")
            else:
                logging.info("3D plot tutorial already shown.")
        self.plot3d_window.lift()
        self.set_status(self._("3d_plot_window_opened"))

    def set_status(self, message: str, is_error: bool = False) -> None:
        """Updates the status label."""
        self.analysis_panel.set_status(message, is_error)
        if is_error:
            logging.error(message)
            messagebox.showerror(self._("app_title"), message)

    def _handle_selection(
        self,
        region: Optional[Tuple[int, int, int, int]],
        message_key: str,
        **kwargs: Any,
    ) -> None:
        """Callback for when a selection is made on the canvas."""
        translated_message = self._(message_key, **kwargs)
        self.selected_region = region
        self.analysis_panel.set_status(translated_message, is_error=not region)

    def _trigger_analysis(self, method: str) -> None:
        """Handles the logic for starting a calculation."""
        if self.selected_region is None:
            self.set_status(self._("region_error"), is_error=True)
            return

        if self._last_frame is None:
            self.set_status(self._("no_frame_to_analyze"), is_error=True)
            return

        if not self.user_settings["tutorial_shown"].get(method, False):
            self._show_tutorial(method)

        try:
            z_factor = self.analysis_panel.get_z_factor()
        except ValueError as e:
            self.set_status(str(e), is_error=True)
            return

        self.set_status(self._("calculating", method=method))
        self.task_queue.submit_task(self._perform_calculation, method, z_factor)

    def _perform_calculation(self, method: str, z_factor: float) -> Dict[str, Any]:
        """The actual calculation logic to be run in a background thread."""
        if self.selected_region is None or self._last_frame is None:
            raise RuntimeError("No selected region or frame to perform calculation.")

        x1, y1, x2, y2 = self.selected_region
        h, w, _ = self._last_frame.shape
        canvas_w, canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()

        rx1 = int(x1 * w / canvas_w)
        rx2 = int(x2 * w / canvas_w)
        ry1 = int(y1 * h / canvas_h)
        ry2 = int(y2 * h / canvas_h)

        region_data = self._last_frame[ry1:ry2, rx1:rx2]

        if method in ["gradient", "volume"]:
            gray_region = cv2.cvtColor(region_data, cv2.COLOR_RGB2GRAY)
            data_for_analysis: np.ndarray = gray_region
        elif method == "arc_length":
            points: list[Tuple[int, int]] = []
            if region_data.shape[0] > 0 and region_data.shape[1] > 0:
                gray_region_for_arc = cv2.cvtColor(region_data, cv2.COLOR_RGB2GRAY)
                middle_row_idx = gray_region_for_arc.shape[0] // 2
                for i in range(gray_region_for_arc.shape[1]):
                    points.append((i, gray_region_for_arc[middle_row_idx, i]))
            data_for_analysis = np.array(points)
        else:
            raise ValueError(f"Unknown analysis method: {method}")

        self.calculus_module.set_strategy(method)
        calc_kwargs: Dict[str, Any] = {}
        if method == "volume":
            calc_kwargs["z_factor"] = z_factor

        result = self.calculus_module.calculate(data_for_analysis, **calc_kwargs)

        return {
            "method": method,
            "result": result,
            "region": self.selected_region,
            "z_factor": z_factor,
        }

    def _process_results(self) -> None:
        """Checks for results from the task queue and updates the GUI."""
        result = self.task_queue.get_result()
        if result:
            if isinstance(result, Exception):
                self.set_status(
                    self._("calculation_error", error=result), is_error=True
                )
            else:
                self._handle_calculation_result(result)
        self.after(100, self._process_results)

    def _handle_calculation_result(self, result: Dict[str, Any]) -> None:
        """Handles a successful calculation result."""
        method: str = result.get("method", "")
        calc_result: Union[GradientResult, VolumeResult, ArcLengthResult, None] = (
            result.get("result")
        )
        region_coords: Optional[Tuple[int, int, int, int]] = result.get("region")

        if region_coords is None:
            self.set_status(
                self._("calculation_error", error="Missing region data in result."),
                is_error=True,
            )
            return

        region = RegionOfInterest(*region_coords)

        if method == "gradient" and isinstance(calc_result, GradientResult):
            self.set_status(
                self._(
                    "calculating_gradient",
                    dx=np.mean(calc_result.dz_dx),
                    dy=np.mean(calc_result.dz_dy),
                )
            )
            if self._last_frame is not None:
                original_image_pil = Image.fromarray(self._last_frame)
                analysis_result_model = AnalysisResult(
                    method=method, result_data=calc_result, region=region
                )
                heatmap = self.visualizer.visualize(
                    analysis_result_model, original_image=original_image_pil
                )
                self.display_result_image(heatmap)
        elif method == "volume" and isinstance(calc_result, VolumeResult):
            self.set_status(self._("calculating_volume", volume=calc_result.volume))
        elif method == "arc_length" and isinstance(calc_result, ArcLengthResult):
            self.set_status(self._("calculating_arc_length", length=calc_result.length))
        else:
            self.set_status(
                self._(
                    "calculation_error",
                    error=f"Unexpected result type for method {method}",
                ),
                is_error=True,
            )

    def clear_selection(self) -> None:
        """Clears the current selection."""
        self.canvas.clear_selection()
        self.selected_region = None
        self.set_status(self._("selection_cleared"))
        if self.plot3d_window and self.plot3d_window.winfo_exists():
            self.plot3d_window.clear_plot_data()

    def toggle_view(self) -> None:
        """Toggles between the live camera view and the analysis view."""
        if self._analysis_result_photo is None:
            self.set_status(self._("no_analysis_to_show"), is_error=True)
            return

        self.is_showing_analysis = not self.is_showing_analysis
        view_state = "analysis" if self.is_showing_analysis else "camera"
        self.set_status(self._(f"view_changed_to_{view_state}"))
        self._refresh_gui_display()

    def display_result_image(self, pil_image: Image.Image) -> None:
        """Displays a result image on the canvas."""
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 1 and h > 1:
            resized_img = pil_image.resize((w, h), Image.Resampling.LANCZOS)
            self._analysis_result_photo = ImageTk.PhotoImage(image=resized_img)
            self.is_showing_analysis = True
            self.set_status(self._("analysis_completed"))
            self._refresh_gui_display()

    def toggle_camera(self) -> None:
        """Toggles the camera state and updates the button text."""
        try:
            self.camera_controller.toggle()
            if self.camera_controller.is_running:
                self.btn_toggle_camera.config(text=self._("pause_camera_button"))
                self.set_status(self._("camera_started"))
                self.is_showing_analysis = False
            else:
                self.btn_toggle_camera.config(text=self._("resume_camera_button"))
                self.set_status(self._("camera_paused"))
        except Exception as e:
            self.set_status(self._("camera_error", error=e), is_error=True)

    def _update_frame(self) -> None:
        """Periodically updates the frame from the camera."""
        if self.camera_controller.is_running:
            frame: Optional[np.ndarray] = self.camera_controller.get_frame()
            if frame is not None:
                denoised_frame: np.ndarray = self.preprocessor.process(frame)
                self._last_frame = denoised_frame
                self._update_canvas_image(denoised_frame)

                if (
                    self.plot3d_window
                    and self.plot3d_window.winfo_exists()
                    and self.selected_region is not None
                ):
                    # Unpack the tuple returned by the helper
                    self.plot3d_window.set_latest_data(*self._prepare_3d_plot_data())

        self.after(15, self._update_frame)

    def _prepare_3d_plot_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Helper to prepare data for the 3D plot."""
        if self.selected_region is None or self._last_frame is None:
            # This should ideally not be called
            # if selected_region or _last_frame is None,
            # but as a safeguard, return empty arrays or raise an error.
            # For now, returning empty arrays.
            return np.array([]), np.array([]), np.array([])

        x1, y1, x2, y2 = self.selected_region
        h, w, _ = self._last_frame.shape
        canvas_w, canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()

        rx1 = int(x1 * w / canvas_w)
        rx2 = int(x2 * w / canvas_w)
        ry1 = int(y1 * h / canvas_h)
        ry2 = int(y2 * h / canvas_h)

        region_data = self._last_frame[ry1:ry2, rx1:rx2]
        if region_data.size == 0:
            return np.array([]), np.array([]), np.array([])

        gray_region: np.ndarray = cv2.cvtColor(region_data, cv2.COLOR_RGB2GRAY)

        try:
            z_factor: float = self.analysis_panel.get_z_factor()
        except ValueError:
            z_factor = 1.0

        rows, cols = gray_region.shape
        x = np.arange(0, cols, 1)
        y = np.arange(0, rows, 1)
        X, Y = np.meshgrid(x, y)
        Z = gray_region * z_factor
        return X, Y, Z

    def _update_3d_plot_live(self) -> None:
        """
        Extracts data from the selected region and sends it to the 3D plot window
        for live update.
        """
        if self.selected_region is None or self._last_frame is None:
            return

        x1, y1, x2, y2 = self.selected_region
        h, w, _ = self._last_frame.shape
        canvas_w, canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()

        rx1 = int(x1 * w / canvas_w)
        rx2 = int(x2 * w / canvas_w)
        ry1 = int(y1 * h / canvas_h)
        ry2 = int(y2 * h / canvas_h)

        region_data = self._last_frame[ry1:ry2, rx1:rx2]
        if region_data.size == 0:
            if self.plot3d_window:
                self.plot3d_window.clear_plot_data()
            return

        gray_region: np.ndarray = cv2.cvtColor(region_data, cv2.COLOR_RGB2GRAY)

        try:
            z_factor: float = self.analysis_panel.get_z_factor()
        except ValueError:
            z_factor = 1.0

        rows, cols = gray_region.shape
        x = np.arange(0, cols, 1)
        y = np.arange(0, rows, 1)
        X, Y = np.meshgrid(x, y)
        Z = gray_region * z_factor

        if self.plot3d_window:
            self.plot3d_window.set_latest_data(X, Y, Z)

    def _update_canvas_image(self, frame: np.ndarray) -> None:
        """Updates the canvas with a new camera frame."""
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 1 and h > 1:
            resized: np.ndarray = cv2.resize(
                frame, (w, h), interpolation=cv2.INTER_AREA
            )
            img: Image.Image = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
            self.photo = ImageTk.PhotoImage(image=img)
            self._refresh_gui_display()

    def _refresh_gui_display(self) -> None:
        """Updates the canvas content based on the current state."""
        current_photo: Optional[ImageTk.PhotoImage] = None
        if self.is_showing_analysis and self._analysis_result_photo:
            current_photo = self._analysis_result_photo
        elif self.camera_controller.started_once and self.photo:
            current_photo = self.photo
        else:
            self._update_initial_canvas_message()
            return

        if current_photo:
            if self._canvas_image_id is None:
                self._canvas_image_id = self.canvas.create_image(
                    0, 0, image=current_photo, anchor=tk.NW
                )
            else:
                self.canvas.itemconfig(self._canvas_image_id, image=current_photo)

    def _update_initial_canvas_message(self) -> None:
        """Displays the initial message on the canvas."""
        self.canvas.delete(tk.ALL)
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 100 and h > 100:
            self.canvas.create_text(
                w / 2,
                h / 2,
                text=self._("click_to_start"),
                fill="#E6E6E6",
                font=("Arial", 16),
                justify="center",
                width=w - 40,
            )

    def _on_exit(self) -> None:
        """Handles the safe closing of the window."""
        self.set_status(self._("closing_app"))
        self.camera_controller.stop()
        self.task_queue.stop()
        if self.plot3d_window and self.plot3d_window.winfo_exists():
            self.plot3d_window.stop_live_update()
            self.plot3d_window.destroy()
        self.destroy()

    def run(self) -> None:
        """Starts the main loop of the application."""
        self.mainloop()
