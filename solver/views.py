from django.shortcuts import render
import sympy as sp
from sympy import latex


def newton_raphson(request):
    context = {}
    decimal_places = int(request.POST.get('decimal_places', 4))

    if request.method == 'POST':
        function = request.POST.get('function')
        initial_guess_str = request.POST.get('initialguess')

        if not function or not initial_guess_str:
            context['error'] = 'Please provide both function and initial guess'
        else:
            try:
                initial_guess = float(initial_guess_str)
                x = sp.symbols('x')

                try:
                    f_expr = sp.sympify(function)
                    f_prime_expr = sp.diff(f_expr, x)

                    context['function_str'] = str(f_expr)
                    context['derivative_str'] = str(f_prime_expr)
                    context['function_display'] = latex(f_expr)
                    context['derivative_display'] = latex(f_prime_expr)

                    result, iterations = perform_newton_raphson(f_expr, f_prime_expr, initial_guess)
                    context.update({
                        'result': result,
                        'iterations': iterations,
                        'function': function,
                        'initialguess': initial_guess_str,
                        'decimal_places': decimal_places
                    })

                except Exception as e:
                    context['error'] = f"Error in function: {str(e)}"

            except ValueError:
                context['error'] = 'Initial guess must be a valid number'

    return render(request, 'solver/solver.html', context)


def perform_newton_raphson(f_expr, f_prime_expr, x0, max_iter=10):
    x = sp.symbols('x')
    iterations = []

    f = sp.lambdify(x, f_expr, "math")
    f_prime = sp.lambdify(x, f_prime_expr, "math")

    for i in range(1, max_iter + 1):
        f_val = f(x0)
        f_der = f_prime(x0)
        if f_der == 0:
            raise ZeroDivisionError("Derivative is zero. Cannot continue.")

        x1 = x0 - f_val / f_der
        rel_error = abs((x1 - x0) / x1) * 100 if x1 != 0 else 0

        iterations.append({
            'iteration': i,
            'x': x0,
            'fx': f_val,
            'fprimex': f_der,
            'error': rel_error,
            'x_next': x1,
            'division': f_val / f_der,
            'f_eval_str': str(f_expr.subs(x, x0)).replace('**', '^'),
            'f_prime_eval_str': str(f_prime_expr.subs(x, x0)).replace('**', '^')
        })

        x0 = x1

    return x0, iterations