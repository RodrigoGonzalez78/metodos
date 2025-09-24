def metodo_punto_fijo(func_g, x0, tolerancia=1e-6, max_iter=100):
    """
    Método de Iteración de Punto Fijo
    
    Para resolver f(x) = 0, se reescribe como x = g(x)
    
    Parámetros:
    - func_g: función g(x) tal que x = g(x)
    - x0: estimación inicial
    - tolerancia: precisión deseada
    - max_iter: número máximo de iteraciones
    """
    historial = []
    x = x0
    
    print(f"{'Iter':>4} | {'x':>12} | {'g(x)':>12} | {'Error':>10}")
    print("-" * 50)
    
    for i in range(max_iter):
        gx = func_g(x)
        error = abs(gx - x)
        
        historial.append({
            'iteracion': i + 1,
            'x': x,
            'gx': gx,
            'error': error
        })
        
        print(f"{i+1:4} | {x:12.8f} | {gx:12.8f} | {error:10.8f}")
        
        if error < tolerancia:
            print(f"\nConvergencia alcanzada en {i+1} iteraciones")
            return gx, i + 1, historial
        
        x = gx
    
    print(f"\nMáximo de iteraciones alcanzado")
    return x, max_iter, historial