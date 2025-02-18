import numpy as np
import matplotlib.pyplot as plt

a = 0
b = 10
m = 50


def f(x):
    return c0 + c1 * x


x_points = np.loadtxt("x_points.txt")
y_points_noisy = np.loadtxt("y_points.txt")

A = np.zeros((2, 2))
B = np.zeros(2)

A[0, 0] = m
A[0, 1] = np.sum(x_points)
A[1, 0] = np.sum(x_points)
A[1, 1] = np.sum(x_points**2)

B[0] = np.sum(y_points_noisy)
B[1] = np.sum(y_points_noisy * x_points)

c = np.linalg.solve(A, B)
c0, c1 = c[0], c[1]


def P(x, c):
    return c[0] + c[1] * x


x_fine = np.linspace(a, b, 200)
f_values = f(x_fine)
p_values = P(x_fine, c)

plt.figure(figsize=(8, 8))
plt.plot(x_fine, f_values, label="f(x)", color="blue")
plt.plot(x_fine, p_values, label="P(x)", color="orange", linestyle="--")
plt.scatter(x_points, y_points_noisy, color="red", label="Data Points")
plt.title("Linear Fit to Noisy Data")
plt.xlabel("X Points")
plt.ylabel("Y Points")
plt.legend()
plt.grid()
plt.show()

print(f"c0 = {c0}")
print(f"c1 = {c1}")
