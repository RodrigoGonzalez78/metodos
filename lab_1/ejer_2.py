import random

def sumar_pares_vector(numeros):
    """
    Suma solo los números pares de un vector validando que sean enteros positivos
    en el rango 0 a 255.
    """
    suma = 0
    for num in numeros:
        if isinstance(num, int) and 0 <= num <= 255:
            if num % 2 == 0:  
                suma += num
        else:
            raise ValueError(f"Número inválido: {num}. Debe estar entre 0 y 255.")
    return suma


def sumar_pares_aleatorios(N=200):
    """
    Genera N números aleatorios en el rango 0-255,
    los suma usando sumar_pares_vector y devuelve el resultado.
    """
    numeros = [random.randint(0, 255) for _ in range(N)]
    return numeros, sumar_pares_vector(numeros)


def sumar_pares_ingresados(N=200):
    """
    Permite ingresar N números por teclado,
    los valida y los suma usando sumar_pares_vector.
    """
    numeros = []
    for i in range(N):
        num = int(input(f"Ingrese el número {i+1}: "))
        if 0 <= num <= 255:
            numeros.append(num)
        else:
            raise ValueError(f"Número inválido: {num}. Debe estar entre 0 y 255.")
    return numeros, sumar_pares_vector(numeros)


if __name__ == "__main__":
    numeros, resultado = sumar_pares_aleatorios(200)
    print("Números generados:", numeros)
    print("\nSuma de pares:", resultado)

