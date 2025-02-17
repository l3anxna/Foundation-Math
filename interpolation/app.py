from flask import Flask, render_template, request
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from model import (
    solve_sle_interpolation,
    lagrange_interpolation,
    evaluate_polynomial,
    parametric_interpolation,
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_type = request.form["input_type"]
        methods = request.form.getlist("methods")
        x_eval = request.form.get("x_eval")
        x_eval_float = None
        if x_eval:
            try:
                x_eval_float = float(x_eval)
            except ValueError:
                return render_template(
                    "index.html", error="Invalid x_eval value. Must be a number."
                )

        if input_type == "function":
            function_str = request.form["function_str"]
            interval_start = int(request.form["interval_start"])
            interval_end = int(request.form["interval_end"])
            degree = int(request.form["degree"])

            try:
                x_values = np.linspace(interval_start, interval_end, degree + 1)
                y_values = eval_function(function_str, x_values)
            except Exception as e:
                return render_template(
                    "index.html", error=f"Error evaluating function: {e}"
                )

            plot_data = {"Original": (x_values, y_values, f"Original: {function_str}")}
            polynomial_strings = {}
            evaluation_results = {}

            if "sle" in methods:
                coeffs_sle = solve_sle_interpolation(x_values, y_values)
                if coeffs_sle is not None:
                    y_sle = evaluate_polynomial(coeffs_sle, x_values)
                    plot_data["SLE"] = (x_values, y_sle, "SLE")
                    polynomial_strings["SLE"] = " + ".join(
                        [f"{coeff:.2f}*x^{i}" for i, coeff in enumerate(coeffs_sle)]
                    )
                    if x_eval_float is not None:
                        evaluation_results["SLE"] = evaluate_polynomial(
                            coeffs_sle, x_eval_float
                        )
                else:
                    polynomial_strings["SLE"] = "SLE failed"

            if "lagrange" in methods:
                poly_lagrange = lagrange_interpolation(x_values, y_values)
                y_lagrange = poly_lagrange(x_values)
                plot_data["Lagrange"] = (x_values, y_lagrange, "Lagrange")
                polynomial_strings["Lagrange"] = str(poly_lagrange)
                if x_eval_float is not None:
                    evaluation_results["Lagrange"] = poly_lagrange(x_eval_float)

            if "parametric" in methods:
                x_param, y_param = parametric_interpolation(x_values, y_values)
                plot_data["Parametric"] = (x_param, y_param, "Parametric")
                polynomial_strings["Parametric"] = (
                    "Parametric interpolation (x(t), y(t))"
                )
                evaluation_results["Parametric"] = (
                    "Not evaluable directly. Plot to see interpolation."
                )

            plot_filename = generate_plot(plot_data)

            return render_template(
                "index.html",
                plot_filename=plot_filename,
                function_str=function_str,
                interval_start=interval_start,
                interval_end=interval_end,
                degree=degree,
                polynomial_strings=polynomial_strings,
                methods=methods,
                x_eval=x_eval,
                evaluation_results=evaluation_results,
            )

        elif input_type == "file":
            file = request.files["file"]
            if file:
                try:
                    points = np.loadtxt(
                        file.read().decode("utf-8").splitlines(), delimiter=","
                    )
                    x_values = points[:, 0]
                    y_values = points[:, 1]
                    degree = len(x_values) - 1

                    plot_data = {"Data Points": (x_values, y_values, "Data Points")}
                    polynomial_strings = {}
                    evaluation_results = {}

                    if "sle" in methods:
                        coeffs_sle = solve_sle_interpolation(x_values, y_values)
                        if coeffs_sle is not None:
                            y_sle = evaluate_polynomial(coeffs_sle, x_values)
                            plot_data["SLE"] = (x_values, y_sle, "SLE")
                            polynomial_strings["SLE"] = " + ".join(
                                [
                                    f"{coeff:.2f}*x^{i}"
                                    for i, coeff in enumerate(coeffs_sle)
                                ]
                            )
                            if x_eval_float is not None:
                                evaluation_results["SLE"] = evaluate_polynomial(
                                    coeffs_sle, x_eval_float
                                )
                        else:
                            polynomial_strings["SLE"] = "SLE failed"

                    if "lagrange" in methods:
                        poly_lagrange = lagrange_interpolation(x_values, y_values)
                        y_lagrange = poly_lagrange(x_values)
                        plot_data["Lagrange"] = (x_values, y_lagrange, "Lagrange")
                        polynomial_strings["Lagrange"] = str(poly_lagrange)
                        if x_eval_float is not None:
                            evaluation_results["Lagrange"] = poly_lagrange(x_eval_float)

                    if "parametric" in methods:
                        x_param, y_param = parametric_interpolation(x_values, y_values)
                        plot_data["Parametric"] = (x_param, y_param, "Parametric")
                        polynomial_strings["Parametric"] = (
                            "Parametric interpolation (x(t), y(t))"
                        )
                        evaluation_results["Parametric"] = (
                            "Not evaluable directly. Plot to see interpolation."
                        )

                    plot_filename = generate_plot(plot_data)

                    return render_template(
                        "index.html",
                        plot_filename=plot_filename,
                        polynomial_strings=polynomial_strings,
                        methods=methods,
                        x_eval=x_eval,
                        evaluation_results=evaluation_results,
                    )

                except Exception as e:
                    return render_template(
                        "index.html", error=f"Error processing file: {e}"
                    )

        return render_template("index.html", methods=methods)

    return render_template("index.html")


def eval_function(function_str, x_values):
    function_str = function_str.replace("^", "**")

    safe_dict = {
        "x": x_values,
        "sin": np.sin,
        "cos": np.cos,
        "abs": np.abs,
        "pi": np.pi,
        "e": np.e,
    }

    try:
        y_values = eval(function_str, {"__builtins__": None}, safe_dict)
        if isinstance(y_values, (int, float)):
            y_values = np.full_like(x_values, y_values)
        return y_values
    except Exception as e:
        raise ValueError(f"Function evaluation error: {e}")


def generate_plot(plot_data):
    plt.figure(figsize=(8, 6))

    for label, (x_values, y_values, legend_label) in plot_data.items():
        if label == "Data Points":
            plt.plot(x_values, y_values, "o", label=legend_label)
        else:
            plt.plot(x_values, y_values, label=legend_label)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Polynomial Interpolation")
    plt.legend()
    plt.grid(True)

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    plt.close()

    img_data = base64.b64encode(img_buffer.read()).decode("utf-8")
    return "data:image/png;base64," + img_data


if __name__ == "__main__":
    app.run(debug=True)
