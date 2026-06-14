## Monte Carlo Method

The Monte Carlo method is a statistical technique used to estimate numerical quantities using random sampling.

In this case study, the Monte Carlo method is used to estimate:

1. The value of π
2. The area of a circle
3. The volume of a sphere

The Monte Carlo method works by generating random points inside a known geometric region and estimating a quantity by determining the fraction of points that fall inside the target shape.

$$
\text{Probability} =
\frac{\text{Points Inside Target Shape}}
{\text{Total Points}}
$$

---

## Estimating π Using a Circle

A circle of radius **0.5** is inscribed inside a square of area **1**.

The probability that a random point falls inside the circle is:

$$
\frac{\text{Points Inside Circle}}
{\text{Total Points}}
=
\frac{\text{Area of Circle}}
{\text{Area of Square}}
=
\frac{\pi (0.5)^2}{1}
=
\frac{\pi}{4}
$$

Therefore, π can be estimated as:

$$
\pi_{estimate}
=
4
\frac{\text{Points Inside Circle}}
{\text{Total Points}}
$$

### Area of Circle

Once π has been estimated, the area of the circle is calculated using:

$$
A = \pi_{estimate} r^2
$$

---

## Estimating π Using a Sphere

The volume of a sphere is given by:

$$
V = \frac{4}{3}\pi r^3
$$

The sphere of radius **0.5** is enclosed inside a cube of volume **1**.

Therefore:

$$
\frac{\text{Points Inside Sphere}}
{\text{Total Points}}
=
\frac{\text{Volume of Sphere}}
{\text{Volume of Cube}}
=
\frac{\frac{4}{3}\pi(0.5)^3}{1}
=
\frac{\pi}{6}
$$

Thus:

$$
\pi_{estimate}
=
6
\frac{\text{Points Inside Sphere}}
{\text{Total Points}}
$$

### Volume of Sphere

After estimating π, the volume of the sphere is computed as:

$$
V = \frac{4}{3}\pi_{estimate} r^3
$$

---

## Point Inclusion Test

A point is considered inside the circle if:

$$
(x - 0.5)^2 + (y - 0.5)^2 \le 0.5^2
$$

For the sphere, a point is considered inside if:

$$
(x - 0.5)^2 + (y - 0.5)^2 + (z - 0.5)^2 \le 0.5^2
$$