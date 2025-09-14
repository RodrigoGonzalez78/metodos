def fibonacci(n):
    """
    Genera los n primeros números de la sucesión de Fibonacci.
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib = [0, 1]
    for _ in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib


if __name__ == "__main__":
    try:
        N = int(input("Ingrese la cantidad de términos de Fibonacci a generar: "))
        fib_n = fibonacci(N)
        print(f"Los {N} primeros números de Fibonacci son:")
        print(fib_n)

        print(f"Cantidad generada: {len(fib_n)}")
    except ValueError:
        print("Por favor, ingrese un número entero válido.")
