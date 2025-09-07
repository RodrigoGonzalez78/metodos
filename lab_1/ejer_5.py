from decimal import Decimal, getcontext
import math

def approx_e(N):
    """
    Aproxima e usando floats nativos de Python.
    """
    suma = 1.0
    term = 1.0
    for k in range(1, N+1):
        term /= k
        suma += term
    return suma


def approx_e_decimal(N, prec=50):
    """
    Aproxima e usando la librería Decimal para más precisión.
    """
    getcontext().prec = prec
    suma = Decimal(1)
    term = Decimal(1)
    for k in range(1, N+1):
        term = term / Decimal(k)
        suma = suma + term
    return suma


if __name__ == "__main__":
    # Pedir N por teclado
    N = int(input("Ingrese el número de aproximaciones (N): "))

    # Aproximaciones
    aprox_float = approx_e(N)
    aprox_dec = approx_e_decimal(N, prec=60)

    print("\nResultados:")
    print(f"N={N} | float ≈ {aprox_float:.15f}")
    print(f"N={N} | Decimal ≈ {aprox_dec}")
    print(f"\nValor real de math.e: {math.e}")

