import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


def F(x):
    return 1 / (1 + 25 * x**2)


x = np.linspace(-1, 1, 20)
y = F(x)


def plot_spline(x, y):
    cs = CubicSpline(x, y, bc_type="natural")

    x_new = np.linspace(-1, 1, 100)
    y_new = cs(x_new)

    plt.figure(figsize=(8, 8))
    plt.plot(x_new, y_new, label="Natural Cubic Spline", color="orange")
    plt.scatter(x, y, color="blue", label="Data Points")
    plt.legend()
    plt.show()


plot_spline(x, y)
