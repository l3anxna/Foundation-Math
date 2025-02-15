import numpy as np
from scipy.interpolate import lagrange
from scipy.interpolate import interp1d


def solve_sle_interpolation(x, y):
    n = len(x)
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
    if isinstance(x_val, np.ndarray):  # Handle array input for plotting
        result = np.zeros_like(x_val)
        for i, coeff in enumerate(coeffs):
            result += coeff * (x_val**i)
        return result

    # Handle single x_val
    result = 0
    for i, coeff in enumerate(coeffs):
        result += coeff * (x_val**i)
    return result


def parametric_interpolation(x, y, num_points=100):
    """
    Performs parametric interpolation using x and y coordinates.

    Args:
        x (np.ndarray): Array of x-coordinates.
        y (np.ndarray): Array of y-coordinates.
        num_points (int): Number of points to generate for the interpolated curve.

    Returns:
        tuple: Arrays of x and y coordinates for the interpolated curve.
    """

    t = np.linspace(0, 1, len(x))  # Normalize to [0, 1]
    t_new = np.linspace(0, 1, num_points)

    # Create interpolation functions for x(t) and y(t)
    x_interp = interp1d(
        t, x, kind="linear", fill_value="extrapolate"
    )  # Use linear interpolation
    y_interp = interp1d(
        t, y, kind="linear", fill_value="extrapolate"
    )  # Use linear interpolation

    # Generate points for the interpolated curve
    x_new = x_interp(t_new)
    y_new = y_interp(t_new)

    return x_new, y_new
