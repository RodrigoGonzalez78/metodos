
def metodo_newton_raphson(func, derivada, x0, tolerancia=1e-6, max_iter=100):
    """
    Método de Newton-Raphson
    
    Parámetros:
    - func: función a evaluar
    - derivada: derivada de la función
    - x0: estimación inicial
    - tolerancia: precisión deseada
    - max_iter: número máximo de iteraciones
    """
    historial = []
    x = x0
    
    print(f"{'Iter':>4} | {'x':>12} | {'f(x)':>12} | {'f\'(x)':>12} | {'Error':>10}")
    print("-" * 65)
    
    for i in range(max_iter):
        fx = func(x)
        fpx = derivada(x)
        
        if abs(fpx) < 1e-14:
            raise ValueError(f"Derivada muy pequeña en x = {x}. El método puede no converger.")
        
        x_nuevo = x - fx / fpx
        error = abs(x_nuevo - x)
        
        historial.append({
            'iteracion': i + 1,
            'x': x,
            'fx': fx,
            'fpx': fpx,
            'x_nuevo': x_nuevo,
            'error': error
        })
        
        print(f"{i+1:4} | {x:12.8f} | {fx:12.8f} | {fpx:12.8f} | {error:10.8f}")
        
        if error < tolerancia or abs(fx) < tolerancia:
            print(f"\nConvergencia alcanzada en {i+1} iteraciones")
            return x_nuevo, i + 1, historial
        
        x = x_nuevo
    
    print(f"\nMáximo de iteraciones alcanzado")
    return x, max_iter, historial
