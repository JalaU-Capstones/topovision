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

Once installed, simply run:

```bash
python -m src.topovision.app
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
   The processed data is displayed as:

   * A **heatmap** representing height/intensity levels.
   * **Vector arrows** showing the direction and magnitude of the gradient.

5. **Interaction**
   Users can select regions or points directly on the GUI to analyze specific areas.

---

## 🖱️ 6. User Interface Controls

| Button                       | Description                                               |
| ---------------------------- | --------------------------------------------------------- |
| **Open Camera**              | Starts the camera feed and begins processing.             |
| **Pause** *(future)*         | Temporarily freezes the analysis.                         |
| **Exit**                     | Safely stops all processes and closes the app.            |
| **Select Region** *(future)* | Allows users to define a custom ROI (region of interest). |

💡 *Note:* During the early prototype (Phase 1–2), only “Open Camera” and “Exit” are active.
Other buttons will be enabled in later phases.

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
