import numpy as np
import matplotlib.pyplot as plt


def x(t):
    return 16 * np.sin(t) ** 3


def y(t):
    return 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)


n = 9

a, b = 0, 2 * np.pi
t_values = np.linspace(a, b, n)

x_values = x(t_values)
y_values = y(t_values)


coeff_x = np.polyfit(t_values, x_values, n - 1)
coeff_y = np.polyfit(t_values, y_values, n - 1)

poly_x = np.poly1d(coeff_x)
poly_y = np.poly1d(coeff_y)

t_fine = np.linspace(a, b, 100)
x_interp = poly_x(t_fine)
y_interp = poly_y(t_fine)

plt.figure(figsize=(8, 8))
plt.plot(x_values, y_values, "ro", label="Sample Points")
plt.plot(x_interp, y_interp, "b-", label="Polynomial Interpolation")
plt.plot(x(t_fine), y(t_fine), "g--", label="Actual Graph")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Parametric Interpolation of a Circle")
plt.axis("equal")
plt.grid()
plt.show()
