import numpy as np
import matplotlib.pyplot as plt

h = 1
k = 2
r = 3


def x(t):
    return h + r * np.cos(t)


def y(t):
    return k + r * np.sin(t)


t_fine = np.linspace(0, 2 * np.pi, 500)
x_fine = x(t_fine)
y_fine = y(t_fine)

plt.figure(figsize=(8, 8))
plt.plot(x_fine, y_fine, label="Circle", color="pink", linewidth=2)


plt.show()
