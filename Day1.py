import math

def f(x):
    return x**2 - 4

def bisection(a, b, tol):
    if f(a) * f(b) > 0:
        return "No root found in the given interval"
    
    n_iter = math.ceil(math.log2((b - a) / tol))
    print("Number of iterations:", n_iter)
    
    for _ in range(n_iter):
        c = (a + b) / 2
        if f(c) == 0 or (b - a) / 2 < tol:
            return c
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2

root = bisection(0, 3, 1e-10)
print("Approximate root:", root)