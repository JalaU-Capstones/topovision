"""
Camera Controller for TopoVision.

This module provides a controller to manage the camera's lifecycle,
including starting, pausing, and stopping the video feed.
"""

import logging
from typing import Callable, Optional, Protocol

import numpy as np


# Define ICamera as a Protocol for type checking
class ICamera(Protocol):
    def start(self) -> None: ...

    def pause(self) -> None: ...

    def stop(self) -> None: ...

    def resume(self) -> None: ...

    def get_frame(self) -> Optional[np.ndarray]: ...


try:
    # Attempt to import the concrete ICamera implementation
    # We import it under a different name to avoid redefinition issues with the Protocol
    from topovision.core.interfaces import ICamera as ConcreteICamera

    # At runtime, if ConcreteICamera is available, we can use it.
    # For type checking, the ICamera Protocol is what matters for CameraController.
except ImportError:
    logging.warning(
        "Could not import topovision.core.interfaces.ICamera. "
        "Ensure concrete camera implementations are available if not using mock."
    )


class CameraController:
    """
    Manages camera operations and state.

    This class acts as a high-level interface to the camera, abstracting
    the underlying state management for starting, pausing, and stopping.
    """

    def __init__(self, camera: ICamera, update_callback: Callable[[np.ndarray], None]):
        """
        Initializes the CameraController.

        Args:
            camera (ICamera): The camera instance to control.
            update_callback (Callable[[np.ndarray], None]): A callback to be invoked
                with the latest frame for UI updates.
        """
        # The type checker will ensure 'camera' conforms to ICamera Protocol.
        self.camera = camera
        self._update_callback = update_callback
        self._is_running = False
        self._started_once = False

    @property
    def is_running(self) -> bool:
        """Returns True if the camera is currently capturing frames."""
        return self._is_running

    @property
    def started_once(self) -> bool:
        """Returns True if the camera has been started at least once."""
        return self._started_once

    def start(self) -> None:
        """Starts or resumes the camera feed."""
        if self._is_running:
            return

        try:
            if not self._started_once:
                self.camera.start()
                self._started_once = True
                logging.info("Camera started for the first time.")
            else:
                self.camera.resume()
                logging.info("Camera resumed.")
            self._is_running = True
        except Exception as e:
            logging.error(f"Failed to start or resume camera: {e}")
            self._is_running = False
            raise

    def pause(self) -> None:
        """Pauses the camera feed."""
        if not self._is_running:
            return

        try:
            self.camera.pause()
            self._is_running = False
            logging.info("Camera paused.")
        except Exception as e:
            logging.error(f"Failed to pause camera: {e}")
            raise

    def stop(self) -> None:
        """Stops the camera feed and releases resources."""
        if not self._started_once:
            return

        try:
            self.camera.stop()
            self._is_running = False
            self._started_once = False
            logging.info("Camera stopped.")
        except Exception as e:
            logging.error(f"Failed to stop camera: {e}")
            # Still update state, as the camera might be unusable
            self._is_running = False
            self._started_once = False
            raise

    def toggle(self) -> None:
        """Toggles the camera state between running and paused."""
        if self._is_running:
            self.pause()
        else:
            self.start()

    def get_frame(self) -> Optional[np.ndarray]:
        """
        Retrieves the latest frame from the camera.

        Returns:
            Optional[np.ndarray]: The frame as a NumPy array, or None if no
            frame is available or the camera is not running.
        """
        if not self._is_running:
            return None
        return self.camera.get_frame()
