#  TopoVision — System Architecture Overview

> **Purpose:**
> This document provides a detailed overview of the internal architecture of **TopoVision**,
> describing its core components, data flow, and design principles.
> It serves as a reference for contributors and maintainers.

---

##  1. Architectural Overview

TopoVision follows a **modular layered architecture** designed for scalability, maintainability,
and separation of concerns.

Each layer has a specific responsibility, and all interactions flow through well-defined interfaces.

```

┌─────────────────────────────┐
│         GUI Layer           │ ← (User Interaction)
├─────────────────────────────┤
│   Visualization & Capture   │ ← (Data Acquisition + Display)
├─────────────────────────────┤
│     Core Calculation        │ ← (Mathematical Processing)
├─────────────────────────────┤
│  Services & Infrastructure  │ ← (Caching, Queues, Validation)
├─────────────────────────────┤
│            Core             │ ← (Models, Interfaces, Exceptions)
└─────────────────────────────┘

```

---

## 2. Design Principles

TopoVision strictly follows the **SOLID** principles and **Design Patterns**
to ensure modularity and testability.

| Principle | Meaning | Application Example |
|------------|----------|----------------------|
| **S** — Single Responsibility | Each module/class should have one job. | `capture_module.py` only handles frame acquisition. |
| **O** — Open/Closed | Modules are open for extension, closed for modification. | New camera backends can be added via `interfaces.py`. |
| **L** — Liskov Substitution | Derived classes can replace base classes without breaking logic. | `MockCamera` can replace `OpenCVCamera` for testing. |
| **I** — Interface Segregation | Interfaces should be small and specific. | Separate `ICamera` and `IVisualizer` interfaces. |
| **D** — Dependency Inversion | High-level modules depend on abstractions, not implementations. | `app.py` injects dependencies dynamically. |

---

## 3. Project Directory Structure

```

src/topovision/
├── app.py                       # Application entry point (Facade pattern)
├── exceptions.py                # Custom exception types
│
├── core/                        # Core contracts and domain models
│   ├── interfaces.py             # Abstract base classes for modules
│   └── models.py                 # Data structures (dataclasses)
│
├── capture/                     # Camera and preprocessing modules
│   ├── capture_module.py         # Capture orchestration and camera implementations (OpenCV, Mock)
│   └── preprocessing.py          # Image normalization, grayscale, filters
│
├── calculus/                    # Mathematical processing (core logic)
│   ├── calculus_module.py        # Coordinates data and computation
│   └── strategies.py             # Mathematical strategies/algorithms
│
├── visualization/               # Rendering and graphical representation
│   ├── plot3d.py                 # 3D plotting utilities
│   ├── heatmap.py                # Surface heatmap visualization
│   ├── overlay.py                # Overlay functionalities
│   └── visualizers.py            # Integration point with GUI and various visualizers
│
├── gui/                         # User Interface (Tkinter-based)
│   ├── gui_module.py             # Main GUI window and event handlers
│   ├── i18n.py                   # Internationalization utilities
│   ├── theme.py                  # GUI theming
│   ├── canvas_panel.py           # Canvas for displaying visualizations
│   ├── plot3d_window.py          # Dedicated window for 3D plots
│   ├── analysis_panel.py         # Panel for analysis controls and display
│   └── camera_controller.py      # Controls for camera settings
│
├── services/                    # Supporting services
│   ├── service_provider.py       # Manages and provides services
│   └── task_queue.py             # Background processing or async queue
│
├── utils/                       # Helper utilities
│   └── math.py                   # Mathematical helper functions
│
└── tests/                       # Unit and integration tests
    ├── test_capture.py
    ├── test_calculus.py
    └── test_visualization.py

```

---

## 4. Module Responsibilities

