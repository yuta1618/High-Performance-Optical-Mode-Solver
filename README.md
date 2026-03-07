# High-Performance-Optical-Mode-Solver
<<<<<<< HEAD
# LuminaFDFD: High-Performance Optical Mode Solver



## Theoretical Framework: The Physics of LuminaFDFD

### 1. From Maxwell’s Equations to the Eigenvalue Problem
The propagation of electromagnetic waves in a $z$-invariant waveguide is governed by the source-free Maxwell’s equations. By assuming a harmonic time dependence $e^{j\omega t}$ and a spatial dependence $e^{-j\beta z}$, we transform the partial differential equations into a transverse plane problem. 

The core challenge in waveguide analysis is solving for the propagation constant $\beta$. LuminaFDFD reduces this to a generalized eigenvalue problem:
$$(P \cdot Q) \mathbf{E}_{xy} = \beta^2 \mathbf{E}_{xy}$$
where $\mathbf{E}_{xy}$ represents the transverse electric field components ($E_x, E_y$). The effective index is then derived as $n_{eff} = \beta / k_0$. Unlike scalar approximations, this fully vectorial approach captures the essential coupling between $E_x$ and $E_y$, which is critical for high-index-contrast platforms like Silicon-on-Insulator (SOI).



### 2. The Yee Lattice: Geometry of Accuracy
The spatial discretization follows the Yee cell convention, a staggered grid where $E$ and $H$ field components are offset by half a grid cell. This is not merely a numerical trick; it is a fundamental geometric mapping that mimics the integral form of Faraday’s and Ampère’s laws.

* **Second-Order Precision**: By evaluating derivatives at the midpoints via central differences, we achieve $O(\Delta^2)$ accuracy.
* **Interface Conditions**: The Yee grid naturally handles the continuity of tangential $E$ and normal $D$ fields at dielectric boundaries—a notorious challenge for standard Cartesian grids.
* **Divergence Cleaning**: The staggered nature implicitly maintains $\nabla \cdot \mathbf{B} = 0$, preventing the emergence of unphysical "spurious modes" that often plague non-staggered finite element or finite difference methods.



### 3. Sparse Operator Matrix Construction
The computational efficiency of LuminaFDFD stems from its sparse matrix architecture. Instead of dense arrays, we construct the differential operators $D_x$ and $D_y$ using **Kronecker products** ($\otimes$). This allows us to map 1D finite differences across a 2D computational domain with minimal memory overhead.

The operators $P$ and $Q$ are defined such that:
- $Q$ maps the electric field to the magnetic field via the curl operation.
- $P$ maps the magnetic field back to the electric field.
By computing the product $A = P \cdot Q$, we create a "Hamiltonian-like" operator for the photonics domain. The sparsity of $A$ (typically $< 0.1\%$ non-zero elements) is exploited using the **Compressed Sparse Column (CSC)** format, enabling high-resolution simulations on consumer-grade hardware.



### 4. Guided Mode Extraction via Shift-Invert Arnoldi
Solving the entire spectrum of a $10^5 \times 10^5$ matrix is computationally prohibitive. However, in waveguide design, we are exclusively interested in **guided modes**—those with the highest $n_{eff}$ confined within the core.

LuminaFDFD employs the **Shift-Invert Arnoldi Method**. By applying a "spectral shift" $\sigma$ near the expected core index (e.g., $n_{Si} \approx 3.48$), we transform the eigenvalue problem to find the modes closest to our target. This ensures that the solver converges rapidly to the fundamental TE and TM modes, bypassing the infinite sea of radiation modes in the cladding.

---

## 🛠️ Implementation Philosophy: Why Python?
While raw performance is often associated with C++, the computational bottleneck in FDFD is dominated by the linear algebra backend. By leveraging `scipy.sparse.linalg` (which wraps highly optimized ARPACK and SuperLU libraries), LuminaFDFD achieves near-native performance while maintaining the extreme flexibility of Python. This makes the library an ideal bridge between rapid prototyping and rigorous academic research.
=======
Based on the Finite-Difference Frequency-Domain (FDFD) method, this solver discretizes Maxwell's equations on a staggered Yee-grid to compute the effective index and electromagnetic field distributions of complex waveguide cross-sections.
>>>>>>> d46dd07c5d8cf3c9396bc27e94d1c98ab0613e8d
