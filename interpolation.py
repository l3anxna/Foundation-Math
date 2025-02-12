import numpy as np
import matplotlib.pyplot as plt


def F(x):
    return np.sin(x)


a, b = 0, 2 * np.pi
m = 5

x_points = np.linspace(a, b, m)
y_points = F(x_points)
V = np.vander(x_points, m)
coeffs = np.linalg.solve(V, y_points)


def P(x, c):
    return np.polyval(c, x)


x_fine = np.linspace(a, b, 100)
f_values = F(x_fine)
p_values = P(x_fine, coeffs)

plt.plot(x_fine, f_values, label="Original Function", color="blue")
plt.plot(
    x_fine, p_values, label="Interpolation Polynomial", linestyle="--", color="orange"
)
plt.scatter(x_points, y_points, color="red", label="Interpolation Points")
plt.legend()
plt.title("Function Approximation using Interpolation Polynomial")
plt.xlabel("x")
plt.ylabel("y")
plt.grid()
plt.show()

print("Coefficients of the interpolation polynomial:", coeffs)
