import time

def metodo_interpolacion_lineal(func, a, b, tolerancia=1e-6, max_iter=100):
    """
    Método de Interpolación Lineal (Regla Falsa)
    """
    tiempo_inicio = time.time()
    
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
            tiempo_total = time.time() - tiempo_inicio  # Calcular tiempo total
            print(f"\nConvergencia alcanzada en {i+1} iteraciones")
            print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
            return c, i + 1, historial
        
        # Determinar nuevo intervalo
        if func(a) * fc < 0:
            b = c
        else:
            a = c
        
        c_anterior = c
    
    tiempo_total = time.time() - tiempo_inicio  # Calcular tiempo total
    print(f"\nMáximo de iteraciones alcanzado")
    print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
    return c, max_iter, historial


def seleccionar_x0_fourier(func, a, b):
    """
    Selecciona x0 basado en la condición de Fourier (menor valor absoluto de f(x))
    
    Parámetros:
    - func: función a evaluar
    - a: extremo izquierdo del intervalo
    - b: extremo derecho del intervalo
    
    Retorna:
    - x0: punto inicial seleccionado
    - fa, fb: valores de la función en los extremos
    """
    try:
        fa = func(a)
        fb = func(b)
        
        print(f"  f({a:.2f}) = {fa:.6f}")
        print(f"  f({b:.2f}) = {fb:.6f}")
        
        # Verificar condición de Bolzano
        if fa * fb > 0:
            print(f"  ⚠ No se cumple la condición de Bolzano en [{a:.2f}, {b:.2f}]")
            return None, fa, fb
        
        # Seleccionar x0 según condición de Fourier
        if abs(fa) < abs(fb):
            x0 = a
            print(f"  ✓ Seleccionado x0 = {x0:.2f} (menor |f(x)|)")
        else:
            x0 = b
            print(f"  ✓ Seleccionado x0 = {x0:.2f} (menor |f(x)|)")
        
        return x0, fa, fb
        
    except Exception as e:
        print(f"  ⚠ Error al evaluar la función: {e}")
        return None, None, None


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
    tiempo_inicio = time.time()  # Iniciar medición de tiempo
    
    historial = []
    x = x0
    
    for i in range(max_iter):
        fx = func(x)
        fpx = derivada(x)
        
        if abs(fpx) < 1e-14:
            tiempo_total = time.time() - tiempo_inicio
            print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
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
        

        if error < tolerancia or abs(fx) < tolerancia:
            tiempo_total = time.time() - tiempo_inicio  # Calcular tiempo total
            print(f"\nConvergencia alcanzada en {i+1} iteraciones")
            print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
            return x_nuevo, i + 1, historial
        
        x = x_nuevo
    
    tiempo_total = time.time() - tiempo_inicio  # Calcular tiempo total
    print(f"\nMáximo de iteraciones alcanzado")
    print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
    return x, max_iter, historial


def aceleracion_aitken(x0, x1, x2):
    """
    Aplica la aceleración de Aitken para mejorar la convergencia
    
    Fórmula: x_acelerado = x0 - (x1 - x0)² / (x2 - 2*x1 + x0)
    """
    denominador = x2 - 2*x1 + x0
    
    # Evitar división por cero
    if abs(denominador) < 1e-14:  
        return x2
    
    return x0 - (x1 - x0)**2 / denominador


def metodo_punto_fijo(func_g, x0, tolerancia=1e-6, max_iter=100, usar_aitken=False):
    """
    Método de Iteración de Punto Fijo con opción de Aceleración de Aitken
    
    Para resolver f(x) = 0, se reescribe como x = g(x)
    
    Parámetros:
    - func_g: función g(x) tal que x = g(x)
    - x0: estimación inicial
    - tolerancia: precisión deseada
    - max_iter: número máximo de iteraciones
    - usar_aitken: True para aplicar aceleración de Aitken
    """
    tiempo_inicio = time.time()  # Iniciar medición de tiempo
    
    historial = []
    x = x0
    
    # Encabezado de la tabla
    if usar_aitken:
        print(f"{'Iter':>4} | {'x':>12} | {'g(x)':>12} | {'x_Aitken':>12} | {'Error':>10}")
        print("-" * 65)
    else:
        print(f"{'Iter':>4} | {'x':>12} | {'g(x)':>12} | {'Error':>10}")
        print("-" * 50)
    
    # Variables para Aitken (necesitamos 3 puntos consecutivos)
    x_prev2, x_prev1 = None, None
    
    for i in range(max_iter):
        gx = func_g(x)
        
        # Aplicar Aitken si está habilitado y tenemos suficientes puntos
        x_aitken = None
        if usar_aitken and i >= 2:
            x_aitken = aceleracion_aitken(x_prev2, x_prev1, x)
            error = abs(x_aitken - x)
            x_siguiente = x_aitken
        else:
            error = abs(gx - x)
            x_siguiente = gx
        
        # Guardar en historial
        historial.append({
            'iteracion': i + 1,
            'x': x,
            'gx': gx,
            'x_aitken': x_aitken,
            'error': error,
            'x_siguiente': x_siguiente
        })
        
        # Mostrar resultados
        if usar_aitken and x_aitken is not None:
            print(f"{i+1:4} | {x:12.8f} | {gx:12.8f} | {x_aitken:12.8f} | {error:10.8f}")
        elif usar_aitken:
            print(f"{i+1:4} | {x:12.8f} | {gx:12.8f} | {'N/A':>12} | {error:10.8f}")
        else:
            print(f"{i+1:4} | {x:12.8f} | {gx:12.8f} | {error:10.8f}")
        
        # Verificar convergencia
        if error < tolerancia:
            tiempo_total = time.time() - tiempo_inicio  # Calcular tiempo total
            print(f"\nConvergencia alcanzada en {i+1} iteraciones")
            metodo = "Punto Fijo con Aitken" if usar_aitken else "Punto Fijo"
            print(f"Método usado: {metodo}")
            print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
            return x_siguiente, i + 1, historial
        
        # Actualizar variables para siguiente iteración
        x_prev2, x_prev1 = x_prev1, x
        x = x_siguiente
    
    tiempo_total = time.time() - tiempo_inicio  # Calcular tiempo total
    print(f"\nMáximo de iteraciones alcanzado")
    metodo = "Punto Fijo con Aitken" if usar_aitken else "Punto Fijo"
    print(f"Método usado: {metodo}")
    print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
    return x, max_iter, historial


def metodo_intervalo_medio(func, a, b, tolerancia=1e-6, max_iter=100):
    """
    Método de Bisección (Intervalo Medio)
    
    Parámetros:
    - func: función a evaluar
    - a, b: extremos del intervalo inicial
    - tolerancia: precisión deseada
    - max_iter: número máximo de iteraciones
    
    Retorna: (raiz, iteraciones, historial)
    """
    tiempo_inicio = time.time()  # Iniciar medición de tiempo
    
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
            tiempo_total = time.time() - tiempo_inicio  # Calcular tiempo total
            print(f"\nConvergencia alcanzada en {i+1} iteraciones")
            print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
            return c, i + 1, historial
        
        # Determinar nuevo intervalo
        if func(a) * fc < 0:
            b = c
        else:
            a = c
    
    tiempo_total = time.time() - tiempo_inicio  # Calcular tiempo total
    print(f"\nMáximo de iteraciones alcanzado")
    print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
    return c, max_iter, historial