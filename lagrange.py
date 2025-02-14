import numpy as np
import matplotlib.pyplot as plt


def F(x):
    return np.sin(x)


def lagrange_interpolation(x_points, y_points, x):
    n = len(x_points)
    P = 0
    for i in range(n):
        L_i = 1
        for j in range(n):
            if i != j:
                L_i *= (x - x_points[j]) / (x_points[i] - x_points[j])
        P += y_points[i] * L_i
    return P


a, b = 0, 4
m = 5


x_points = np.linspace(a, b, m)
y_points = F(x_points)


V = np.vander(x_points, m)
coeffs = np.linalg.solve(V, y_points)


def P_sle(x):
    return np.polyval(coeffs, x)


x_fine = np.linspace(a, b, 500)
f_values = F(x_fine)
p_sle_values = P_sle(x_fine)
p_lagrange_values = [lagrange_interpolation(x_points, y_points, xi) for xi in x_fine]

plt.figure(figsize=(8, 6))
plt.plot(x_fine, f_values, label="Original Function", color="blue")
plt.plot(
    x_fine,
    p_sle_values,
    label="Interpolation Polynomial (SLE)",
    linestyle="--",
    color="orange",
)
plt.plot(
    x_fine,
    p_lagrange_values,
    label="Interpolation Polynomial (Lagrange)",
    linestyle="-.",
    color="green",
)
plt.scatter(x_points, y_points, color="red", label="Interpolation Points")
plt.legend()
plt.title("Comparison of Interpolation Methods")
plt.xlabel("x")
plt.ylabel("y")
plt.grid()
plt.show()
