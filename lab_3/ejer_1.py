# ejer_1.py
from metodos_num import bisection, regula_falsi
import numpy as np
import matplotlib.pyplot as plt
import time
from math import pi


def V_spherical_cap(h, R=3.0):
    return pi * h**2 * (R - h/3.0)


def f(h, R=3.0, Vtarget=30.0):
    return V_spherical_cap(h, R) - Vtarget


def plot_function(R=3.0, Vtarget=30.0, a=0.0, b=None):
    if b is None:
        b = 2*R
    xs = np.linspace(a, b, 400)
    ys = [f(x, R, Vtarget) for x in xs]
    plt.figure(figsize=(8, 4))
    plt.axhline(0, color='k', linewidth=0.6)
    plt.plot(xs, ys, label=f"f(h)=V(h)-{Vtarget}")
    plt.xlabel("h (m)")
    plt.ylabel("f(h)")
    plt.title("Volumen tanque: f(h) = V(h) - V_target")
    plt.legend()
    plt.grid(True)
    plt.show()


def tanteo(a=0.0, b=6.0, inc=0.5):
    xs = np.arange(a, b, inc)
    intervals = []
    for i in range(len(xs)-1):
        if f(xs[i]) * f(xs[i+1]) <= 0:
            intervals.append((xs[i], xs[i+1]))
    return intervals


def main():
    R = 3.0
    Vtarget = 30.0
    print(f"Datos: R={R} m, V_target={Vtarget} m^3")
    print("Graficando f(h)...")
    plot_function(R, Vtarget)
    inc = float(
        input("Ingrese incremento para método de tanteo (p.ej. 0.5): ") or "0.5")
    print("Buscando intervalos donde cambia signo (método de tanteo)...")
    intervals = tanteo(0.0, 2*R, inc)
    print("Intervalos detectados (a,b):", intervals)
    if not intervals:
        print("No se detectaron cambios de signo con ese incremento.")
        return

    # Aplicar Bisección y Falsa posición en el primer intervalo encontrado (normalmente único)
    a, b = intervals[0]
    tol = float(input("Ingrese tolerancia (p.ej. 0.001): ") or "0.001")

    print("\n--- Método de Intervalo Medio (Bisección) ---")
    try:
        root_bis, it_bis, hist_bis, time_bis = bisection(
            lambda x: f(x, R, Vtarget), a, b, tol=tol, maxiter=200)
        print(
            f"Raíz aproximada h = {root_bis:.6f} m en {it_bis} iteraciones (tiempo {time_bis:.4f} s)")
    except Exception as e:
        print("Bisección falló:", e)

    print("\n--- Interpolación Lineal (Falsa posición) ---")
    try:
        root_rf, it_rf, hist_rf, time_rf = regula_falsi(
            lambda x: f(x, R, Vtarget), a, b, tol=tol, maxiter=200)
        print(
            f"Raíz aproximada h = {root_rf:.6f} m en {it_rf} iteraciones (tiempo {time_rf:.4f} s)")
    except Exception as e:
        print("Falsa posición falló:", e)

    # Comparación gráfica: función y raíces encontradas
    xs = np.linspace(0, 2*R, 400)
    ys = [f(x, R, Vtarget) for x in xs]
    plt.figure(figsize=(8, 4))
    plt.plot(xs, ys, label="f(h)")
    plt.axhline(0, color='k', linewidth=0.6)
    if 'root_bis' in locals():
        plt.plot(root_bis, 0, 'ro', label=f'Bisección: h={root_bis:.4f}')
    if 'root_rf' in locals():
        plt.plot(root_rf, 0, 'go', label=f'Falsa posición: h={root_rf:.4f}')
    plt.xlabel("h (m)")
    plt.ylabel("f(h)")
    plt.legend()
    plt.grid(True)
    plt.title("Comparación de métodos (Ejercicio 1)")
    plt.show()

    # Conclusiones impresas
    print("\n--- Conclusiones (Ejercicio 1) ---")
    if 'time_bis' in locals() and 'time_rf' in locals():
        print(
            f"Tiempo bisección: {time_bis:.4f}s, tiempo falsa posición: {time_rf:.4f}s")
        faster = "bisección" if time_bis < time_rf else "falsa posición"
        print(f"Más rápido: {faster}")
    print("- Ambos métodos encuentran raíces similares. La falsa posición suele converger en menos iteraciones en funciones suaves.")
    print("- La bisección garantiza reducción del intervalo en cada paso (convergencia segura).")
    print("\nParticipación en foro (simulada):")
    print("He implementado bisección y falsa posición para el tanque esférico. Probé incrementos distintos para tanteo y confirmé la raíz en ~h metros. Pregunta al foro: ¿qué tolerancia recomendarían para ingeniería (¿1e-3 o 1e-4?)")


if __name__ == "__main__":
    main()
