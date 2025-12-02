"""
Heatmap rendering utilities for TopoVision.
Dark, minimal and compatible with project requirements.
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io


def generate_heatmap(data: np.ndarray, cmap: str = "plasma", label: str = "Valor Topográfico (Unidades)") -> Image.Image:
    """
    Generates a heatmap as a PIL.Image from a 2D numpy array.

    Args:
        data (np.ndarray): 2D matrix of numerical values.
        cmap (str): Name of the colormap to use (default: 'plasma', good for dark themes).
        label (str): Label for the color bar (e.g., "Altitud (m)").

    Returns:
        PIL.Image: RGB image containing the heatmap.
    """
    if data is None or not isinstance(data, np.ndarray):
        raise ValueError("Heatmap requires a valid numpy 2D array.")

    if data.ndim != 2:
        raise ValueError("Heatmap only accepts 2D matrices.")

    # ---- Figure configuration (dark minimal) ----
    fig = plt.figure(figsize=(4, 3), dpi=120)
    ax = fig.add_subplot(111)

    # Configuración de fondo oscuro
    BG_COLOR = "#111214"
    TEXT_COLOR = "white"
    ax.set_facecolor(BG_COLOR)
    fig.patch.set_facecolor(BG_COLOR)

    # 1. Draw heatmap
    img_plot = ax.imshow(data, cmap=cmap, aspect="auto")
    ax.set_axis_off()

    # 2. Add Color Bar (Legend) for visual scaling refinement
    cbar = fig.colorbar(img_plot, ax=ax, orientation="vertical", shrink=0.8, pad=0.03)
    
    # 3. Apply dark theme to color bar elements
    cbar.ax.yaxis.set_tick_params(color=TEXT_COLOR)
    cbar.outline.set_edgecolor('none') 
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=TEXT_COLOR, fontsize=8) 
    
    # 4. Set descriptive label
    cbar.set_label(label, color=TEXT_COLOR, fontsize=9)
    
    plt.tight_layout(pad=0.5)

    # Convert to image
    buffer = io.BytesIO()
    fig.canvas.print_png(buffer)
    plt.close(fig)

    buffer.seek(0)
    img = Image.open(buffer).convert("RGB")
    return img