from decimal import Decimal, getcontext
import math

def approx_e(N):
    """
    Aproxima e usando floats nativos de Python y muestra cada paso.
    """
    suma = 1.0
    term = 1.0
    print("\nSerie con float:")
    print(f"0: {suma}")  
    for k in range(1, N+1):
        term /= k
        suma += term
        print(f"{k}: {suma}")  
    return suma


def approx_e_decimal(N, prec=50):
    """
    Aproxima e usando Decimal para más precisión y muestra cada paso.
    """
    getcontext().prec = prec
    suma = Decimal(1)
    term = Decimal(1)
    print("\nSerie con Decimal:")
    print(f"0: {suma}")  
    for k in range(1, N+1):
        term = term / Decimal(k)
        suma = suma + term
        print(f"{k}: {suma}")  
    return suma


if __name__ == "__main__":
   
    N = int(input("Ingrese el número de aproximaciones (N): "))

    aprox_float = approx_e(N)
    aprox_dec = approx_e_decimal(N, prec=60)

    print("\nResultados finales:")
    print(f"N={N} | float ≈ {aprox_float:.15f}")
    print(f"N={N} | Decimal ≈ {aprox_dec}")
    print(f"Valor real de math.e: {math.e}")


    print("\nResultados:")
    print(f"N={N} | float ≈ {aprox_float:.15f}")
    print(f"N={N} | Decimal ≈ {aprox_dec}")
    print(f"\nValor real de math.e: {math.e}")

