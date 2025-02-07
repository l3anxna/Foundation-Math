def f(x):
    return x**2 - 5 * x + 4


def f_prime(x):
    return 2 * x - 5


def newton_method(x0, tol, max_iter):
    x = x0
    for i in range(max_iter):
        fx = f(x)
        fpx = f_prime(x)
        if abs(fx) < tol:
            print(f"Converged in {i} iterations")
            return x
        x = x - fx / fpx
    print("Did not converge")
    return x


root = newton_method(-3, 1e-6, 100)
print("Approximate root:", root)
