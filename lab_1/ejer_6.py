import math
import time

def pi_leibniz(N):
    """
    Calcula pi usando la serie de Leibniz con N términos.
    """
    suma = 0.0
    for k in range(N):
        suma += ((-1)**k) / (2*k + 1)
    return 4 * suma


def buscar_terminos(decimales):
    """
    Encuentra cuántos términos de la serie son necesarios
    para que la aproximación de pi tenga 'decimales' correctos.
    """
    objetivo = round(math.pi, decimales)
    N = 1
    while True:
        aprox = pi_leibniz(N)
        if round(aprox, decimales) == objetivo:
            return N, aprox
        N += 1


if __name__ == "__main__":
    for dec in [3, 4, 5]:
        start = time.perf_counter()
        N, aprox = buscar_terminos(dec)
        elapsed = time.perf_counter() - start
        print(f"Decimales correctos: {dec}")
        print(f"  Términos necesarios: {N}")
        print(f"  Aproximación: {aprox}")
        print(f"  Tiempo: {elapsed:.4f} segundos\n")

    # Comparación con valor real
    print("Valor real math.pi =", math.pi)
