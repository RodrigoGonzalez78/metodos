import metodos.newton_raphson as mnr

def P(x):
    return 8*x + 0.3*x**2 - 0.0013*x**3 - 372

def P_derivada(x):
    return 8 + 0.6*x - 0.0039*x**2


if __name__ == "__main__":
    print("\n=== Raíz en el intervalo [24, 26] ===")
    raiz1, iter1, hist1 = mnr.metodo_newton_raphson(P, P_derivada, x0=25, tolerancia=1e-3)

    print("\n=== Raíz en el intervalo [250, 252] ===")
    raiz2, iter2, hist2 = mnr.metodo_newton_raphson(P, P_derivada, x0=251, tolerancia=1e-3)

    print(f"\n Puntos de equilibrio aproximados: {raiz1:.6f} y {raiz2:.6f}")
