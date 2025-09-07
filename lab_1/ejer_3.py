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


# Ejemplo de uso
if __name__ == "__main__":
    # Probar con N = 200
    N = 200
    fib200 = fibonacci(N)
    print(f"Los {N} primeros números de Fibonacci son:")
    print(fib200)

    # Verificar longitud
    print(f"Cantidad generada: {len(fib200)}")
