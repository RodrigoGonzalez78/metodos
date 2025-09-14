import random

def sumar_vector(numeros):
    suma = 0
    for num in numeros:
        if isinstance(num, int) and 0 <= num <= 255:
            suma += num
        else:
            raise ValueError(f"Número inválido: {num}. Debe estar entre 0 y 255.")
    return suma


def sumar_numeros_aleatorios(N):
    numeros = [random.randint(0, 255) for _ in range(N)]
    return numeros, sumar_vector(numeros)


def sumar_ingresados(N):
    """
    Permite ingresar N números por teclado,
    los valida y los suma usando sumar_vector.
    """
    numeros = []
    for i in range(N):
        num = int(input(f"Ingrese el número {i+1}: "))
        if 0 <= num <= 255:
            numeros.append(num)
        else:
            raise ValueError(f"Número inválido: {num}. Debe estar entre 0 y 255.")
    return numeros, sumar_vector(numeros)


if __name__ == "__main__":
    numeros, resultado = sumar_numeros_aleatorios(20)
    print("Números generados:", numeros)
    print("Suma:", resultado)

    print("Suma de [10, 20, 30]:", sumar_vector([10, 20, 30]))

