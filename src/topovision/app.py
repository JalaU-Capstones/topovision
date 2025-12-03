"""TopoVision main application entry point (Facade pattern)."""

from topovision.capture.capture_module import OpenCVCamera
from topovision.gui.gui_module import MainWindow
from topovision.capture.camera_backends import OpenCVCamera, MockCamera


def main() -> None:
    """Entry point for the TopoVision system."""
    print("🚀 TopoVision initialized (development mode).")

    # --- Dependency Injection ---
    # Create a camera instance (could be OpenCVCamera or MockCamera)
    camera = OpenCVCamera(camera_id=0)

    # Inject the camera into the GUI
    app = MainWindow(camera)

    # Run the main application loop
    app.run()


if __name__ == "__main__":
    main()
