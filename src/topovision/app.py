"""TopoVision main application entry point (Facade pattern)."""

from topovision.gui.gui_module import start_gui


def main() -> None:
    """Entry point for the TopoVision system."""
    print("🚀 TopoVision initialized (development mode).")
    start_gui()


if __name__ == "__main__":
    main()
