from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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
    Poly3DCollection,
    Optional[LineCollection],
]:
    """
    Creates the initial 3D surface plot and returns the figure, axes, and the
    surface object.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

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
    )

    wireframe_obj: Optional[LineCollection] = None
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

    # Set aspect ratio
    x_range = np.ptp(x_data)
    y_range = np.ptp(y_data)
    z_range = np.ptp(z_data)
    if x_range > 0 and y_range > 0 and z_range > 0:
        ax.set_box_aspect((x_range, y_range, z_range))

    ax.view_init(elev=30, azim=45)
    fig.colorbar(surface, shrink=0.5, aspect=5)

    return fig, ax, surface, wireframe_obj


def update_surface_plot_data(
    ax: Axes3D,
    x_data: NDArray[np.float64],
    y_data: NDArray[np.float64],
    z_data: NDArray[np.float64],
    current_surface_obj: Poly3DCollection,
    current_wireframe_obj: Optional[LineCollection],
    cmap: str = "viridis",
    shade: bool = True,
    wireframe: bool = False,
    rstride: int = 1,
    cstride: int = 1,
) -> tuple[Poly3DCollection, Optional[LineCollection]]:
    """
    Updates the 3D surface plot by removing the old surface/wireframe and
    creating new ones.
    """
    if current_surface_obj:
        current_surface_obj.remove()
    if current_wireframe_obj:
        current_wireframe_obj.remove()

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

    def f(x: NDArray[np.float64], y: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.sin(np.sqrt(x**2 + y**2))

    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    fig, ax, surface, wireframe_obj = create_initial_surface_plot(
        X, Y, Z, title="Live 3D Surface Plot", rstride=5, cstride=5, wireframe=True
    )
    plt.show(block=False)

    for i in range(100):
        new_Z = f(X, Y + i * 0.1) + np.sin(i * 0.5) * 0.5
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
        fig.canvas.draw_idle()
        fig.canvas.flush_events()
        plt.pause(0.01)
