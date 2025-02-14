import numpy as np
import matplotlib.pyplot as plt

h = 1
k = 2
r = 3


def x(t):
    return 16 * np.sin(t) ** 3


def y(t):
    return 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)


t_fine = np.linspace(0, 2 * np.pi, 500)
x_fine = x(t_fine)
y_fine = y(t_fine)

plt.figure(figsize=(8, 8))
plt.plot(x_fine, y_fine, label="Circle", color="lightcoral", linewidth=2)
ax = plt.gca()
ax.set_facecolor("mistyrose")

plt.show()
