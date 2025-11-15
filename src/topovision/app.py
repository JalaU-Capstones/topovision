"""TopoVision main application entry point (Facade pattern)."""

import tkinter as tk

from topovision.gui.gui_module import MainWindow


def main() -> None:
    """Entry point for the TopoVision system."""
    print("🚀 TopoVision initialized (development mode).")

    # Create and run the main GUI window
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
