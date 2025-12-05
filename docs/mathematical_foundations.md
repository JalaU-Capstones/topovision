# Mathematical Foundations of TopoVision (v0.2.1)

> **Purpose:**
> This document provides a rigorous mathematical exposition of the core concepts underpinning TopoVision's analytical capabilities. It is intended for mathematicians and engineers seeking to understand the theoretical basis of the system.

---

## 1. Introduction to Topographic Analysis

TopoVision is designed to analyze and visualize three-dimensional surfaces derived from two-dimensional image data, where pixel intensity represents a scalar field (e.g., elevation). The system employs various tools from multivariable calculus and linear algebra to extract meaningful information from these surfaces, such as slopes, curvatures, volumes, and arc lengths.

Let a surface be represented by a scalar field $z = f(x, y)$, where $(x, y)$ are coordinates in a two-dimensional domain.

---

## 2. Core Calculus Concepts in TopoVision

### 2.1. Partial Derivatives and the Gradient Vector

The foundation of slope analysis in TopoVision is the **gradient vector**. For a surface $z = f(x, y)$, the gradient, denoted $\nabla f$, is a vector that points in the direction of the steepest ascent at any given point. Its components are the partial derivatives of the function:

$$ \nabla f(x, y) = \left\langle \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right\rangle $$

-   $\frac{\partial f}{\partial x}$: The rate of change of height along the x-axis.
-   $\frac{\partial f}{\partial y}$: The rate of change of height along the y-axis.

In TopoVision, the image data is discrete. Therefore, we approximate these partial derivatives numerically using a **finite difference** method, specifically the central difference scheme, which is implemented efficiently by NumPy's `np.gradient` function.

Given a grid of pixel values, the partial derivatives at a point $(i, j)$ are approximated as:

$$ \frac{\partial f}{\partial x} \approx \frac{f(i, j+1) - f(i, j-1)}{2 \cdot \Delta x} $$
$$ \frac{\partial f}{\partial y} \approx \frac{f(i+1, j) - f(i-1, j)}{2 \cdot \Delta y} $$

Where $\Delta x$ and $\Delta y$ are the real-world distances between pixel centers, determined by the user-defined scale.

### 2.2. Volume Calculation via Double Integrals

The volume under a surface $z = f(x, y)$ over a region $R$ in the $xy$-plane is given by the double integral:

$$ V = \iint_R f(x, y) \,dA $$

In a computational context, we approximate this integral using a **Riemann sum**. The region $R$ is partitioned into small rectangles, each corresponding to a pixel. The volume of the column above each pixel is the pixel's area multiplied by its height (intensity).

The area of a single pixel, $\Delta A$, is calculated from the user-provided scale (in pixels per meter):

$$ \Delta A = (\text{meters per pixel})^2 = \left( \frac{1}{\text{scale}} \right)^2 $$

The total volume is the sum of the volumes of all pixel columns:

$$ V \approx \sum_{i} \sum_{j} f(x_i, y_j) \cdot \Delta A $$

Where $f(x_i, y_j)$ is the intensity of the pixel at $(i, j)$. The final result is also scaled by the user-defined **Z-factor**.

### 2.3. Arc Length of a Surface Cross-Section

The arc length of a curve defined by a function $y = g(x)$ from $x=a$ to $x=b$ is given by the integral:

$$ L = \int_a^b \sqrt{1 + [g'(x)]^2} \,dx $$

In TopoVision, we calculate the arc length of a cross-section of the topographic surface. This is treated as a 3D path where the x-coordinate is the pixel index and the y-coordinate is the pixel's height.

For a discrete set of points $(x_i, y_i)$, the total arc length is approximated by summing the Euclidean distances between consecutive points:

$$ L \approx \sum_{i=1}^{N-1} \sqrt{(x_{i+1} - x_i)^2 + (y_{i+1} - y_i)^2} $$

The coordinates are first scaled to their real-world units:
-   $x_i$ is scaled using the `pixels_per_meter` value.
-   $y_i$ (height) is scaled using the `z_factor`.

This calculation is performed efficiently using NumPy's vectorized operations.

---

## 3. Linear Algebra for Perspective Correction

A key feature of TopoVision is its ability to correct for perspective distortion. This is achieved using a **homography transformation**, a concept from projective geometry.

### 3.1. The Homography Matrix

A homography is an invertible transformation that maps points in one plane to another. In our case, it maps the distorted, real-world plane captured by the camera to a corrected, "top-down" orthographic view.

This transformation is represented by a $3 \times 3$ matrix, $H$:

$$ H = \begin{pmatrix}
h_{11} & h_{12} & h_{13} \\
h_{21} & h_{22} & h_{23} \\
h_{31} & h_{32} & 1
\end{pmatrix} $$

Given a point in the source image $(x, y)$, its corresponding point in the destination (corrected) image $(x', y')$ is calculated as:

$$ \begin{pmatrix} x_p \\ y_p \\ w_p \end{pmatrix} = H \begin{pmatrix} x \\ y \\ 1 \end{pmatrix} $$

Where $x' = x_p / w_p$ and $y' = y_p / w_p$.

### 3.2. Computing the Homography

To compute $H$, we need at least four pairs of corresponding points between the source and destination planes. In TopoVision, the user provides these by:
1.  Selecting the four corners of a known rectangle in the source image.
2.  Providing the real-world width and height of that rectangle.

These four source points are mapped to the four corners of a destination rectangle with the correct aspect ratio. OpenCV's `getPerspectiveTransform` function is then used to solve for the matrix $H$.

### 3.3. Applying the Correction

Once $H$ is known, it can be used to:
-   **Warp the entire image or a region of interest (ROI)** into a top-down view for accurate analysis. This is done using OpenCV's `warpPerspective` function.
-   **Calculate accurate real-world dimensions** of any selection by transforming its corner points and measuring the distances in the corrected space.
-   **Display visualizations correctly** by using the inverse matrix, $H^{-1}$, to warp the generated heatmap back onto the original, uncorrected image, ensuring it perfectly overlays the selected region.

This two-step process of warping the data for analysis and then un-warping the result for visualization is crucial for maintaining both analytical accuracy and visual coherence.

---

## 4. Conclusion

The mathematical framework of TopoVision combines the analytical power of multivariable calculus with the geometric transformations of linear algebra. By approximating derivatives and integrals numerically and using homography to correct for perspective, the system provides a robust tool for quantitative topographic analysis from real-time video.
