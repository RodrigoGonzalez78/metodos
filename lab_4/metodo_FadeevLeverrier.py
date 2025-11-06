import numpy as np

def ingresar_matriz():
    n = int(input("Ingrese el tamaño de la matriz (n x n): "))
    A = np.zeros((n, n))
    print("Ingrese los elementos de la matriz fila por fila:")
    for i in range(n):
        fila = input(f"Fila {i+1} separada por espacios: ").strip().split()
        A[i] = [float(x) for x in fila]
    return A

def metodo_faddeev_leverrier(A):
    n = A.shape[0]
    I = np.eye(n)
    B_prev = A.copy()
    b = []
    print("\n--- Método de Faddeev–Leverrier ---")

    # Primer coeficiente
    b1 = np.trace(B_prev)
    b.append(b1)
    print(f"B1 = A\n{A}")
    print(f"b1 = tr(B1) = {b1:.6f}")

    # Iteraciones
    for k in range(2, n + 1):
        Bk = np.dot(A, B_prev - b[-1] * I)
        bk = np.trace(Bk) / k
        b.append(bk)
        print(f"\nIteración {k}:")
        print(f"B{k} = A * (B{k-1} - b{k-1}*I)\n{Bk}")
        print(f"b{k} = tr(B{k})/{k} = {bk:.6f}")
        B_prev = Bk

    # Polinomio característico
    coef = [1]  # coeficiente de λ^n
    for i in range(n):
        coef.append(-b[i])
    print("\nCoeficientes del polinomio característico:")
    print(coef)

    print("\nPolinomio característico:")
    terms = [f"λ^{n - i}" if i == 0 else f"λ^{n - i}" for i in range(n)]
    poly = " + ".join([f"{coef[i]}*λ^{n-i}" if i < n else f"{coef[i]}" for i in range(n+1)])
    print(poly.replace("+ -", "- "))

    return coef

def main():
    print("=== MÉTODO DE FADDEEV–LEVERRIER ===")
    A = ingresar_matriz()
    coef = metodo_faddeev_leverrier(A)

    # Cálculo de autovalores con numpy para verificar
    autovalores, _ = np.linalg.eig(A)
    print("\nAutovalores calculados con numpy (verificación):")
    print(np.round(autovalores, 6))

if __name__ == "__main__":
    main()
