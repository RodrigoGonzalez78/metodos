import sympy as sp
from metodos_num import metodo_newton_raphson


def probar_metodo_newton_raphson():
    x = sp.symbols('x')
    expresion = x**3 - x - 1

    print("Prueba con valor inicial = 1")
    raiz1, iteraciones1, historial1, tiempo1 = metodo_newton_raphson(
        expresion, x, 1, tolerancia=1e-6)
    print(f"Raíz aproximada: {raiz1}")
    print(f"Iteraciones: {iteraciones1}")
    print(f"Tiempo de ejecución: {tiempo1:.6f} segundos\n")

    print("Prueba con valor inicial = 2")
    raiz2, iteraciones2, historial2, tiempo2 = metodo_newton_raphson(
        expresion, x, 2, tolerancia=1e-6)
    print(f"Raíz aproximada: {raiz2}")
    print(f"Iteraciones: {iteraciones2}")
    print(f"Tiempo de ejecución: {tiempo2:.6f} segundos\n")


if __name__ == "__main__":
    probar_metodo_newton_raphson()
