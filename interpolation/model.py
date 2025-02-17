import numpy as np
from scipy.interpolate import lagrange
from scipy.interpolate import interp1d


def solve_sle_interpolation(x, y):
    V = np.vander(x, increasing=True)
    try:
        coeffs = np.linalg.solve(V, y)
    except np.linalg.LinAlgError:
        return None
    return coeffs


def lagrange_interpolation(x, y):
    poly = lagrange(x, y)
    return poly


def evaluate_polynomial(coeffs, x_val):
    if isinstance(x_val, np.ndarray):
        result = np.zeros_like(x_val)
        for i, coeff in enumerate(coeffs):
            result += coeff * (x_val**i)
        return result

    result = 0
    for i, coeff in enumerate(coeffs):
        result += coeff * (x_val**i)
    return result


def parametric_interpolation(x, y, num_points=100):
    t = np.linspace(0, 1, len(x))
    t_new = np.linspace(0, 1, num_points)

    x_interp = interp1d(t, x, kind="linear", fill_value="extrapolate")
    y_interp = interp1d(t, y, kind="linear", fill_value="extrapolate")

    x_new = x_interp(t_new)
    y_new = y_interp(t_new)

    return x_new, y_new
