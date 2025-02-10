from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

def bisection_method(f, a, b, tol):
    f_a, f_b = f(a), f(b)
    iterations, errors = [], []

    if f_a * f_b >= 0:
        return None, None, None

    while (b - a) / 2 > tol:
        c = (a + b) / 2
        iterations.append(c)
        errors.append(abs(f(c)))

        if f(c) == 0:
            break
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c

    return (a + b)/2, len(iterations), (iterations, errors)

def newton_method(f, df, x0, tol, max_iter=100):
    iterations, errors = [], []
    x = x0

    for _ in range(max_iter):
        fx = f(x)
        iterations.append(x)
        errors.append(abs(fx))

        if abs(fx) < tol:
            break

        try:
            x = x - fx / df(x)
        except ZeroDivisionError:
            break

    return x, len(iterations), (iterations, errors)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            func_str = request.form['function']
            a = float(request.form['a'])
            b = float(request.form['b'])
            tol = float(request.form['tolerance'])

            x = sp.symbols('x')
            try:
                f_expr = sp.parse_expr(func_str)
            except SyntaxError as e:
                return render_template('error.html', error=f"Invalid function syntax: {str(e)}")

            f = sp.lambdify(x, f_expr, 'numpy')
            df = sp.lambdify(x, sp.diff(f_expr, x), 'numpy')

            root_bisect, iter_bisect, (bisect_vals, bisect_errors) = bisection_method(f, a, b, tol)
            root_newton, iter_newton, (newton_vals, newton_errors) = newton_method(f, df, (a+b)/2, tol)
            
            plt.figure()
            plt.semilogy(bisect_errors, label='Bisection')
            plt.semilogy(newton_errors, label='Newton')
            plt.xlabel('Iteration')
            plt.ylabel('Error')
            plt.legend()
            plt.savefig('static/convergence.png')

            return render_template('results.html',
                                func=func_str,
                                bisect_result=root_bisect,
                                newton_result=root_newton,
                                iter_bisect=iter_bisect,
                                iter_newton=iter_newton)

        except Exception as e:
            return render_template('error.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
