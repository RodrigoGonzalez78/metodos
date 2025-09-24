

def metodo_regla_falsa(func, a, b, tolerancia=1e-6, max_iter=100):
    """
    Método de Interpolación Lineal (Regla Falsa)
    """
    if func(a) * func(b) > 0:
        raise ValueError("La función debe cambiar de signo en el intervalo [a,b]")
    
    historial = []
    
    print(f"{'Iter':>4} | {'a':>10} | {'b':>10} | {'c':>10} | {'f(c)':>12} | {'Error':>10}")
    print("-" * 70)
    
    c_anterior = a
    
    for i in range(max_iter):
        fa, fb = func(a), func(b)
        
        # Interpolación lineal
        c = a - fa * (b - a) / (fb - fa)
        fc = func(c)
        
        if i > 0:
            error = abs(c - c_anterior)
        else:
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
        
        c_anterior = c
    
    print(f"\nMáximo de iteraciones alcanzado")
    return c, max_iter, historial
