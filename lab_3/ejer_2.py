# ejer_2.py
from sympy import symbols, sympify
from metodos_num import metodo_newton_raphson, check_fourier_like_conditions
import matplotlib.pyplot as plt
import numpy as np

x = symbols('x')
expr = 8*x + 0.3*x**2 - 0.0013*x**3 - 372  # P(x)


def plot_problem(a=0, b=400):
    xs = np.linspace(a, b, 600)
    def f(t): return 8*t + 0.3*t**2 - 0.0013*t**3 - 372
    ys = f(xs)
    plt.figure(figsize=(10, 4))
    plt.plot(xs, ys, label="P(x)")
    plt.axhline(0, color='k', linewidth=0.6)
    plt.xlim(a, b)
    plt.ylim(min(ys)*1.1, max(ys)*1.1)
    plt.grid(True)
    plt.legend()
    plt.xlabel("x")
    plt.title("Utilidad total P(x)")
    plt.show()


def apply_newton_on_interval(interval, x0_guess, tol=1e-3):
    print(f"\nAnalizando intervalo {interval} con inicio x0={x0_guess}")
    conds = check_fourier_like_conditions(expr, x, interval)
    print("Chequeo condiciones tipo Fourier (concavidad constante y derivada no nula):")
    print(
        f"Concavidad constante en el intervalo? {conds['concavity_constant']}")
    print(f"Derivada no nula en el intervalo? {conds['fprime_nonzero']}")
    print(
        f"M (estimado) = {conds['M_estimate']:.4g} (ver referencia sobre condiciones de convergencia de Newton).")
    root, its, hist, elapsed = metodo_newton_raphson(
        expr, x, x0_guess, tol=tol, maxiter=100)
    print(
        f"Newton-Raphson -> raíz: x = {root:.6f} en {its} iter. (tiempo {elapsed:.4f}s)")
    return root, its


def main():
    print("Ejercicio 2 — Punto de equilibrio impresoras")
    plot_problem(0, 400)
    tol = float(
        input("Ingrese tolerancia para Newton (p.ej. 0.001): ") or "0.001")
    # análisis en los dos intervalos indicados
    intervals = [(24, 26, 25), (250, 252, 251)]
    results = []
    for a, b, x0 in intervals:
        r, it = apply_newton_on_interval((a, b), x0, tol)
        results.append((a, b, r, it))
    # mostrar comparación
    print("\nComparación de raíces encontradas:")
    for a, b, r, it in results:
        print(f"Intervalo [{a},{b}] -> raíz ~ {r:.6f}, iteraciones {it}")
    print("\nConclusiones:")
    print("- Si la función cumple concavidad constante y derivada no nula en el intervalo,\n  Newton suele converger rápida y monotonamente desde el punto inicial indicado.")
    print("- Si falla la condición (p.ej. f' cambia de signo o f'' no mantiene signo),\n  la convergencia puede ser lenta o divergir. (Referencia: Newton–Fourier).")


if __name__ == "__main__":
    main()
