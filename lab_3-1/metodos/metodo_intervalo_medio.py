
def metodo_biseccion(func, a, b, tolerancia=1e-6, max_iter=100):
    """
    Método de Bisección (Intervalo Medio)
    
    Parámetros:
    - func: función a evaluar
    - a, b: extremos del intervalo inicial
    - tolerancia: precisión deseada
    - max_iter: número máximo de iteraciones
    
    Retorna: (raiz, iteraciones, historial)
    """
    if func(a) * func(b) > 0:
        raise ValueError("La función debe cambiar de signo en el intervalo [a,b]")
    
    historial = []
    
    print(f"{'Iter':>4} | {'a':>10} | {'b':>10} | {'c':>10} | {'f(c)':>12} | {'|b-a|':>10}")
    print("-" * 70)
    
    for i in range(max_iter):
        c = (a + b) / 2  # punto medio
        fc = func(c)
        error = abs(b - a)
        
        historial.append({
            'iteracion': i + 1,
            'a': a,
            'b': b,
            'c': c,
            'fc': fc,
            'error': error
        })
        
        print(f"{i+1:4} | {a:10.6f} | {b:10.6f} | {c:10.6f} | {fc:12.8f} | {error:10.8f}")
        
        if error < tolerancia or abs(fc) < tolerancia:
            print(f"\nConvergencia alcanzada en {i+1} iteraciones")
            return c, i + 1, historial
        
        # Determinar nuevo intervalo
        if func(a) * fc < 0:
            b = c
        else:
            a = c
    
    print(f"\nMáximo de iteraciones alcanzado")
    return c, max_iter, historial
