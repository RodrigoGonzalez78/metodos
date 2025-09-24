# metodos_num.py
"""
Métodos numéricos reutilizables:
- bisection (Intervalo Medio)
- regula_falsi (Interpolación lineal / Falsa posición)
- metodo_newton_raphson (con sympy para derivadas)
- fixed_point_iteration (opcional Aitken)
Cada función devuelve (root, iterations, history, elapsed_time).
"""

import time
import numpy as np
from math import isfinite
from sympy import lambdify


def bisection(f, a, b, tol=1e-3, maxiter=100):
    t0 = time.time()
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")
    history = []
    for i in range(1, maxiter+1):
        c = (a + b) / 2.0
        fc = f(c)
        history.append((i, a, b, c, fc))
        if abs(fc) < tol or (b - a)/2 < tol:
            return c, i, history, time.time()-t0
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    return (a+b)/2.0, maxiter, history, time.time()-t0


def regula_falsi(f, a, b, tol=1e-3, maxiter=100):
    t0 = time.time()
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")
    history = []
    x0, x1 = a, b
    f0, f1 = fa, fb
    for i in range(1, maxiter+1):
        x2 = x1 - f1*(x1 - x0)/(f1 - f0)
        f2 = f(x2)
        history.append((i, x0, x1, x2, f2))
        if abs(f2) < tol or abs(x2 - x1) < tol:
            return x2, i, history, time.time()-t0
        # update interval preserving sign
        if f0 * f2 < 0:
            x1, f1 = x2, f2
        else:
            x0, f0 = x2, f2
    return x2, maxiter, history, time.time()-t0


def metodo_newton_raphson(expresion_simbolica, variable, valor_inicial, tolerancia=1e-3, maximo_iteraciones=100):
    inicio_tiempo = time.time()
    funcion = lambdify(variable, expresion_simbolica, 'numpy')
    derivada = lambdify(variable, expresion_simbolica.diff(variable), 'numpy')
    valor_actual = float(valor_inicial)
    historial = []

    for numero_iteracion in range(1, maximo_iteraciones + 1):
        valor_funcion = float(funcion(valor_actual))
        valor_derivada = float(derivada(valor_actual))
        historial.append((numero_iteracion, valor_actual,
                         valor_funcion, valor_derivada))

        if abs(valor_funcion) < tolerancia:
            return valor_actual, numero_iteracion, historial, time.time() - inicio_tiempo

        if valor_derivada == 0:
            raise ZeroDivisionError("La derivada es cero en el punto actual.")

        nuevo_valor = valor_actual - valor_funcion / valor_derivada

        if abs(nuevo_valor - valor_actual) < tolerancia:
            return nuevo_valor, numero_iteracion, historial, time.time() - inicio_tiempo

        valor_actual = nuevo_valor

    return valor_actual, maximo_iteraciones, historial, time.time() - inicio_tiempo


def check_fourier_like_conditions(sympy_expr, sympy_var, interval):
    """
    Chequea condiciones tipo 'Fourier' (concavidad constante y derivada no nula)
    para dar evidencia de convergencia monotónica local del método de Newton.
    Devuelve un dict con información: sign_fpp, fprime_nonzero, M_estimate.
    """
    import numpy as np
    fprime = lambdify(sympy_var, sympy_expr.diff(sympy_var), 'numpy')
    fpp = lambdify(sympy_var, sympy_expr.diff(sympy_var, 2), 'numpy')
    a, b = interval
    xs = np.linspace(a, b, 50)
    fpp_vals = fpp(xs)
    fprime_vals = fprime(xs)
    # check sign of second derivative (concavity)
    try:
        sign_fpp = np.sign(fpp_vals)
        unique_signs = np.unique(sign_fpp[np.isfinite(sign_fpp)])
        concavity_constant = (len(unique_signs) == 1)
    except Exception:
        concavity_constant = False
    # derivative nonzero?
    fprime_nonzero = np.all(np.abs(fprime_vals) > 1e-12)
    # compute M = 1/2 sup |f''(x)| * sup 1/|f'(x)|
    sup_fpp = np.nanmax(np.abs(fpp_vals))
    sup_inv_fp = np.nanmax(1.0/np.abs(fprime_vals))
    M = 0.5 * sup_fpp * sup_inv_fp
    return {
        'concavity_constant': concavity_constant,
        'fprime_nonzero': bool(fprime_nonzero),
        'M_estimate': float(M),
        'fpp_sample_max': float(sup_fpp)
    }


def fixed_point_iteration(g_func, x0, tol=1e-4, maxiter=200, aitken=False):
    """
    g_func: función x -> g(x)
    aitken: si True aplica Aitken delta^2 a la secuencia generada (si posible)
    """
    t0 = time.time()
    xs = [float(x0)]
    for k in range(1, maxiter+1):
        x_next = float(g_func(xs[-1]))
        xs.append(x_next)
        if abs(xs[-1] - xs[-2]) < tol:
            elapsed = time.time() - t0
            if aitken and len(xs) >= 3:
                # aplicar Aitken a la última triple si posible
                x0a, x1a, x2a = xs[-3], xs[-2], xs[-1]
                denom = (x2a - 2*x1a + x0a)
                if abs(denom) > 1e-14:
                    x_hat = x0a - (x1a - x0a)**2 / denom
                    return x_hat, k, xs, elapsed
            return xs[-1], k, xs, elapsed
    # si no converge, aún podemos intentar Aitken sobre últimas tres
    elapsed = time.time()-t0
    if aitken and len(xs) >= 3:
        x0a, x1a, x2a = xs[-3], xs[-2], xs[-1]
        denom = (x2a - 2*x1a + x0a)
        if abs(denom) > 1e-14:
            x_hat = x0a - (x1a - x0a)**2 / denom
            return x_hat, maxiter, xs, elapsed
    return xs[-1], maxiter, xs, elapsed
