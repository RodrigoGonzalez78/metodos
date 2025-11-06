import numpy as np

def ingresar_matriz():
    n = int(input("Ingrese el tamaño de la matriz (n x n): "))
    A = np.zeros((n, n))
    print("Ingrese los elementos de la matriz fila por fila:")
    for i in range(n):
        fila = input(f"Fila {i+1} separada por espacios: ").strip().split()
        A[i] = [float(x) for x in fila]
    return A

def metodo_potencias(A, tol=1e-6, max_iter=100):
    n = A.shape[0]
    x = np.ones(n)  # vector inicial (1,1,...,1)
    lambda_old = 0.0

    for k in range(max_iter):
        y = np.dot(A, x)
        lambda_new = np.max(np.abs(y))  # estimación del autovalor
        x = y / lambda_new  # normalización del vector

        error = abs(lambda_new - lambda_old) / (abs(lambda_new) if lambda_new != 0 else 1) * 100
        print(f"Iteración {k+1}: λ = {lambda_new:.6f}, Error = {error:.4f}%")

        if error < tol:
            print("\nConvergencia alcanzada ✅")
            break

        lambda_old = lambda_new

    print("\nAutovalor máximo aproximado:", round(lambda_new, 6))
    print("Vector propio asociado (normalizado):")
    print(x)
    return lambda_new, x

def metodo_potencias_inversa(A, tol=1e-6, max_iter=100):
    print("\n--- Método de las Potencias Inverso (para mínimo autovalor) ---")
    try:
        A_inv = np.linalg.inv(A)
    except np.linalg.LinAlgError:
        print("❌ La matriz no es invertible.")
        return None, None

    lambda_max_inv, vector = metodo_potencias(A_inv, tol, max_iter)
    lambda_min = 1 / lambda_max_inv
    print("\nAutovalor mínimo aproximado:", round(lambda_min, 6))
    print("Vector propio asociado (normalizado):")
    print(vector)
    return lambda_min, vector

def main():
    print("=== MÉTODO DE LAS POTENCIAS ===")
    A = ingresar_matriz()

    print("\n--- Cálculo del autovalor máximo ---")
    metodo_potencias(A)

    opcion = input("\n¿Desea calcular también el mínimo autovalor? (s/n): ").lower()
    if opcion == "s":
        metodo_potencias_inversa(A)

if __name__ == "__main__":
    main()
