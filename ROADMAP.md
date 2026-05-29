# HPC PROJECT ROADMAP & REFERENCE GUIDE

## 📋 PHASE 1: JupyterLab & Python Core Fundamentals

*Objective: Establish the development environment, review foundational syntax, and analyze the architectural differences between Python and Fortran.*

### 🔹 Theoretical Anchors to Include in the Report:

* **Compilation vs. Interpretation:** Explain that Fortran is a compiled language (producing optimized machine code ahead of time), whereas Python is interpreted/compiled to bytecode at runtime, introducing initialization and execution overhead.
* **Dynamic vs. Static Typing:** Discuss how Python's dynamic typing provides massive flexibility but requires runtime type-checking, which slows down execution compared to Fortran’s static, compile-time bound variables.
* **The Global Interpreter Lock (GIL):** A crucial topic for HPC. Explain that the GIL prevents multiple native threads from executing Python bytecodes at once, making standard Python multithreading ineffective for CPU-bound tasks (hence the strict reliance on multiprocessing/MPI).
* **Memory Overhead:** Contrast Fortran's raw, contiguous memory allocation with Python's object model (where even a simple integer is a C structure with reference counters and type info).

### 🔹 Practical Exercise Hint for the Team:

* **Exercise 1.1 (File I/O & Error Handling):** Write a script that reads a text file (`.dat`) containing large matrices or grid coordinates (simulating Fortran outputs). Use a `try-except` block to catch `FileNotFoundError` or `ValueError` during parsing. Convert rows into custom Python Python `classes` representing physical nodes, demonstrating data encapsulation.

---

### 📋 Additional Examples for PHASE 1: Core Fundamentals

**Example 1.2: Data Structures & Flow Control (Parameter Sweeping)**
*Context: In Fortran, managing heterogeneous data often requires complex derived types or multiple arrays. Python handles this elegantly with dictionaries and lists, which is highly useful for running simulations across a range of parameters.*

```python
# Simulating a parameter sweep for a physics model
simulation_parameters = {
    "temperature_K": [300, 400, 500],
    "pressure_atm": 1.0,
    "gas_constant": 8.314
}

results = []

# Flow control iterating directly over the list (no index variables needed)
for T in simulation_parameters["temperature_K"]:
    # Simple ideal gas volume calculation: V = RT/P
    V = (simulation_parameters["gas_constant"] * T) / simulation_parameters["pressure_atm"]
    results.append((T, V))
    
print(f"Simulation sweep completed. Results (T, V): {results}")

```

**Example 1.3: Classes, Functions, and Exceptions (Particle Kinematics)**
*Context: Demonstrating Object-Oriented Programming (OOP) and error handling. Python's `try-except` blocks prevent the entire HPC cluster from crashing due to a single mathematical anomaly (like division by zero).*

```python
class Particle:
    def __init__(self, mass, velocity):
        self.mass = mass
        self.velocity = velocity

    def compute_kinetic_energy(self):
        return 0.5 * self.mass * (self.velocity ** 2)

    def compute_acceleration(self, force):
        try:
            # Prevent division by zero if mass is improperly initialized
            return force / self.mass
        except ZeroDivisionError:
            print("Error: Particle mass cannot be zero. Setting acceleration to 0.0")
            return 0.0

# Instantiating the class and testing the exception
photon = Particle(mass=0.0, velocity=299792458)
accel = photon.compute_acceleration(force=10.0) 

```

---

## 📋 PHASE 2: The Scientific Stack & MPI Integration

*Objective: Transition from pure Python loops to vectorized operations, and translate Fortran MPI concepts into `mpi4py` equivalents.*

### 🔹 Theoretical Anchors to Include in the Report:

* **NumPy Vectorization & SIMD:** Explain how NumPy bypasses Python's slow loops by executing operations in compiled C/Fortran arrays under the hood, leveraging SIMD (Single Instruction, Multiple Data) instructions.
* **Memory Layout (C vs. Fortran Order):** Note that NumPy arrays defaults to C-contiguous (row-major), whereas Fortran uses column-major order. Explain how setting `order='F'` in NumPy can optimize interoperability or specific directional memory accesses.
* **`mpi4py` Critical Distinction (The Capitalization Rule):**
* *Lowercase API (`comm.send`, `comm.recv`, `comm.bcast`):* Uses Python’s `pickle` module to serialize arbitrary objects. It introduces high latency and CPU overhead.
* *Uppercase API (`comm.Send`, `comm.Recv`, `comm.Bcast`):* Communicates memory-contiguous buffers (like NumPy arrays) directly via underlying C/Fortran MPI libraries. **This achieves near-native Fortran communication speeds.**



### 🔹 Practical Exercise Hint for the Team:

* **Exercise 2.1 (Point-to-Point Benchmark):** Implement a simple ping-pong communication between Rank 0 and Rank 1. Compare the timing of sending a standard Python list using `comm.send` versus sending a vectorized NumPy array of the same size using `comm.Send`. Plot the latency difference.

---


### 📋 Additional Examples for PHASE 2: Scientific Stack & MPI

**Example 2.2: NumPy Vectorization vs. Native Loops**
*Context: This is the most critical concept to explain when comparing Python to Fortran. Native Python loops are extremely slow. NumPy pushes the loop down to compiled C/Fortran code.*

