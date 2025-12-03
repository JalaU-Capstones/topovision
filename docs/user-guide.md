# 👨‍💻 TopoVision — User Guide

> **Purpose:**
> This guide explains how to install, run, and use the **TopoVision 3D Topographic Analysis System**.
> It is written for academic users and reviewers who wish to test the system for Calculus II applications.

---

## 🧩 1. Overview

**TopoVision** is an educational software designed to connect **multivariable calculus** with **visual topographic analysis**.

It uses a standard webcam (or video input) to:
- Capture surface or terrain data in real time,
- Compute **gradients**, **partial derivatives**, and **surface integrals**,
- Visualize the data through **color maps** and **vector fields**.

---

## 💻 2. System Requirements

| Component | Minimum | Recommended |
|------------|----------|-------------|
| **Python** | 3.11 | 3.11+ |
| **RAM** | 4 GB | 8 GB |
| **CPU** | Dual-core | Quad-core |
| **Camera** | 720p (USB/Webcam) | 1080p (or higher) |
| **OS** | Windows 10 / Ubuntu 22.04 / macOS 13 | Latest version of any supported OS |

---

## ⚙️ 3. Installation Guide

### 🪜 Step 1 — Clone the Repository

```bash
git clone https://github.com/JalaU-Capstones/topovision.git
cd topovision
````

### 🧱 Step 2 — Create a Virtual Environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate       # On Linux/macOS
# OR
.venv\Scripts\activate          # On Windows
```

### 📦 Step 3 — Install Dependencies

For full installation:

```bash
pip install -r requirements.txt
```

For lightweight environments:

```bash
pip install -r requirements-light.txt
```

### 🧪 Step 4 — (Optional) Install Development Tools

If you plan to contribute:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

---

## ▶️ 4. Running TopoVision

There are a few ways to run TopoVision, depending on how you installed it and your operating system.

### Option 1: Using the provided scripts (Recommended for repository clones)

If you cloned the repository and followed the installation steps, you can use the convenience scripts:

**On Linux/macOS:**
```bash
./run.sh
```

**On Windows:**
```bash
.\run.bat
```

These scripts will activate your virtual environment and launch the application.

### Option 2: Directly from the command line (After `pip install`)

If you installed TopoVision via `pip install topovision` (either from PyPI or in editable mode), you can run it directly:

```bash
topovision
```

This command leverages the entry point defined in the project's `pyproject.toml`.

### Option 3: Running the main module (Advanced)

For development or debugging, you can also run the main module directly from the `src` directory, ensuring your virtual environment is active:

```bash
python -m topovision
```

If everything is configured correctly, a **Tkinter window** will appear with the following interface:

```
+-----------------------------------+
|          🛰️  TOPOVISION           |
|-----------------------------------|
| [ Open Camera ]   [ Exit ]        |
|                                   |
|  (Live camera feed area)          |
|                                   |
+-----------------------------------+
```

---

## 🧠 5. How It Works (Simplified)

### Step-by-step process:

1. **Camera Capture**
   TopoVision connects to your webcam using **OpenCV** and starts reading frames.

2. **Preprocessing**
   Each frame is converted to grayscale and normalized to enhance contrast.

3. **Mathematical Analysis**

   * Partial derivatives are computed using **finite differences**.
   * Gradient vectors are calculated and visualized.
   * Integrals are approximated via **Riemann sums**.

4. **Visualization**
   The processed data is dynamically displayed through various visualizations:

   *   **2D Heatmaps:** A color-coded representation of height or intensity levels on a flat image plane.
   *   **Gradient Vector Fields:** Overlays showing the direction and magnitude of the steepest ascent (gradient) using vector arrows.
   *   **3D Surface Plots:** An interactive three-dimensional rendering of the terrain's surface, providing a comprehensive view of its topography.

5. **Interaction**
   Users can select regions or points directly on the GUI to analyze specific areas.

---

## 🖱️ 6. User Interface Controls

