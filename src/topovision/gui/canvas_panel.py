"""
Canvas Panel for TopoVision.

This module defines a custom Tkinter Canvas that allows users to select
a rectangular region on top of the video feed or analysis results.
"""

import tkinter as tk
from typing import Any, Callable, Optional, Tuple


class CanvasPanel(tk.Canvas):
    """
    A custom canvas for displaying video and handling user selections.

    This canvas is responsible for:
    - Drawing the video frames or analysis results.
    - Allowing the user to draw a selection rectangle.
    - Notifying a callback function when a selection is made.
    """

    MIN_SELECTION_SIZE = 10  # Minimum size for a valid selection

    def __init__(self, parent: tk.Widget, **kwargs: Any):
        """
        Initializes the CanvasPanel.

        Args:
            parent (tk.Widget): The parent widget.
            **kwargs: Additional keyword arguments for the tk.Canvas.
        """
        super().__init__(parent, **kwargs)

        self._selection_start: Optional[Tuple[int, int]] = None
        self._selection_rect_id: Optional[int] = None
        self.selected_region: Optional[Tuple[int, int, int, int]] = None

        # The callback to be invoked when a selection is made or cleared.
        # It receives the region, a message key, and optional format arguments.
        self.on_selection_made: Optional[Callable[..., None]] = (
            None  # Changed type hint
        )

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event: tk.Event) -> None:
        """Handles the initial click to start a selection."""
        self._selection_start = (event.x, event.y)
        self.delete("selection")  # Clear any previous selection rectangle

    def _on_drag(self, event: tk.Event) -> None:
        """Handles dragging to draw or update the selection rectangle."""
        if not self._selection_start:
            return

        x1, y1 = self._selection_start
        x2, y2 = event.x, event.y

        # Redraw the rectangle for immediate visual feedback
        self.delete("selection")
        self._selection_rect_id = self.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            outline="#FFD34D",
            width=2,
            dash=(3, 2),
            tags="selection",
        )

    def _on_release(self, event: tk.Event) -> None:
        """Finalizes the selection when the mouse button is released."""
        if not self._selection_start:
            return

        x1, y1 = self._selection_start
        x2, y2 = event.x, event.y
        self._selection_start = None

        # Ensure the coordinates are ordered (top-left, bottom-right)
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Validate selection size
        if (x2 - x1) < self.MIN_SELECTION_SIZE or (y2 - y1) < self.MIN_SELECTION_SIZE:
            self.delete("selection")
            if self.on_selection_made:
                self.on_selection_made(
                    None, "selection_too_small", min_size=self.MIN_SELECTION_SIZE
                )
            return

        self.selected_region = (x1, y1, x2, y2)

        if self.on_selection_made:
            width, height = x2 - x1, y2 - y1
            self.on_selection_made(
                self.selected_region, "selection_made", width=width, height=height
            )

    def clear_selection(self) -> None:
        """Clears the current selection rectangle and region data."""
        self.selected_region = None
        self.delete("selection")
        if self.on_selection_made:
            self.on_selection_made(None, "selection_cleared")
