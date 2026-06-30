LuminaFDFD: High-Performance Optical Mode Solver

Theoretical Framework: The Physics of LuminaFDFD

1. From Maxwell’s Equations to the Eigenvalue Problem
   LuminaFDFD is based on the fundamental description of light as electromagnetic waves governed by Maxwell’s equations. For waveguides that do not change along the propagation direction, the full three-dimensional field problem can be reduced to a two-dimensional cross-sectional problem. This reduction is possible because the field profile remains invariant along the propagation axis except for a phase accumulation.

The core task is to determine how light propagates in such a structure, which is fully characterized by the propagation constant. This quantity determines confinement, phase velocity, and effective refractive index of each optical mode. LuminaFDFD reformulates Maxwell’s equations into a structured eigenvalue problem where each solution corresponds to a physically valid guided or radiative mode. The key advantage of this formulation is that it directly produces both field distributions and propagation constants in a unified mathematical framework, without relying on heuristic mode assumptions.

2. Discretization and Physical Consistency via the Yee Grid
   To solve the continuous electromagnetic equations numerically, the spatial domain is discretized using the Yee grid. This approach places electric and magnetic field components at interleaved spatial positions, reflecting the natural coupling structure of Maxwell’s curl equations.

This staggered representation is critical because it preserves the physical consistency of electromagnetic conservation laws at the discrete level. It ensures that field continuity conditions at material boundaries are automatically respected without additional constraints. It also improves numerical stability by preventing artificial solutions that do not correspond to any physical electromagnetic mode. In practice, this allows accurate modeling of sharp dielectric interfaces such as silicon–oxide boundaries, which are essential in integrated photonics.

3. Sparse Structure and Computational Efficiency
   The numerical system generated from the discretization is extremely large but highly structured. Each spatial point interacts only with its nearest neighbors, which means the resulting operator contains mostly zero entries. LuminaFDFD exploits this structure by storing and computing the system using sparse representations instead of dense matrices.

This sparsity is not only a computational optimization but also a direct reflection of physical locality: electromagnetic fields in a homogeneous medium couple locally through differential operators. By leveraging this property, the solver achieves high spatial resolution without exponential growth in memory or computation cost, making it practical to simulate realistic photonic devices on standard computing hardware.

4. Targeted Mode Extraction and Physical Selectivity
   In waveguide analysis, the full mathematical solution space contains many modes that are not physically useful, such as leaky radiation states. The primary interest is in guided modes that remain confined in the high-index region and carry optical power along the structure.

LuminaFDFD addresses this by transforming the numerical problem so that the solver naturally focuses on modes near a chosen physical regime. This allows efficient isolation of fundamental and higher-order guided modes without explicitly computing the full spectrum. The method improves convergence and ensures that the computed solutions correspond to physically meaningful optical states rather than numerical artifacts.

5. Physical Interpretation and Design Significance
   Beyond being a numerical tool, LuminaFDFD serves as a direct bridge between electromagnetic theory and photonic device design. The computed modes can be interpreted in terms of confinement strength, propagation loss tendencies, and field overlap with materials, which are critical parameters in integrated photonics. This enables systematic design of waveguides, couplers, and resonant structures based on first-principles physics rather than empirical tuning.
