# 🚀 TopoVision — Detailed Installation Guide

This guide provides comprehensive instructions for installing the TopoVision 3D Topographic Analysis System. Choose the method that best suits your needs: installing directly from PyPI for general use, or installing from source for development and contribution.

---

## 1. System Requirements

Before you begin, ensure your system meets the following requirements:

*   **Python:** Version 3.11 or higher.
    *   *Note:* Tkinter, the GUI toolkit, usually comes pre-installed with Python on Windows and macOS. On Linux, you might need to install it separately (e.g., `sudo apt-get install python3-tk` on Ubuntu/Debian).
*   **RAM:** 4 GB (minimum), 8 GB (recommended)
*   **CPU:** Dual-core (minimum), Quad-core (recommended)
*   **Camera:** A 720p (or higher) USB webcam or integrated camera.
*   **Operating System:** Windows 10+, Ubuntu 22.04+, or macOS 13+.

---

## 2. Installation Options

### Option A: Install from PyPI (Recommended for Users)

This is the easiest way to get TopoVision up and running for general use. It installs the core application and its necessary dependencies.

1.  **Ensure Python and pip are installed:**
    Make sure you have Python 3.11+ and its package installer `pip` available on your system. You can check by running:
    ```bash
    python3.11 --version
    pip --version
    ```

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

#### Lightweight Installation (without OpenCV GUI components)

If you need a minimal installation without the full OpenCV library (e.g., for server environments or specific use cases), you can install the lightweight version:

```bash
pip install topovision[light]
```

---

### Option B: Install from Source (Recommended for Developers & Contributors)

This method is for users who want to contribute to TopoVision, modify its code, or access the latest development features.

#### Step 1: Clone the Repository

First, you need to get a copy of the TopoVision source code.

1.  **Open your terminal** or command prompt.
2.  **Navigate to your desired development directory.**
3.  **Clone the repository** using Git:
    ```bash
    git clone https://github.com/JalaU-Capstones/topovision.git
    ```
4.  **Change into the project directory:**
    ```bash
    cd topovision
    ```

#### Step 2: Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with other Python projects.

1.  **Create the virtual environment:**
    ```bash
    python3.11 -m venv .venv
    ```
    This creates a new directory named `.venv` in your project folder, containing a isolated Python environment.

2.  **Activate the virtual environment:**
    *   **On Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    *   **On Windows (Command Prompt):**
        ```bash
        .venv\Scripts\activate.bat
        ```
    *   **On Windows (PowerShell):**
        ```bash
        .venv\Scripts\Activate.ps1
        ```
    You should see `(.venv)` or a similar indicator in your terminal prompt, signifying that the virtual environment is active.

#### Step 3: Install Dependencies

Now, install the project's dependencies within your active virtual environment.

1.  **Install Core (Runtime) Dependencies:**
    These are the essential libraries required for TopoVision to run.
    ```bash
    pip install -e .
    ```
    The `-e .` (editable mode) flag installs the package in a way that allows you to make changes to the source code directly without needing to reinstall.

2.  **Install Development Dependencies (Optional, but Recommended for Contributors):**
    These include tools for testing, linting, formatting, and documentation.
    ```bash
    pip install -e .[dev]
    ```
    This command installs the `dev` extras defined in `pyproject.toml`.

#### Step 4: Initialize Pre-commit Hooks (Recommended for Contributors)

Pre-commit hooks help maintain code quality by automatically running checks (like formatting and linting) before you commit your changes.

1.  **Install the hooks:**
    ```bash
    pre-commit install
    ```
    Now, every time you run `git commit`, the configured checks will execute.

#### Step 5: Verify Installation (Run Tests)

It's a good practice to run the project's test suite to ensure everything is installed correctly and working as expected.

1.  **Run tests with coverage:**
    ```bash
    pytest --cov
    ```
    You should see output indicating that tests are collected and passed. For example:
    ```
    ==================== test session starts ====================
    collected X items
    src/topovision/tests/test_capture.py .....
    src/topovision/tests/test_calculus.py ....
    ================= X passed in Y.YYs ==========================
    ```

---

## 3. Running TopoVision (After Installation)

Once TopoVision is installed, you can run it using one of the following methods:

### Method 1: Using the `topovision` command (Recommended for PyPI installations)

If you installed from PyPI or in editable mode, the `topovision` command-line entry point should be available:
```bash
topovision
```

### Method 2: Using the provided `run.sh` or `run.bat` scripts (Recommended for Source installations)

If you cloned the repository, these scripts simplify launching the application by activating the virtual environment and then running TopoVision.

*   **On Linux/macOS:**
    ```bash
    ./run.sh
    ```
*   **On Windows:**
    ```bash
    .\run.bat
    ```

### Method 3: Running the main module (Advanced)

You can also run the main module directly, ensuring your virtual environment is active:
```bash
python -m topovision
```

Upon successful execution, a Tkinter GUI window will appear, ready for you to start your topographic analysis.