TopoVision's graphical user interface (GUI) provides intuitive controls for interacting with the system.

| Button                       | Description                                                                                             |
| :--------------------------- | :------------------------------------------------------------------------------------------------------ |
| **Open Camera**              | Initiates the camera feed, starts real-time image processing, and begins the topographic analysis.      |
| **Pause** *(future)*         | Temporarily freezes the analysis and camera feed, allowing for detailed inspection of a static frame.   |
| **Exit**                     | Safely terminates all running processes, closes the camera, and exits the application.                  |
| **Select Region** *(future)* | Enables users to define a custom Region of Interest (ROI) on the camera feed for focused analysis.      |

💡 *Note:* During the early prototype (Phase 1–2), only the “Open Camera” and “Exit” buttons are fully functional. Additional features will be enabled in subsequent development phases.

### Interactive 3D Plot Controls

When a 3D surface plot is displayed (e.g., in a separate window or embedded within the GUI), you can interact with it using standard `matplotlib` controls:

*   **Rotate:** Click and drag the plot with your mouse to change the viewing angle and perspective.
*   **Zoom:** Use the scroll wheel on your mouse to zoom in and out of the plot.
*   **Pan:** Hold down the `Shift` key (or sometimes `Ctrl` or `Alt`, depending on your OS and `matplotlib` backend) and click-and-drag to move the plot horizontally and vertically within the display area.

These interactive controls allow for a comprehensive exploration of the 3D topographic data, enabling users to examine specific features and understand the surface's geometry from various viewpoints.

---

## 🧮 7. Example Use Case

**Scenario:**
You place a small object (like a ramp or a curved surface) in front of your camera.

**Result:**
TopoVision:

* Captures the light intensity map,
* Calculates the slope at each pixel,
* Displays a heatmap with color-coded elevations,
* Overlays gradient vectors pointing in the direction of maximum increase.

This helps visualize **how partial derivatives and gradients behave** in a real-world context.

---

## 🧪 8. Testing and Validation

To verify the system is working correctly:

```bash
pytest --cov
```

You should see output like:

```
==================== test session starts ====================
collected 6 items
tests/test_capture.py .....                        [ 40%]
tests/test_calculus.py ....                        [100%]
================= 9 passed in 3.45s ==========================
```

---

## 🧰 9. Troubleshooting

| Problem                    | Possible Cause                              | Solution                                                |
| -------------------------- | ------------------------------------------- | ------------------------------------------------------- |
| **Camera not detected**    | Device not connected or used by another app | Close other apps or check camera permissions            |
| **App closes immediately** | Missing dependencies                        | Run `pip install -r requirements.txt`                   |
| **Slow performance**       | Low-end hardware                            | Use `requirements-light.txt` or lower camera resolution |
| **No GUI window appears**  | Tkinter not installed                       | Reinstall Python (Tkinter comes by default)             |

---

## 👥 10. Team Credits

| Name                             | Role                                |
| -------------------------------- | ----------------------------------- |
| **Alejandro Botina Herrera**     | Technical Lead & System Architect   |
| **Andreina Olivares Cabrera**    | Interface Developer & Documentation |
| **Jonathan Joel Ruviño**         | Testing & Numerical Computation     |
| **Kiara Vanessa Muñoz Bayter**   | Environment Setup & Visualization   |
| **Víctor Manuel Barrero Acosta** | Capture Systems & Demonstrations    |

---

## 📚 11. License

This project is distributed under the **Apache License 2.0**.
You may freely use, modify, and distribute it for academic purposes.
For details, see the [LICENSE](../LICENSE) file.

---

## 🏁 12. Summary

**TopoVision** bridges the gap between **mathematical theory** and **visual intuition**.
By combining calculus, computer vision, and real-time visualization, it offers a unique way
to understand surface behavior through direct experimentation.

---

**TopoVision Development Team — 2025**

> “When numbers shape reality, vision becomes understanding.”
