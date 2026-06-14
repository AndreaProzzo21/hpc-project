# Phase 1: Core Fundamentals - Python vs. Fortran in HPC

## Overview
This phase establishes the foundational knowledge required to understand why and how Python is used in High-Performance Computing (HPC), traditionally dominated by compiled languages like Fortran. 

Through a series of Jupyter Notebooks, we explore the core architectural differences between the two languages, analyzing syntax, data structures, and the physical limitations that dictate parallel code design.

## Topics Covered

### 1. Architectural Differences & Limitations
* **Compilation vs. Interpretation:** Understanding the execution overhead of Python's runtime bytecode interpretation compared to Fortran's ahead-of-time optimized machine code.
* **Dynamic vs. Static Typing:** Analyzing the flexibility of Python's dynamic typing against the runtime type-checking overhead, contrasted with Fortran's strict compile-time bounds.
* **The Global Interpreter Lock (GIL):** A deep dive into why standard Python multithreading is ineffective for CPU-bound tasks, necessitating multiprocess paradigms (MPI).
* **Memory Overhead:** Comparing Fortran's raw, contiguous memory allocation with the fragmented nature of Python's object model (`PyObject`).

### 2. Syntax, Ecosystem, and HPC Comparisons
* **0.1 JupyterLab Environment:** An introduction to Literate Programming. We discuss the benefits for "Time-to-Science" data exploration and the strict limitations when running parallel HPC codes.
* **0.2 File I/O & Error Handling:** Syntax and commands for reading/writing data. We compare Python's flexible context managers and robust exception handling (`try-except`) against Fortran's rigid I/O routines.
* **0.3 Data Types, Structures & Flow Control:** Parameter sweeping and logic handling. We contrast Python's dynamic lists, dictionaries, and iteration mechanics with Fortran's static arrays and index-based loops.
* **0.4 Classes and Functions (OOP):** Exploring Object-Oriented concepts in Python to abstract physical problems, comparing them with Fortran's subroutines and modules.


---
*Note: All examples, theoretical concepts, and code snippets for these topics are contained within the Jupyter Notebooks (`.ipynb`) located in this directory.*