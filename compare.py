import matplotlib.pyplot as plt

def f(x):
    return x**2 - 4


def f_prime(x):
    return 2 * x


def f_alpha(x: float) -> float:
    return (-1 / 3) * (x**2 - 4) + x


def find_newton(f, f_prime, x0, num_iter):
    x_vals = []
    for _ in range(num_iter):
        x_vals.append(x0)
        x0 = x0 - f(x0) / f_prime(x0)
    return x0, len(x_vals), x_vals


def find_bisect(f, a, b, num_iters):
    x_vals = []
    if f(a) * f(b) > 0:
        print("No root found in the interval.")
        return None, 0, []
    for _ in range(num_iters):
        c = (a + b) / 2
        x_vals.append(c)
        if f(c) == 0:
            break
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2, len(x_vals), x_vals


def find_fixed(f_alpha, x0: float, num_iters: int):
    x_vals = []
    for _ in range(num_iters):
        x0 = f_alpha(x0)
        x_vals.append(x0)
    return x0, len(x_vals), x_vals


a = 0
b = 3
x0_newton = 0.5
x0_fixed = 0.5
num_iter = 50
real_solution = 2

use_newton = True
use_bisection = True
use_fixed_point = True

results = []
if use_newton:
    c_newton, it_newton, vals_newton = find_newton(f, f_prime, x0_newton, num_iter)
    errors_newton = [abs(x - real_solution) for x in vals_newton]
    results.append(("Newton", errors_newton))

if use_bisection:
    c_bisect, it_bisect, vals_bisect = find_bisect(f, a, b, num_iter)
    errors_bisect = [abs(x - real_solution) for x in vals_bisect]
    results.append(("Bisection", errors_bisect))

if use_fixed_point:
    c_fixed, it_fixed, vals_fixed = find_fixed(f_alpha, x0_fixed, num_iter)
    errors_fixed = [abs(x - real_solution) for x in vals_fixed]
    results.append(("Fixed Point", errors_fixed))

fig, ax = plt.subplots()
for method_name, errors in results:
    ax.plot(range(len(errors)), errors, label=method_name)

ax.set_yscale("log")
ax.set_title("Error on each step")
ax.set_xlabel("Iteration")
ax.set_ylabel("Error")
ax.legend()
plt.show()
