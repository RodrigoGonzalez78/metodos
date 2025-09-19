# ejer_3.py
from metodos_num import fixed_point_iteration
import numpy as np
import matplotlib.pyplot as plt

# --- REEMPLAZAR si la guía tiene otra A(x).
# Ejemplo: empleamos una función plausible que crece con x (ajústala a la de la guía)


def A_of_x(x):
    # --- EJEMPLO: gasto en publicidad (modelo ejemplo)
    # Puedes reemplazar por la fórmula exacta de la guía si difiere.
    return 1000 + 2*(x-200) + 0.005*(x-200)**2


def R_of_x(x):
    return 5*x - A_of_x(x)

# Queremos R(x) = 1000 => 5x - A(x) - 1000 = 0
# Para iteración de punto fijo definimos g(x) con forma conveniente: x = g(x)
# Una forma simple: x = (A(x) + 1000)/5  => g(x) = (A(x) + 1000)/5


def g(x):
    return (A_of_x(x) + 1000)/5.0


def plot_problem(x0=200):
    xs = np.linspace(100, 300, 400)
    ys = [R_of_x(t) for t in xs]
    plt.figure(figsize=(8, 4))
    plt.plot(xs, ys, label="R(x)")
    plt.axhline(1000, color='k', linestyle='--', label="R=1000")
    plt.xlabel("x")
    plt.ylabel("R(x)")
    plt.title("Utilidad neta R(x)")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    print("Ejercicio 3 — Iteración y Aceleración de Aitken")
    plot_problem()
    tol = float(input("Ingrese tolerancia (ej. 1e-4): ") or "1e-4")
    x0 = float(input("Ingrese x0 (entorno 200): ") or "200")
    use_aitken = input(
        "Aplicar Aitken? (s/N): ").strip().lower().startswith('s')
    root, iters, seq, elapsed = fixed_point_iteration(
        g, x0, tol=tol, maxiter=500, aitken=use_aitken)
    print(
        f"Resultado: x ≈ {root:.6f} en {iters} iteraciones (tiempo {elapsed:.4f}s).")
    print("Secuencia (últimos 10):", np.array(seq[-10:]))
    # graficar secuencia sobre g(x)
    xs = np.linspace(150, 250, 300)
    plt.figure(figsize=(7, 5))
    plt.plot(xs, [g(t) for t in xs], label='g(x) (punto fijo)')
    plt.plot(xs, xs, label='y=x')
    plt.scatter(seq, seq, c='red', s=20, label='iterates')
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("g(x)")
    plt.grid(True)
    plt.title("Iteración de Punto Fijo y Aitken (si aplica)")
    plt.show()

    print("\nConclusiones (Ejercicio 3):")
    print("- Si |g'(x)| < 1 cerca de la solución, la iteración converge; Aitken puede acelerar si la secuencia es regular.")
    print("- Comparar tiempos y número de iteraciones entre con/ sin Aitken y justificar elección del método.")
    if use_aitken:
        print(
            "Observación: se aplicó Aitken delta^2 al final de la secuencia si fue posible.")
    print("\nForo (simulado): ¿Qué modelo de A(x) consideran más realista para publicidad en este mercado? ¿Cómo afecta la convexidad de A(x) a la convergencia del método de punto fijo?")


if __name__ == "__main__":
    main()
