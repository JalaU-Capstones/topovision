# 🛰️ **TopoVision — 3D Topographic Analysis System**

> A Python-based system for topographic data visualization, real-time analysis, and calculus-based gradient computation.

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/JalaU-Capstones/topovision/actions)

📦 **Repository:** [https://github.com/JalaU-Capstones/topovision.git](https://github.com/JalaU-Capstones/topovision.git)

---

## 🧭 **Overview**

**TopoVision** is a collaborative academic project developed as part of the **Calculus II course** at *Universidad Jala*.
The system combines **Computer Vision**, **Numerical Methods**, and **Topographic Analysis** to calculate and visualize slopes, gradients, and surface volumes in real time.

The main goal is to create a tool that connects mathematical theory with visual and spatial understanding — transforming multivariable calculus into an interactive experience.

---

## ⚙️ **Key Features**

* 🎥 Real-time video capture using OpenCV.
* 🧮 Numerical computation of partial derivatives and gradients.
* 🌈 3D visualization of heatmaps and vector fields.
* 🖱️ Interactive point and region selection on GUI.
* 🧠 Modular design following **SOLID** principles and **Design Patterns**.
* ⚡ Optimized for low-resource environments (Python 3.11 + NumPy vectorization).

---

## 🧩 **Project Structure**

```
topovision/
├── src/
│   └── topovision/
│       ├── app.py
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
│       ├── tests/
│       │   ├── test_capture.py
│       │   ├── test_calculus.py
│       │   └── test_visualization.py
│       └── exceptions.py
├── docs/
│   ├── architecture.md
│   ├── user-guide.md
│   ├── api.md
│   ├── presentation.pptx
│   └── github-flow-guide.md
├── .gitignore
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
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
| Documentation        | Markdown + pdoc      |
| Testing              | Pytest               |
| Linting / Formatting | Flake8, Black, Mypy  |
| Version Control      | GitHub (GitHub Flow) |

---

## 🚀 **Installation Guide**

### 1️⃣ Clone the repository

```bash
git clone https://github.com/JalaU-Capstones/topovision.git
cd topovision
```

### 2️⃣ Create a virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate      # On macOS/Linux
# OR
.venv\Scripts\activate         # On Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the project

```bash
python -m src.topovision.app
```

You should see a GUI window with two buttons:
**“Open Camera”** and **“Exit”**.

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

* `feat` — new feature
* `fix` — bug fix
* `docs` — documentation changes
* `refactor` — code structure improvements
* `test` — test-related commits
* `chore` — build, CI, or maintenance

### 🔁 Typical Workflow

```bash
git checkout develop
git pull
git checkout -b feature/capture-module
# make changes...
git add .
git commit -m "feat(capture): implemented OpenCVCamera class"
git push origin feature/capture-module
# open Pull Request → merge into develop → then into main
```

---

## 🧮 **Core Functionalities (Mathematical Overview)**

| Feature               | Description                                 |
| --------------------- | ------------------------------------------- |
| Partial Derivatives   | Calculated using finite difference methods. |
| Gradient Vector       | Visualized as direction + magnitude arrows. |
| Double Integrals      | Computed with discrete Riemann sums.        |
| Surface Visualization | Rendered via color heatmaps.                |

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

## 🧱 **Project Roadmap (4 Weeks)**

|  Week | Focus                    | Key Deliverables                            |
| :---: | :----------------------- | :------------------------------------------ |
| **1** | Setup & Architecture     | Folder structure, interfaces, mock GUI      |
| **2** | Capture & Processing     | Camera module + preprocessing filters       |
| **3** | Calculus & Visualization | Derivatives, gradients, and heatmaps        |
| **4** | Testing & Presentation   | Final polish, documentation, and demo video |

---

## 🧾 **License**

This project is licensed under the **Apache License 2.0**.
See the [LICENSE](LICENSE) file for more details.

---

## 📚 **Acknowledgements**

* *Universidad Jala* — Department of Computer Science
* Course: **Calculus II — Applied Computational Analysis**
* Instructor: *[Professor’s Name]*
* Year: 2025

---

## 💡 **Contributing**

We welcome contributions!

1. Fork the repository
2. Create a new branch (`feature/your-feature`)
3. Commit your changes using Conventional Commits
4. Open a Pull Request

---

## 🧠 **Future Improvements**

* Add 3D mesh visualization using Plotly or Mayavi.
* Implement topographic point cloud import (LAS/CSV).
* Integrate hardware sensors for live terrain capture.
* Develop a lightweight Web-based viewer (Flask + WebGL).

---

🎯 *TopoVision — bridging the gap between Calculus and reality, one frame at a time.*

---