```python
import numpy as np
import time

N = 10_000_000
# Initialize arrays
x = np.random.rand(N)
y = np.random.rand(N)

# 1. Native Python Loop (Slow - similar to unoptimized Fortran without flags)
start_time = time.time()
distance_loop = [ (x[i]**2 + y[i]**2)**0.5 for i in range(N) ]
print(f"Native loop time: {time.time() - start_time:.4f} seconds")

# 2. NumPy Vectorization (Fast - leverages SIMD and contiguous memory)
start_time = time.time()
distance_vec = np.sqrt(x**2 + y**2)
print(f"NumPy vectorization time: {time.time() - start_time:.4f} seconds")

```

**Example 2.3: Leveraging SciPy for Advanced Physics**
*Context: HPC codes often require solving large linear systems (e.g., implicit PDE solvers). Instead of writing a solver from scratch in Fortran, Python uses SciPy, which wraps highly optimized LAPACK/BLAS Fortran libraries.*

```python
import numpy as np
from scipy import linalg

# Solving a linear system A*x = b (e.g., steady-state heat distribution)
# Matrix A (coefficients) and vector b (boundary conditions)
A = np.array([[4, -1, 0], 
              [-1, 4, -1], 
              [0, -1, 4]])
b = np.array([15, 10, 15])

# scipy.linalg.solve is significantly faster and more stable than manual matrix inversion
temperatures = linalg.solve(A, b)
print(f"Solved temperatures at nodes: {temperatures}")

```

**Example 2.4: MPI Collective Communications (Broadcast and Gather)**
*Context: Distributing a configuration dictionary to all nodes, computing a vectorized chunk of data, and gathering it back. This highlights the use of uppercase `Bcast` and `Gather` for memory-buffer efficiency.*

```python
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# 1. Broadcasting parameters (lowercase 'bcast' is fine for small dictionaries)
if rank == 0:
    params = {'steps': 1000, 'dt': 0.01}
else:
    params = None
params = comm.bcast(params, root=0)

# 2. Parallel Computation: Each rank computes its own NumPy array chunk
local_data = np.ones(100, dtype=np.float64) * rank * params['dt']

# 3. Gathering data (Uppercase 'Gather' is MANDATORY for fast NumPy array communication)
if rank == 0:
    # Rank 0 must pre-allocate the memory to receive all data
    global_data = np.empty(size * 100, dtype=np.float64)
else:
    global_data = None

comm.Gather(sendbuf=local_data, recvbuf=global_data, root=0)

if rank == 0:
    print(f"Root process successfully gathered {len(global_data)} elements.")

```

## 📋 PHASE 3: Parallel Case Studies Implementation

*Objective: Develop, debug, and execute the selected physical simulations using parallel patterns.*

### 💡 Case Study 1: Monte Carlo Estimation of $\pi$

* **HPC Pattern:** Embarrassingly Parallel / High Throughput.
* **Theoretical Concept:** Statistical sampling where independent tasks require zero communication during execution, culminating in a final aggregation phase.
* **Implementation Steps & Hints:**
1. Divide the total number of random samples $N$ uniformly across $p$ processes ($N_{local} = N / p$).
2. *Crucial Step:* Ensure each rank initializes a distinct random number generator seed using `numpy.random.default_rng(seed=rank)` to avoid generating identical parallel streams.
3. Each process generates local random $(x, y)$ points and checks if they fall inside the unit circle ($x^2 + y^2 \le 1$).
4. Use collective communication to aggregate the results on Rank 0:
```python
comm.Reduce(local_count, global_count, op=MPI.SUM, root=0)

```


5. Rank 0 computes the final value: $\pi \approx 4 \times \frac{\text{global\_count}}{N}$.



### 💡 Case Study 2: 2D Heat Equation via Finite Differences

* **HPC Pattern:** Domain Decomposition & Stencil Computation.
* **Theoretical Concept:** Discretization of a continuous PDE on a spatial grid where each cell's next state depends on its current neighbors (Jacobi Iteration).
* **Implementation Steps & Hints:**
1. Decompose the 2D matrix spatial grid into horizontal slices (1D decomposition) distributed across the available MPI processes.
2. Allocate **Ghost Cells (Halo Zones)**: Each process needs an extra row at the top and bottom to store boundary values owned by adjacent processes.
3. At every time step, execute point-to-point boundary exchanges using synchronous or non-blocking primitives:
```python
# Exchange top and bottom ghost layers simultaneously
comm.Sendrecv(sendbuf=local_boundary, dest=neighbor_up, recvbuf=ghost_layer, source=neighbor_down)

```


4. Update the interior grid using optimized NumPy array slicing (avoid explicit `for` loops inside the physics solver).
5. Use `comm.Gather` or `comm.Gatherv` to collect the full temperature grid at designated intervals for visualization in JupyterLab.



---

## 📋 PHASE 4: Performance Evaluation & Comparative Reporting

*Objective: Collect scaling data, analyze bottleneck differences, and synthesize the final document.*

### 🔹 Theoretical Anchors to Include in the Report:

* **Parallel Scaling Laws:** Define and compute **Speedup** ($S(p) = T_1 / T_p$) and **Parallel Efficiency** ($E(p) = S(p)/p$). Relate your scaling curves to *Amdahl's Law* (strong scaling limits due to serial fractions) and *Gustafson's Law* (weak scaling advantages).
* **The "Time-to-Science" vs. "Time-to-Solution" Trade-off:** Conclude by analyzing how Python drastically reduces code development, debugging, and data visualization times (Time-to-Science) compared to Fortran, even if Fortran retains a slight edge in raw, peak execution performance (Time-to-Solution).

### 🔹 Practical Exercise Hint for the Team:

* Run both case studies on varying process counts (e.g., $p = 1, 2, 4, 8$). Log the execution times, plot the strong scaling curves, and pinpoint where the communication overhead starts to dominate the computation.

---
