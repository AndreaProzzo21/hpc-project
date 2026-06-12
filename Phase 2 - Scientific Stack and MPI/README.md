# Phase 2: The Scientific Stack & MPI

## Overview
In this phase we explore how to bypass Python's memory and GIL limitations using the Scientific Stack (NumPy/SciPy) and introduce distributed memory parallelism with MPI (`mpi4py`).

## Topics Covered

### 1. The Scientific Stack & Compilers
* **NumPy & Vectorization:** How contiguous memory arrays and vectorized operations (SIMD) completely bypass slow Python loops and the GIL.
* **SciPy Integration:** Using Python as a "glue language" to call highly optimized legacy Fortran/C libraries for complex math (e.g., linear algebra).
* **Compiler Insights:** A benchmark study showing that the compiler (e.g., Intel vs. GCC) and JIT compilation (Numba) often matter more for performance than the language itself.

### 2. Distributed Parallelism (mpi4py)
* **MPI Basics:** Understanding communicators, ranks, and the massive speed difference between lowercase and uppercase commands.
* **Parallel File I/O:** How to safely open, read, and write files simultaneously across multiple processes.
* **Point-to-Point Communication:** Exchanging data directly between two processes using blocking (`Send`, `Recv`) and non-blocking (`Isend`, `Irecv`) methods.
* **Collective Communication:** Synchronizing and moving data across the entire group using `Bcast`, `Scatter`, `Gather`, `Reduce`, and `Alltoall`.
* **Fortran vs. Python MPI:** A direct comparison table mapping standard Fortran MPI subroutines to their `mpi4py` equivalents.

---
*Note: All examples, theoretical anchors, and code snippets for these topics are contained within the Jupyter Notebooks (`.ipynb`) located in this directory.*