import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def f(x):
    return (x**2) - 5 

start, end, tol = -3, 2, 1e-10


def bisection_with_tracking(start, end, tol):
    approximations = []
    
    for _ in range(100):
        mid = (start + end) / 2
        approximations.append(mid)

        if abs(f(mid)) < tol or (end - start) / 2 < tol:
            break

        if f(start) * f(mid) < 0:
            end = mid
        else:
            start = mid

    return approximations

approximations = bisection_with_tracking(start, end, tol)

x = np.linspace(start, end, 400)
y = f(x)

fig, ax = plt.subplots()
ax.plot(x, y, label="f(x)")
ax.axhline(0, color="black", linewidth=0.8)
approx_dots, = ax.plot([], [], "ro", markersize=5, label="Approximations")

def update(i):
    approx_dots.set_data(approximations[:i+1], [0] * (i+1))
    return approx_dots,

ani = animation.FuncAnimation(fig, update, frames=len(approximations), interval=500, repeat=False)

plt.legend()
plt.show()

ani.save("bisection_convergence.mp4", writer="ffmpeg")