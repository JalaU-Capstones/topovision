# 👨‍💻 TopoVision — User Guide (v0.2.1)

> **Purpose:**
> This guide explains how to install, run, and use the **TopoVision 3D Topographic Analysis System**.
> It is written for academic users and reviewers who wish to test the system for Calculus II applications.

---

## 🧩 1. Overview

**TopoVision** is an educational software designed to connect **multivariable calculus** with **visual topographic analysis**.

It uses a standard webcam to:
- Capture surface or terrain data in real time.
- Compute **gradients**, **arc length**, and **surface volumes**.
- Visualize the data through **heatmaps** and interactive **3D surface plots**.
- Provide accurate, real-world measurements through **unit conversion** and **perspective calibration**.

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

### 📦 Installation from PyPI (Recommended)

```bash
pip install topovision
```

### 🛠️ Installation from Source

For developers who want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/JalaU-Capstones/topovision.git
cd topovision

# Create a virtual environment
python3.11 -m venv .venv
source .venv/bin/activate       # On Linux/macOS
# OR
.venv\Scripts\activate          # On Windows

# Install in editable mode with development dependencies
pip install -e .[dev]
```

---

## ▶️ 4. Running TopoVision

After installation, you can run TopoVision from your terminal:

```bash
topovision
```

The first time you run the application, an interactive tutorial will guide you through the initial steps.

---

## 🧠 5. Interactive Tutorials

TopoVision includes a built-in tutorial system to guide first-time users. On your first interaction with a key feature, a message box will appear explaining its purpose and how to use it.

Tutorials are provided for:
- **Initial Startup**: Guides you to open the camera.
- **Analysis Panel**: Explains the purpose of the main control panel.
- **Z-Factor**: Describes how height scaling works.
- **Scale**: Explains how to set the pixels-per-meter ratio for measurements.
- **Perspective Calibration**: Details how to correct for perspective distortion.
- **Analysis Buttons**: Explains what each calculation does when you first click it.

Your progress is saved in `user_settings.json` in the project's root directory, so tutorials are only shown once.

---

## 🖱️ 6. User Interface Controls

The main window is divided into the **Canvas** (left) and the **Analysis Panel** (right).

### Analysis Panel

This panel contains all the controls for performing calculations and managing the view.

| Control | Description |
| :--- | :--- |
| **Z-Factor** | A multiplier to scale the height of the data. A value > 1.0 exaggerates topographic features. |
| **Scale (px/m)** | Defines how many pixels in the image correspond to one meter in the real world. **Crucial for accurate measurements if not using perspective calibration.** |
| **Unit** | A dropdown to select the measurement unit for all calculation results (e.g., meters, feet). |
| **Calibrate Perspective** | Starts the 4-point perspective calibration process. See the "Perspective Calibration" section below for details. |
| **Calculate Gradient** | Computes the rate of change of height and displays it as a heatmap on the selected region. |
| **Calculate Volume** | Estimates the volume under the surface of the selected region. |
| **Calculate Arc Length** | Estimates the length of a curve across the horizontal center of the selected region. |
| **Toggle View** | Switches the canvas between the live camera feed and the last analysis result (e.g., a heatmap). |
| **Clear Selection** | Removes the selection rectangle from the canvas. |

### Main Window Buttons

| Button | Description |
| :--- | :--- |
| **Open/Pause Camera** | Starts or pauses the live camera feed. |
| **Open 3D Plot Window** | Opens a new window with an interactive 3D plot of the selected region. |
| **Exit** | Closes the application. |

---

## 📐 7. Performing Measurements and Analysis

### Step 1: Start the Camera

Click the **"Open Camera"** button to start the video feed.

### Step 2: Calibrate for Accurate Measurements

For the most accurate results, you must calibrate the perspective.

1.  Click **"Calibrate Perspective"**.
2.  The status bar will prompt you to select four points. Click the four corners of a known rectangle in the camera's view (e.g., a sheet of A4 paper, a book).
3.  After selecting the fourth point, input fields will appear in the analysis panel.
4.  Enter the **real-world width and height** of the rectangle in **meters**.
5.  Click **"Apply Calibration"**.

The system will automatically calculate the correct scale and apply it to all future measurements.

> **Note:** If you do not calibrate, you **must** set the **Scale (px/m)** value manually for calculations to be accurate.

### Step 3: Select a Region

Click and drag your mouse on the canvas to draw a rectangle over the area you want to analyze. The dimensions of the selection will be displayed in the status bar in both pixels and your chosen real-world unit.

### Step 4: Run an Analysis

With a region selected, click one of the calculation buttons:
- **Calculate Gradient**: Overlays a heatmap showing the slope.
- **Calculate Volume**: Displays the calculated volume in the status bar.
- **Calculate Arc Length**: Displays the calculated length in the status bar.

### Step 5: View in 3D

Click the **"Open 3D Plot Window"** button to see a live, interactive 3D surface plot of your selected region. The plot will update in real time as you move the selection.

---

## 🧪 8. Testing and Validation

To run the automated test suite:

```bash
pytest --cov
```

---

## 🧰 9. Troubleshooting

| Problem | Possible Cause | Solution |
| :--- | :--- | :--- |
| **Camera not detected** | Device not connected or used by another app | Close other apps or check camera permissions. |
| **App closes immediately** | Missing dependencies | Ensure you have installed the requirements from `pyproject.toml`. |
| **Measurements are inaccurate** | Incorrect scale or no calibration | Use the **"Calibrate Perspective"** tool or set the **Scale (px/m)** value manually. |

---

**TopoVision Development Team — 2025**
