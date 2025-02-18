import numpy as np
import matplotlib.pyplot as plt


def f1(t, k):
    return


def f2(t, k):
    return np.sin(k * t)


def f3(t, k):
    return t**k


def g(x, c, M):
    res = c[0]
    for i in range(1, int(M / 2)):
        res += c[i] * f1(x, i)
    for i in range(int(M / 2), M):
        res += c[i] * f2(x, i - int(M / 2) + 1)
    return res


N = 4
M = 4
x = np.array([0, 1, 2, 3])
y = np.array([1, 2, 3, 2])

A = np.zeros((N, M))
b = np.zeros(N)

for i in range(N):
    A[i, 0] = 1
    for j in range(1, M):
        if i < M / 2:
            A[i, j] = f1(x[i], j)
        else:
            A[i, j] = f2(x[i], j - M / 2 + 1)
    b[i] = y[i]

print(f"AT*A: {A.T @ A} ")

c = np.linalg.solve(A.T @ A, A.T @ b)

print(f"computed coeficient: {c}")

x_fine = np.linspace(0, 3, 100)
g_values = g(x_fine, c)

plt.figure(figsize=(8, 8))
plt.plot(x_fine, g_values, label="g(x)")
plt.scatter(x, y, label="data points")
plt.legend()
plt.show()
