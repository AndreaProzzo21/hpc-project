# Python for High-Performance Computing

## Project Overview

This project explores how Python can be used in a High-Performance Computing
(HPC) context, where compiled languages such as Fortran are traditionally the
standard choice. The work starts by introducing Jupyter Notebooks as an
interactive environment for scientific computing, together with the fundamental
concepts of Python programming. These foundations are then used to compare
Python with Fortran and to show how Python's performance limitations can be
reduced through the scientific stack and distributed-memory parallelism.

The central idea is that pure Python is usually not suitable for heavy
CPU-bound numerical loops, mainly because of interpretation overhead, dynamic
typing, memory overhead, and the Global Interpreter Lock (GIL). However, Python
can still be effective in HPC when it is used as a high-level language for
orchestration, prototyping, data analysis, and interaction with optimized
compiled libraries.

The project is organized in three phases. Each phase builds on the previous one:
from core language fundamentals, to NumPy/SciPy and MPI, and finally to a
parallel Monte Carlo case study.

## Repository Structure

```text
Progetto/
|-- Phase 1 - Core Fundamentals/
|   |-- 01_JupyterLab.ipynb
|   |-- 02_IO_&_Error_Handling.ipynb
|   |-- 03_Data_Types_&_Structures_&Flow_Control.ipynb
|   |-- 04_OOP_Classes.ipynb
|   |-- 05_Core_Differences.ipynb
|   `-- README.md
|
|-- Phase 2 - Scientific Stack and MPI/
|   |-- 01_SciPy&NumPy.ipynb
|   |-- 02_MPI.ipynb
|   |-- 03_Extra_Insight.ipynb
|   `-- README.md
|
|-- Phase 3 - Case Study/
|   |-- CaseStudy.ipynb
|   |-- MPI_Scaling_Analysis.ipynb
|   |-- mc_results_mpi.txt
|   |-- mpi_montecarlo.py
|   |-- LYRA_RUN_GUIDE.md
|   `-- README.md
|
|-- requirements.txt
`-- README.md
```

## Phase 1 - Core Fundamentals

The first phase introduces the Python tools and language features needed to
understand the rest of the project. The work begins with JupyterLab, used as an
interactive environment for scientific computing and exploratory analysis. This
is useful for learning, documenting, testing small code fragments, and combining
code with explanations, although it is not the ideal execution environment for
large parallel HPC runs.

The phase then covers file input/output, error handling, data types, data
structures, flow control, functions, and classes. These topics are presented not
only as Python syntax, but also in comparison with Fortran. This comparison is
important because it highlights the different design philosophies of the two
languages: Python favors flexibility, readability, and productivity, while
Fortran favors static structure, direct numerical efficiency, and predictable
memory behavior.

The final part of the phase focuses on the main architectural differences that
matter in HPC:

- Python is interpreted, while Fortran is compiled ahead of time.
- Python uses dynamic typing, while Fortran relies on static typing.
- Standard Python threads are limited for CPU-bound code by the GIL.
- Python objects introduce more memory overhead than raw Fortran arrays.
- Fortran usually gives the programmer more direct control over contiguous
  memory and low-level numerical performance.

This phase establishes the main problem addressed by the rest of the project:
Python is productive and expressive, but pure Python alone is not enough for
efficient large-scale numerical computing.

## Phase 2 - Scientific Stack and MPI

The second phase shows how Python can overcome many of its native performance
limitations by relying on optimized scientific libraries and parallel computing
tools.

The first part focuses on NumPy and SciPy. NumPy arrays store numerical data in a
compact and contiguous form, closer to the memory model expected in scientific
computing. Vectorized operations allow computations to be executed in optimized
compiled code instead of slow Python loops. This reduces interpreter overhead
and can also take advantage of low-level optimizations such as SIMD instructions.

SciPy extends this approach by providing high-level interfaces to optimized
algorithms for linear algebra, sparse matrices, Fourier transforms, and other
scientific computing tasks. In this sense, Python acts as a "glue language": the
user writes clear high-level code, while the computationally expensive work is
delegated to optimized C, C++, or Fortran backends such as BLAS and LAPACK.

The second part introduces MPI through `mpi4py`. MPI is used for
distributed-memory parallelism, where multiple independent processes cooperate
by exchanging messages. This is especially relevant for Python because MPI
parallelism uses separate processes and therefore avoids the limitations of the
GIL for CPU-bound work.

The MPI notebooks cover:

- communicators, ranks, and process groups;
- point-to-point communication with `Send`, `Recv`, `Isend`, and `Irecv`;
- collective communication with `Bcast`, `Scatter`, `Gather`, `Reduce`, and
  `Alltoall`;
