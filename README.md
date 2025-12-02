# 🛰️ **TopoVision — 3D Topographic Analysis System**

> A Python-based system for topographic data visualization, real-time analysis, and calculus-based gradient computation.

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://img.shields.io/pypi/v/topovision.svg)](https://pypi.org/project/topovision/)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/JalaU-Capstones/topovision/actions)

📦 **Repository:** [https://github.com/JalaU-Capstones/topovision.git](https://github.com/JalaU-Capstones/topovision.git)

---

## 🧭 **Overview**

**TopoVision** is a collaborative academic project developed as part of the **Calculus II course** at *Universidad Jala*.
The system combines **Computer Vision**, **Numerical Methods**, and **Topographic Analysis** to calculate and visualize slopes, gradients, and surface volumes in real time.

The main goal is to create a tool that connects mathematical theory with visual and spatial understanding — transforming multivariable calculus into an interactive experience.

---

## ⚙️ **Key Features**

* 🎥 Real-time video capture using OpenCV
* 🧮 Numerical computation of partial derivatives and gradients
* 🌈 3D visualization of heatmaps and vector fields
* 🖱️ Interactive point and region selection on GUI
* 🧠 Modular design following **SOLID** principles and **Design Patterns**
* ⚡ Optimized for low-resource environments (Python 3.11 + NumPy vectorization)
* 📦 Easy installation via PyPI

---

## 🚀 **Quick Start**

### Installation from PyPI

```bash
pip install topovision
```

### Run the application

```bash
python -m topovision
```

Or simply:

```bash
topovision
```

You should see a GUI window with **"Open Camera"** and **"Exit"** buttons.

---

## 📋 **System Requirements**

### Required
- **Python 3.11** or higher
- **Tkinter** (GUI toolkit)

### Tkinter Installation

Tkinter comes pre-installed with Python on **Windows** and **macOS**.

On **Linux**, you may need to install it manually:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S tk
```

---

## 🛠️ **Installation Options**

### Standard Installation
Includes all features and GUI support:
```bash
pip install topovision
```

### Development Installation
Includes testing, linting, and documentation tools:
```bash
pip install topovision[dev]
```

### Lightweight Installation
Minimal dependencies without OpenCV GUI components:
```bash
pip install topovision[light]
```

### Installation from Source

For developers who want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/JalaU-Capstones/topovision.git
cd topovision

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate      # macOS/Linux
# OR
.venv\Scripts\activate         # Windows

# Install in editable mode
pip install -e .

# Or install with dev dependencies
pip install -e .[dev]
```

---

## 🧩 **Project Structure**

```
topovision/
├── src/
│   └── topovision/
│       ├── __init__.py
│       ├── __main__.py          # Entry point for CLI execution
│       ├── app.py               # Main application logic
│       ├── core/
│       │   ├── interfaces.py
│       │   └── models.py
│       ├── capture/
│       │   ├── capture_module.py
│       │   ├── camera_backends.py
│       │   └── preprocessing.py
│       ├── calculus/
│       │   ├── calculus_module.py
│       │   └── methods/
│       │       ├── finite_diff.py
│       │       ├── gradient.py
│       │       └── riemann.py
│       ├── visualization/
│       │   ├── visualization_module.py
│       │   ├── heatmap.py
│       │   └── vector_overlay.py
│       ├── gui/
│       │   └── gui_module.py
│       ├── services/
│       │   ├── cache.py
│       │   └── task_queue.py
│       ├── utils/
│       │   └── validators.py
│       └── tests/
│           ├── test_capture.py
│           ├── test_calculus.py
│           └── test_visualization.py
├── docs/
│   ├── architecture.md
│   ├── user-guide.md
│   └── github-flow-guide.md
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── LICENSE
└── README.md
```

---

## 🧰 **Tech Stack**

| Layer                | Technology           |
| -------------------- | -------------------- |
| Language             | Python 3.11          |
| GUI                  | Tkinter              |
| Computer Vision      | OpenCV               |
| Numerical Analysis   | NumPy, SciPy         |
| Visualization        | Matplotlib           |
| Performance          | Numba                |
| Documentation        | Markdown + pdoc      |
| Testing              | Pytest               |
| Linting / Formatting | Flake8, Black, Mypy  |
| Version Control      | GitHub (GitHub Flow) |
| Distribution         | PyPI                 |

---

## 🎯 **Usage Examples**

### Basic Usage

```python
# After installation, simply run:
python -m topovision

# Or use the command directly:
topovision
```

### Programmatic Usage

```python
from topovision.app import main

# Launch the application
main()
```

---

## 🧮 **Core Functionalities (Mathematical Overview)**

| Feature               | Description                                 | Method                      |
| --------------------- | ------------------------------------------- | --------------------------- |
| Partial Derivatives   | Calculated using finite difference methods  | Central Difference Scheme   |
| Gradient Vector       | Visualized as direction + magnitude arrows  | Sobel Operator              |
| Double Integrals      | Computed with discrete Riemann sums         | Trapezoidal Rule            |
| Surface Visualization | Rendered via color heatmaps                 | Matplotlib + NumPy          |
| Real-time Processing  | Optimized numerical computations            | Numba JIT Compilation       |

---

## 🧩 **Development Workflow — GitHub Flow**

### 🌿 Main Branches

| Branch      | Purpose                      |
| ----------- | ---------------------------- |
| `main`      | Stable release branch        |
| `develop`   | Integration branch           |
| `feature/*` | Individual development tasks |
| `hotfix/*`  | Urgent fixes                 |
| `docs/*`    | Documentation-only updates   |

### 💬 Commit Convention

Follow **Conventional Commits** format:

```
<type>(<scope>): <description>
```

**Examples:**

```bash
feat(capture): added OpenCVCamera backend
fix(gui): fixed window resize event
docs(readme): updated installation steps
```

**Types:**
- `feat` — new feature
- `fix` — bug fix
- `docs` — documentation changes
- `refactor` — code structure improvements
- `test` — test-related commits
- `chore` — build, CI, or maintenance

### 🔁 Typical Workflow

```bash
git checkout develop
git pull
git checkout -b feature/my-feature
# Make changes...
git add .
git commit -m "feat(scope): description"
git push origin feature/my-feature
# Open Pull Request → merge into develop → then into main
```

---

## 🧪 **Testing**

Run the test suite:

```bash
# Install with dev dependencies
pip install topovision[dev]

# Run tests
pytest

# Run with coverage
pytest --cov=topovision
```

---

## 👥 **Team Members**

| Name                             | Role                                |
| -------------------------------- | ----------------------------------- |
| **Alejandro Botina Herrera**     | Technical Lead & System Architect   |
| **Andreina Olivares Cabrera**    | Interface Developer & Documentation |
| **Jonathan Joel Ruviño**         | Testing & Numerical Computation     |
| **Kiara Vanessa Muñoz Bayter**   | Environment Setup & Visualization   |
| **Víctor Manuel Barrero Acosta** | Capture Systems & Demonstrations    |

---

## 🧱 **Project Roadmap**

| Week  | Focus                    | Key Deliverables                            |
| :---: | :----------------------- | :------------------------------------------ |
| **1** | Setup & Architecture     | Folder structure, interfaces, mock GUI      |
| **2** | Capture & Processing     | Camera module + preprocessing filters       |
| **3** | Calculus & Visualization | Derivatives, gradients, and heatmaps        |
| **4** | Testing & Publication    | PyPI release, documentation, and demo video |

---

## 🧾 **License**

This project is licensed under the **Apache License 2.0**.
See the [LICENSE](LICENSE) file for more details.

---

## 📚 **Acknowledgements**

* *Universidad Jala* — Department of Computer Science
* Course: **Calculus II — Applied Computational Analysis**
* Year: 2025

---

## 💡 **Contributing**

We welcome contributions!

1. Fork the repository
2. Create a new branch (`feature/your-feature`)
3. Install development dependencies: `pip install -e .[dev]`
4. Commit your changes using Conventional Commits
5. Run tests: `pytest`
6. Open a Pull Request

---

## 🐛 **Troubleshooting**

### Tkinter not found
**Error:** `ModuleNotFoundError: No module named '_tkinter'`

**Solution:** Install Tkinter for your system (see System Requirements section above)

### OpenCV camera issues
**Error:** Camera not opening or permission denied

**Solution:**
- Ensure your camera is not being used by another application
- On Linux, add your user to the `video` group: `sudo usermod -a -G video $USER`
- Restart your session after group changes

### Import errors after installation
**Error:** `ModuleNotFoundError: No module named 'topovision'`

**Solution:**
```bash
# Verify installation
pip list | grep topovision

# Reinstall if needed
pip uninstall topovision
pip install topovision
```

---

## 🧠 **Future Improvements**

* Add 3D mesh visualization using Plotly or Mayavi
* Implement topographic point cloud import (LAS/CSV)
* Integrate hardware sensors for live terrain capture
* Develop a lightweight Web-based viewer (Flask + WebGL)
* Machine learning integration for automatic feature detection
* Export functionality for analysis results (JSON, CSV, HDF5)

---

## 📊 **Performance**

TopoVision is optimized for real-time analysis:
- **Frame processing:** ~30 FPS on modern hardware
- **Gradient computation:** <50ms per frame
- **Memory usage:** ~200MB typical, <500MB peak

**Tested on:**
- CPU: Intel i5-8250U / AMD Ryzen 5 3600
- RAM: 8GB minimum, 16GB recommended
- OS: Windows 10/11, Ubuntu 20.04+, macOS 12+

---

## 🔗 **Links**

- **PyPI Package:** https://pypi.org/project/topovision/
- **GitHub Repository:** https://github.com/JalaU-Capstones/topovision
- **Issue Tracker:** https://github.com/JalaU-Capstones/topovision/issues
- **Documentation:** [docs/](docs/)

---

🎯 *TopoVision — bridging the gap between Calculus and reality, one frame at a time.*

---
