# Phase 3: Monte Carlo HPC Case Study

This case study demonstrates how to apply distributed parallel computing to solve a computationally heavy math problem: estimating Pi, and consequentially the area of a circle and the volume of a sphere, using the Monte Carlo method.

Key technologies and concepts used include:
* **NumPy:** For fast, vectorized random number generation.
* **MPI (mpi4py):** For collective communication between CPU cores (broadcasting parameters with `Bcast`, gathering partial sums with `Reduce`).
* **Dynamic Convergence:** The program automatically scales the number of simulated points until it reaches the required precision. This allow us to increase the size of the problem by increaasing the level of precision of the estimate.
* **HPC Analysis:** Performance measurement using Strong Scaling (Speedup and Efficiency).

The complete theory, formulas, detailed code explanations, and scaling analysis can be found inside the Jupyter Notebook attached to this folder.