- parallel file I/O concepts;
- the difference between lowercase `mpi4py` methods, which handle generic
  Python objects, and uppercase methods, which work with buffer-like numerical
  data and are much more suitable for HPC;
- the correspondence between common Fortran MPI subroutines and their Python
  `mpi4py` equivalents.

This phase shows that Python can be used in HPC when the numerically intensive
parts are moved away from pure Python loops and into optimized libraries or
parallel processes.

## Phase 3 - Monte Carlo Case Study

The final phase applies the previous concepts to a complete case study: a
parallel Monte Carlo simulation for estimating pi, the area of a circle, and the
volume of a sphere.

The Monte Carlo method is based on random sampling. In the two-dimensional case,
random points are generated inside a square and the fraction of points that fall
inside the circle is used to estimate pi and the area of the circle. The same
idea is extended to three dimensions to estimate the volume of a sphere.

The implementation combines NumPy and MPI:

- NumPy is used to generate large arrays of random points efficiently.
- Each MPI process works on a portion of the total sampling work.
- `Bcast` is used to distribute configuration parameters from the root process.
- `Reduce` is used to combine the partial counts of points inside the target
  region.
- The final estimate is computed on the root process.

The case study also introduces dynamic convergence. Instead of using only a
fixed number of points, the program can continue increasing the sample size
until the estimate reaches a target precision. This connects numerical accuracy
with computational cost: a stricter convergence threshold generally requires
more samples and therefore more execution time.

This phase is organized around complementary materials:

- `CaseStudy.ipynb` introduces the exercise, the Monte Carlo method, and the
  parallelization strategy.
- `mpi_montecarlo.py` contains the MPI implementation used for the simulations.
- `mc_results_mpi.txt` stores the collected execution results.
- `MPI_Scaling_Analysis.ipynb` parses these results and studies the scaling
  behavior of the code.
- `LYRA_RUN_GUIDE.md` summarizes the practical steps needed to run the code on
  the university cluster.

Performance is analyzed through standard HPC metrics such as execution time,
speedup, and efficiency, starting from a 1-process reference run. The analysis
also includes throughput and the absolute error on the pi estimate, which helps
separate numerical quality from runtime behavior.

At the same time, the results must be interpreted carefully: because the code
uses a dynamic convergence criterion, different runs may stop after different
numbers of sampled points. For this reason, the scaling analysis is informative
but not equivalent to a perfectly controlled strong-scaling benchmark with a
strictly fixed workload.

## Main Takeaways

The main conclusion of the project is that Python should not be seen as a direct
replacement for Fortran in low-level numerical kernels. Pure Python loops are
usually too slow for HPC workloads, and the GIL prevents standard Python
threads from scaling efficiently on CPU-bound tasks.

However, Python becomes much more powerful when used together with the right
tools. NumPy and SciPy allow Python code to access optimized compiled routines
while keeping a readable high-level interface. MPI, through `mpi4py`, makes it
possible to use distributed-memory parallelism and run independent processes
across multiple CPU cores or nodes.

Fortran remains closer to the machine and is still extremely effective for
performance-critical numerical kernels. Python, on the other hand, is very
effective as a language for experimentation, workflow coordination,
post-processing, visualization, and high-level scientific programming.

The practical lesson is therefore not that Python replaces Fortran, but that the
two approaches can complement each other. In modern scientific computing, Python
can provide productivity and flexibility, while optimized compiled libraries and
parallel programming models provide the performance required by HPC workloads.

## Requirements and Execution

The required Python packages are listed in `requirements.txt`:

```text
numpy
scipy
matplotlib
mpi4py
jupyter
notebook
```

They can be installed with:

```bash
pip install -r requirements.txt
```

The notebooks can be opened with Jupyter:

```bash
jupyter notebook
```

To run the Monte Carlo MPI case study locally, an MPI runtime must also be
available on the system. The script can then be executed with a command such as:

```bash
mpirun -np 4 python "Phase 3 - Case Study/mpi_montecarlo.py"
```

The number after `-np` defines how many MPI processes are launched.

For execution on LYRA, the practical workflow used in this project is described
in `Phase 3 - Case Study/LYRA_RUN_GUIDE.md`. In particular, the cluster setup
relies on the available Anaconda Python distribution, a virtual environment
created with `--system-site-packages`, and a separate installation of `mpi4py`.

## Final Comment

This project follows a progressive path: first it identifies the limitations of
pure Python for HPC, then it introduces the scientific and parallel tools used
to overcome those limitations, and finally it applies them to a concrete Monte
Carlo simulation together with an analysis of the observed scaling behavior.

The overall result is a practical demonstration of how Python can be part of an
HPC workflow when it is used with the right abstractions, optimized numerical
libraries, and distributed-memory parallelism.
