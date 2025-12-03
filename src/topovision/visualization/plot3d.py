from typing import Optional  # Ensure Optional is imported

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection  # Correct import for LineCollection
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import (  # Correct import for Poly3DCollection
    Poly3DCollection,
)
from numpy.typing import NDArray


def create_initial_surface_plot(
    x_data: NDArray[np.float64],
    y_data: NDArray[np.float64],
    z_data: NDArray[np.float64],
    title: str = "3D Surface Plot",
    xlabel: str = "X",
    ylabel: str = "Y",
    zlabel: str = "Z",
    cmap: str = "viridis",
    shade: bool = True,
    wireframe: bool = False,
    rstride: int = 1,
    cstride: int = 1,
) -> tuple[
    plt.Figure,
    plt.Axes,
    Poly3DCollection,  # Updated type hint
    Optional[LineCollection],  # Updated type hint, can be None
]:
    """
    Creates the initial 3D surface plot and returns the figure, axes, and the
    surface object. This function is designed to be called once for initialization.

    Args:
        x_data (np.ndarray): 2D array of x-coordinates.
        y_data (np.ndarray): 2D array of y-coordinates.
        z_data (np.ndarray): 2D array of z-coordinates (function values).
        title (str): Title of the plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        zlabel (str): Label for the z-axis.
        cmap (str): Colormap to use for the surface.
        shade (bool): Whether to apply shading to the surface.
        wireframe (bool): Whether to draw a wireframe on the surface.
        rstride (int): Row stride (step size) for the surface mesh.
        cstride (int): Column stride (step size) for the surface mesh.

    Returns:
        tuple: (matplotlib.figure.Figure, matplotlib.axes.Axes,
                Poly3DCollection,
                Optional[LineCollection])
               The Figure object, Axes object, the initial surface plot object,
               and the wireframe object (or None).
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Plot the surface with specified strides
    surface = ax.plot_surface(
        x_data,
        y_data,
        z_data,
        cmap=cmap,
        shade=shade,
        rstride=rstride,
        cstride=cstride,
        alpha=0.9,
        antialiased=False,
    )  # Antialiased can be slow

    wireframe_obj: Optional[LineCollection] = None
    # Optionally add a wireframe
    if wireframe:
        wireframe_obj = ax.plot_wireframe(
            x_data,
            y_data,
            z_data,
            color="black",
            linewidth=0.5,
            rstride=rstride * 2,
            cstride=cstride * 2,
            alpha=0.3,
        )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

    # Adjust view for better perception
    ax.view_init(elev=30, azim=45)  # Default viewing angle

    # Set colorbar
    fig.colorbar(surface, shrink=0.5, aspect=5)

    return fig, ax, surface, wireframe_obj


def update_surface_plot_data(
    ax: Axes3D,
    x_data: NDArray[np.float64],
    y_data: NDArray[np.float64],
    z_data: NDArray[np.float64],
    current_surface_obj: Poly3DCollection,  # Updated type hint
    current_wireframe_obj: Optional[LineCollection],  # Updated type hint
    cmap: str = "viridis",
    shade: bool = True,
    wireframe: bool = False,
    rstride: int = 1,
    cstride: int = 1,
) -> tuple[Poly3DCollection, Optional[LineCollection]]:  # Updated type hint
    """
    Updates the 3D surface plot by removing the old surface/wireframe and
    creating new ones. This is a targeted redraw approach to handle changing Z-data.

    Args:
        ax (matplotlib.axes.Axes): The 3D axes object.
        x_data (np.ndarray): 2D array of x-coordinates (full resolution).
        y_data (np.ndarray): 2D array of y-coordinates (full resolution).
        z_data (np.ndarray): New 2D array of z-coordinates (function values,
                              full resolution).
        current_surface_obj (Poly3DCollection): The existing
                                    surface plot object to remove.
        current_wireframe_obj (Optional[LineCollection]): The existing
                                    wireframe object to remove.
        cmap (str): Colormap to use for the surface.
        shade (bool): Whether to apply shading to the surface.
        wireframe (bool): Whether to draw a wireframe on the surface.
        rstride (int): Row stride (step size) for the surface mesh.
        cstride (int): Column stride (step size) for the surface mesh.

    Returns:
        tuple: (Poly3DCollection,
                Optional[LineCollection])
               The new surface plot object and the new wireframe object (or None).
    """
    # Remove old surface and wireframe objects
    if current_surface_obj:
        current_surface_obj.remove()
    if current_wireframe_obj:
        current_wireframe_obj.remove()

    # Create new surface with updated Z-data
    new_surface = ax.plot_surface(
        x_data,
        y_data,
        z_data,
        cmap=cmap,
        shade=shade,
        rstride=rstride,
        cstride=cstride,
        alpha=0.9,
        antialiased=False,
    )

    new_wireframe: Optional[LineCollection] = None
    if wireframe:
        new_wireframe = ax.plot_wireframe(
            x_data,
            y_data,
            z_data,
            color="black",
            linewidth=0.5,
            rstride=rstride * 2,
            cstride=cstride * 2,
            alpha=0.3,
        )

    return new_surface, new_wireframe


if __name__ == "__main__":
    # Example for 3D Surface Plot
    def f(x: NDArray[np.float64], y: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.sin(np.sqrt(x**2 + y**2))

    x = np.linspace(-5, 5, 100)  # Full resolution data
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    # Initial plot with stride
    fig, ax, surface, wireframe_obj = create_initial_surface_plot(
        X, Y, Z, title="Live 3D Surface Plot", rstride=5, cstride=5, wireframe=True
    )
    plt.show(block=False)  # Don't block for live update example

    # Simulate live update
    for i in range(100):
        new_Z = (
            f(X, Y + i * 0.1) + np.sin(i * 0.5) * 0.5
        )  # Change Z data over time (full resolution)

        # Update the plot using the new function
        surface, wireframe_obj = update_surface_plot_data(
            ax,
            X,
            Y,
            new_Z,
            surface,
            wireframe_obj,
            cmap="plasma",
            shade=True,
            wireframe=True,
            rstride=5,
            cstride=5,
        )

        fig.canvas.draw_idle()  # Redraw the canvas
        fig.canvas.flush_events()  # Process events
        plt.pause(0.01)  # Small pause to see the animation
