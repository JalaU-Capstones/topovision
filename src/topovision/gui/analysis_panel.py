"""
This module defines the AnalysisPanel class, which is a UI component
for displaying analysis controls in the TopoVision application.
"""

import tkinter as tk
from tkinter import ttk
from typing import Any, Callable

from topovision.gui.i18n import Translator


class AnalysisPanel(ttk.Frame):
    """
    A panel for analysis controls, parameters, and status feedback.

    This panel provides the user with:
    - Buttons to trigger different types of analysis (e.g., gradient, volume).
    - Input fields for analysis parameters like the Z-factor.
    - Controls for managing the view and selections.
    - A status bar for feedback and error messages.
    """

    def __init__(
        self,
        parent: tk.Widget,
        analysis_callback: Callable[[str], None],
        translator: Translator,
        **kwargs: Any,
    ):
        """
        Initializes the AnalysisPanel.

        Args:
            parent (tk.Widget): The parent widget.
            analysis_callback (Callable[[str], None]): Callback to trigger an analysis.
            translator (Translator): Function for string translation.
            **kwargs: Additional keyword arguments for the ttk.Frame.
        """
        super().__init__(parent, **kwargs)

        self.analysis_callback = analysis_callback
        self._ = translator
        self._setup_widgets()

    def _setup_widgets(self) -> None:
        """Creates and arranges the widgets in the panel."""
        self.columnconfigure(0, weight=1)

        # --- Section: Calculation Parameters ---
        self._create_section_header(self._("calculation_parameters_title"))
        self._create_z_factor_input()

        # --- Section: Analysis Actions ---
        self._create_section_header(self._("analysis_actions_title"))
        self._create_analysis_buttons()

        # --- Section: Visualization ---
        self._create_section_header(self._("visualization_title"))
        self._create_visualization_buttons()

        # --- Section: Status Feedback ---
        self._create_status_label()

    def _create_section_header(self, text: str) -> None:
        """Creates a styled header for a panel section."""
        ttk.Label(self, text=text, style="Heading.TLabel").pack(
            pady=(15, 5), anchor=tk.W, padx=5
        )
        ttk.Separator(self).pack(fill=tk.X, padx=5)

    def _create_z_factor_input(self) -> None:
        """Creates the Z-factor input field and its description."""
        param_frame = ttk.Frame(self)
        param_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(param_frame, text=self._("z_factor_label")).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        self.z_factor_entry = ttk.Entry(param_frame, width=8)
        self.z_factor_entry.insert(0, "1.0")
        self.z_factor_entry.pack(side=tk.LEFT)

        info_label = ttk.Label(
            self,
            text=self._("z_factor_info"),
            font=("Segoe UI", 8),
            foreground="#8B949E",
        )
        info_label.pack(anchor=tk.W, padx=10, pady=(0, 10))

    def _create_analysis_buttons(self) -> None:
        """Creates buttons for triggering different analyses."""
        btn_config = [
            ("gradient_button", "gradient"),
            ("volume_button", "volume"),
            ("arc_length_button", "arc_length"),
        ]

        def _command_factory(method_name: str) -> Callable[[], None]:
            return lambda: self.analysis_callback(method_name)

        for text_key, method in btn_config:
            btn = ttk.Button(
                self,
                text=self._(text_key),
                command=_command_factory(method),
                style="TButton",
            )
            btn.pack(fill=tk.X, padx=10, pady=5)

    def _create_visualization_buttons(self) -> None:
        """Creates buttons for view and selection control."""
        self.toggle_btn = ttk.Button(
            self, text=self._("toggle_view_button"), style="TButton"
        )
        self.toggle_btn.pack(fill=tk.X, padx=10, pady=5)

        self.clear_btn = ttk.Button(
            self, text=self._("clear_selection_button"), style="TButton"
        )
        self.clear_btn.pack(fill=tk.X, padx=10, pady=5)

    def _create_status_label(self) -> None:
        """Creates the label for status messages."""
        self.status_label_var = tk.StringVar(value=self._("status_ready"))
        self.status_label = ttk.Label(
            self,
            textvariable=self.status_label_var,
            wraplength=220,
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.status_label.pack(
            fill=tk.X, padx=10, pady=(15, 5), expand=True, side=tk.BOTTOM
        )

    def get_z_factor(self) -> float:
        """
        Returns the Z-factor from the entry field, handling validation.

        Raises:
            ValueError: If the Z-factor is not a positive number.
        """
        try:
            z_factor = float(self.z_factor_entry.get())
            if z_factor <= 0:
                raise ValueError("Z-factor must be positive.")
            return z_factor
        except ValueError:
            raise ValueError(self._("z_factor_error"))

    def set_status(self, message: str, is_error: bool = False) -> None:
        """
        Sets the status message, with appropriate styling for errors.
        """
        color = "#FF6B6B" if is_error else "#E6E6E6"
        self.status_label.config(foreground=color)
        self.status_label_var.set(message)