| Module | Responsibility |
|---------|----------------|
| **app.py** | Entry point using the **Facade pattern**. Initializes dependencies, modules, and launches GUI. |
| **exceptions.py** | Defines custom exception types for robust error handling. |
| **core/interfaces.py** | Defines abstract interfaces (e.g., `ICamera`, `IVisualizer`, `ICalculusModule`). |
| **core/models.py** | Contains data classes like `FrameData`, `GradientResult`, etc. |
| **capture/** | Responsible for acquiring and preprocessing image frames, including camera implementations. |
| **calculus/** | Implements mathematical analysis (partial derivatives, gradients, surface integration) and defines calculation strategies. |
| **visualization/** | Renders analytical results (heatmaps, vector fields, 3D plots) and manages visualizers. |
| **gui/** | Manages user interaction through Tkinter, including panels, windows, and internationalization. |
| **services/** | Provides support utilities like service management and asynchronous tasks. |
| **utils/** | Contains lightweight mathematical helper functions. |

---

## 5. Data Flow Overview

```text
[ Camera Backend ]
       │
       ▼
 [ Preprocessing ]
       │
       ▼
 [ Calculus Module ]
 (Derivatives, Gradient, Integration)
       │
       ▼
 [ Visualization ]
 (Heatmap + Vectors)
       │
       ▼
 [ GUI ]
 (User Interaction, Display, Input)
```

### Example Workflow:

1. The user clicks **“Open Camera”** on the GUI.
2. `app.py` initializes the selected camera backend (`OpenCVCamera`).
3. Frames are sent to `preprocessing.py` (grayscale, normalization).
4. Processed data is analyzed by `calculus_module.py`.
5. Results (e.g., gradient vectors) are passed to `visualization_module.py`.
6. The GUI displays the processed results in real time.

---

## 6. Design Patterns Used

| Pattern      | Purpose                                               | Example in TopoVision                   |
| ------------ | ----------------------------------------------------- | --------------------------------------- |
| **Facade**   | Simplifies system access through a unified interface. | `app.py` orchestrates all subsystems.   |
| **Strategy** | Allows interchangeable algorithms.                    | Different gradient calculation methods. |
| **Observer** | GUI updates when new data arrives.                    | Real-time visualization updates.        |
| **Factory**  | Instantiates appropriate backends.                    | Camera selection logic in `app.py`.     |
| **Adapter**  | Standardizes interaction with different camera APIs.  | `camera_backends.py` abstracts OpenCV.  |

---

##  7. Testing Strategy

Tests are organized to ensure clarity and coverage:

* **Unit tests:** inside `src/topovision/tests/`
* **Integration tests:** executed automatically via GitHub Actions
* **Coverage goal:** ≥ 85%

Example:

```bash
pytest --cov=src/topovision --maxfail=1 --disable-warnings
```

---

## 8. Future Architectural Improvements

| Area          | Potential Enhancement                          |
| ------------- | ---------------------------------------------- |
| Performance   | Implement multiprocessing for frame analysis   |
| Visualization | Add 3D surface rendering (Plotly/Mayavi)       |
| Extensibility | Add plug-in system for new math methods        |
| Portability   | Migrate to PySide6 (Qt) for cross-platform GUI |
| Deployment    | Package with PyInstaller for standalone app    |

---

##  9. Architecture Summary Diagram

```text
                 ┌───────────────────────┐
                 │        GUI            │
                 │  (Tkinter Frontend)   │
                 └──────────┬────────────┘
                            │
               ┌────────────┴────────────┐
               │     Visualization       │
               │ (heatmap, vector field) │
               └────────────┬────────────┘
                            │
               ┌────────────┴────────────┐
               │       Calculus          │
               │  (Derivatives, Integrals)│
               └────────────┬────────────┘
                            │
               ┌────────────┴────────────┐
               │       Capture           │
               │   (Camera + Filters)    │
               └────────────┬────────────┘
                            │
               ┌────────────┴────────────┐
               │         Core             │
               │ (Interfaces + Models)   │
               └─────────────────────────┘
```

---

##  10. Summary

TopoVision is structured to:

* Encourage **clean separation of logic** between layers.
* Support **team collaboration** through well-defined modules.
* Allow **easy testing and scaling**.
* Reflect the **mathematical foundation** of topographic analysis in software form.

---

**TopoVision Development Team — 2025**

> “Mathematics meets visualization — designed for performance and clarity.”
