import numpy as np
import matplotlib.pyplot as plt

def F(x):
    return np.sin(x)

def F2(x):
    return np.sin(3*x)

def F3(x):
    return np.sin(5*x)

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

def plot_interpolation(func, a, b, m, title):
    x_points = np.linspace(a, b, m)
    y_points = func(x_points)

    V = np.vander(x_points, m)
    coeffs = np.linalg.solve(V, y_points)

    def P_sle(x):
        return np.polyval(coeffs, x)

    x_fine = np.linspace(a, b, 500)
    f_values = func(x_fine)
    p_sle_values = P_sle(x_fine)
    p_lagrange_values = [lagrange_interpolation(x_points, y_points, xi) for xi in x_fine]

    plt.figure(figsize=(8, 6))
    plt.plot(x_fine, f_values, label="Original Function", color="blue")
    plt.plot(x_fine, p_sle_values, label="Interpolation Polynomial (SLE)", linestyle="--", color="orange")
    plt.plot(x_fine, p_lagrange_values, label="Interpolation Polynomial (Lagrange)", linestyle="-.", color="green")
    plt.scatter(x_points, y_points, color="red", label="Interpolation Points")
    plt.legend()
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    plt.show()

a, b = 0, 4

functions = [F, F2, F3]
num_points = [5, 7, 9]

for func in functions:
    for m in num_points:
        func_name = func.__name__
        title = f"Interpolation of {func_name} on [0, 4] with {m} points"
        plot_interpolation(func, a, b, m, title)
