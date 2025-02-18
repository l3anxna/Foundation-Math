import numpy as np
import matplotlib.pyplot as plt


def f1(t):
    return np.cos(t)

def f2(t):
    return np.sin(t)

def f3(t):
    return t

def f4(t):
    return t ** 2

def f5(t):
    return np.log(t)

def g(x, c):
    return c[0] + c[1] * f1(x) + c[2] * f2(x) + c[3] * f3(x) + c[4] * f4(x) + c[5] * f5(x)

x = np.loadtxt("data.csv", delimiter= ',', usecols= 0)
y = np.loadtxt("data.csv", delimiter= ',', usecols= 1)

N = 500
A = np.zeros((N, 6))
b = np.zeros(N)

for i in range(N):
    A[i, 0] = 1
    A[i, 1] = f1(x[i])
    A[i, 2] = f2(x[i])
    A[i, 3] = f3(x[i])
    A[i, 4] = f4(x[i])
    A[i, 5] = f5(x[i])
    b[i] = y[i]

c = np.linalg.solve(A.T@A, A.T@b)
print(f"c is: {c}")
print(f"Resulting coefficients: c0={c[0]:.4f}, c1={c[1]:.4f}, c2={c[2]:.4f}, c3={c[3]:.4f}, c4={c[4]:.4f}, c5={c[5]:.4f}")

x_fine = np.linspace(1, 5, 1000)
g_values = g(x_fine, c)

plt.plot(x_fine, g_values, color = 'red', label = 'Regression Line')
plt.scatter(x, y, label = 'Data Points')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.savefig('guess_coe.png')
plt.show()