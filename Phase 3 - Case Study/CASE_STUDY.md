# CASE STUDY: Computation of PI, Area of Circle & Sphere Using Monte Carlo Method

## Overview

This section presents the case study in which PI, the area of a circle, and the volume of a sphere are computed. The program is written in Python.

This case study includes the use of the following concepts:

1. File I/O
2. NumPy arrays
3. Random Number Generation
4. Monte Carlo Method
5. MPI for parallelization
6. Collective Communication (Broadcast and Reduce)

---

## Monte Carlo Method

The Monte Carlo method is a statistical technique used to estimate numerical quantities using random sampling.

In this case study, the Monte Carlo method is used to estimate:

1. The value of π
2. The area of a circle
3. The volume of a sphere

The Monte Carlo method works by generating random points inside a known geometric region and estimating a quantity by determining the fraction of points that fall inside the target shape.

\[
\text{Probability} =
\frac{\text{Points inside the target shape}}
{\text{Total points}}
\]

---

## Estimating π Using a Circle

A circle of radius \(R = 0.5\) is inscribed in a square of area 1.

Random points are generated inside the square. The probability that a random point falls inside the circle is:

\[
\frac{\text{Points inside the target shape}}
{\text{Total points}}
=
\frac{\text{Area of Circle}}
{\text{Area of Square}}
=
\frac{\pi (0.5)^2}{1}
=
\frac{\pi}{4}
\]

Therefore, π can be estimated as:

\[
\pi_{estimate}
=
4 \times
\frac{\text{Points inside circle}}
{\text{Total points}}
\]

### Area of Circle

\[
\text{Area of Circle}
=
\pi_{estimate} r^2
\]

---

## Estimating π Using a Sphere

The volume of a sphere is:

\[
V = \frac{4}{3}\pi r^3
\]

The sphere is enclosed inside a cube of volume 1.

Therefore:

\[
\frac{\text{Points inside the target shape}}
{\text{Total points}}
=
\frac{\text{Volume of Sphere}}
{\text{Volume of Cube}}
=
\frac{\pi}{6}
\]

Thus:

\[
\pi_{estimate}
=
6 \times
\frac{\text{Points inside sphere}}
{\text{Total points}}
\]

### Volume of Sphere

\[
\text{Volume of Sphere}
=
\frac{4}{3}\pi_{estimate} r^3
\]

---

## Input Parameters

At startup, the program reads the input file:

```json
{
    "total_points": 1000000,
    "dimensions": 2,
    "radius": 0.5
}
```

---

## MPI Parallelization

Once the total number of points is read, the root process (usually rank 0) sends this data to all processes in the communicator using the Broadcast operation.

The total number of points is divided among the available MPI processes. Each process independently performs the Monte Carlo simulation to determine how many points fall inside the circle.

The implementation handles situations where the points cannot be distributed equally among all processes.

A point is considered inside the circle if:

\[
(x - 0.5)^2 + (y - 0.5)^2 \le 0.5^2
\]

---

## Collective Reduction

Each process computes the number of points lying inside the circle and sends this information to the root process using the MPI Reduce collective communication operation.

Reduce sums all local counts and returns the global count to the root process.

The root process then:

1. Estimates π.
2. Checks convergence against a threshold of `1.0e-5`.
3. If convergence is achieved, computes the area of the circle.
4. Otherwise, increases the number of sample points and broadcasts the updated value to all processes.

The process repeats until convergence is reached.

---

## Sphere Calculation

The same procedure is followed for estimating π and the volume of a sphere.

The only difference is that the simulation dimension is changed from:

```text
dimensions = 2
```

to

```text
dimensions = 3
```

---

## Output

At the end of execution, the program writes:

- Estimated value of π
- Area of circle or volume of sphere
- Total computation time

to the output file.

---

## Experimental Setup

The program was executed using:

- 2 processes
- 4 processes
- 8 processes
- 16 processes
- 20 processes

The effect of strong scaling is also presented and analyzed in the study.
