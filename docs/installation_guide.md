# 🚀 TopoVision — Installation Guide (v0.2.1)

This guide provides comprehensive instructions for installing the TopoVision 3D Topographic Analysis System.

---

## 1. System Requirements

Before you begin, ensure your system meets the following requirements:

*   **Python:** Version 3.11 or higher.
*   **Tkinter:** This GUI toolkit usually comes pre-installed with Python. On Linux, you might need to install it separately (e.g., `sudo apt-get install python3-tk` on Ubuntu/Debian).
*   **Camera:** A standard USB webcam or integrated camera.

---

## 2. Installation from PyPI (Recommended)

This is the easiest and most reliable way to get TopoVision up and running.

1.  **Ensure Python and pip are installed:**
    Make sure you have Python 3.11+ and its package installer `pip` available on your system.

2.  **Install TopoVision:**
    Open your terminal or command prompt and run:
    ```bash
    pip install topovision
    ```
    This command will download and install the latest stable version of TopoVision and all its required libraries.

3.  **Run the application:**
    Once installed, you can launch TopoVision directly from your terminal:
    ```bash
    topovision
    ```
    Or, if the direct command doesn't work:
    ```bash
    python -m topovision
    ```

---

## 3. Installation from Source (For Developers)

This method is for users who want to contribute to TopoVision or modify its source code.

#### Step 1: Clone the Repository

```bash
git clone https://github.com/JalaU-Capstones/topovision.git
cd topovision
```

#### Step 2: Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the environment
python3.11 -m venv .venv

# Activate the environment
source .venv/bin/activate  # On Linux/macOS
# .venv\Scripts\activate    # On Windows
```

#### Step 3: Install Dependencies in Editable Mode

Install the project and its development dependencies. The `-e` flag (editable) allows you to make changes to the source code without needing to reinstall.

```bash
pip install -e .[dev]
```

#### Step 4: Initialize Pre-commit Hooks

This step is recommended for contributors to ensure code quality and consistency.

```bash
pre-commit install
```

---

## 4. Running TopoVision After Installation

Once TopoVision is installed, you can run it using one of the following methods:

### Method 1: Using the `topovision` command (Recommended)

If you installed from PyPI or in editable mode, the `topovision` command should be available:
```bash
topovision
```

### Method 2: Using the provided run scripts (For source installations)

If you cloned the repository, these scripts simplify launching the application:

*   **On Linux/macOS:**
    ```bash
    ./run.sh
    ```
*   **On Windows:**
    ```bash
    .\run.bat
    ```

Upon successful execution, a GUI window will appear, and an interactive tutorial will guide you through the first steps.
