import numpy as np
import matplotlib.pyplot as plt

def F1(x):
    return np.sin(x)

def F2(x):
    return np.sin(3 * x)

def F3(x):
    return np.sin(5 * x)

def interpolate_and_plot(F, a, b, m, title):
    x_points = np.linspace(a, b, m)
    y_points = F(x_points)

    V = np.vander(x_points, m)
    coeffs = np.linalg.solve(V, y_points)

    def P(x):
        return np.polyval(coeffs, x)

    x_fine = np.linspace(a, b, 500)
    f_values = F(x_fine)
    p_values = P(x_fine)


    plt.figure()
    plt.plot(x_fine, f_values, label="Original Function", color="blue")
    plt.plot(x_fine, p_values, label="Interpolation Polynomial", linestyle="--", color="orange")
    plt.scatter(x_points, y_points, color="red", label="Interpolation Points")
    plt.legend()
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    plt.show()

a, b = 0, 4  
m = 5 

interpolate_and_plot(F1, a, b, m, "Interpolation of sin(x) on [0, 4]")
interpolate_and_plot(F2, a, b, m, "Interpolation of sin(3x) on [0, 4]")
interpolate_and_plot(F3, a, b, m, "Interpolation of sin(5x) on [0, 4]")
