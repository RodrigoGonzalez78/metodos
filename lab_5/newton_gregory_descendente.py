import numpy as np

# ============================================================================
# MÓDULO DE LÓGICA: Interpolación de Newton-Gregory Descendente
# ============================================================================

def calcular_diferencias_finitas_retrogradas(y):
    """
    Calcula la tabla completa de diferencias finitas retrógradas (hacia atrás).
    
    Parámetros:
    -----------
    y : array_like
        Vector de valores y = f(x)
    
    Retorna:
    --------
    numpy.ndarray
        Matriz donde tabla[i][j] contiene la j-ésima diferencia finita
        retrógrada terminando en el punto i
    """
    n = len(y)
    # Crear matriz para almacenar todas las diferencias
    tabla = np.zeros((n, n))
    
    # Primera columna: valores originales de y
    tabla[:, 0] = y
    
    # Calcular diferencias retrógradas de orden superior
    for j in range(1, n):  # j = orden de la diferencia
        for i in range(j, n):  # i = índice final (necesitamos i >= j)
            tabla[i, j] = tabla[i, j - 1] - tabla[i - 1, j - 1]
    
    return tabla


def factorial(n):
    """
    Calcula el factorial de un número entero no negativo.
    
    Parámetros:
    -----------
    n : int
        Número entero no negativo
    
    Retorna:
    --------
    int
        n! = n × (n-1) × (n-2) × ... × 2 × 1
    
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def coeficiente_binomial_generalizado(v, n):
    """
    Calcula el coeficiente binomial generalizado para interpolación descendente.
    
    
    Parámetros:
    -----------
    v : float
        Parámetro de interpolación v = (x - xₙ) / h
    n : int
        Orden del coeficiente
    
    Retorna:
    --------
    float
        Valor del coeficiente binomial generalizado
    
    """
    if n == 0:
        return 1
    
    # Calcular el producto v(v+1)(v+2)...(v+n-1)
    producto = 1
    for i in range(n):
        producto *= (v + i)
    
    # Dividir por n!
    return producto / factorial(n)


def interpolar_newton_gregory_descendente(x, y, x_interpolar):
    """
    Realiza interpolación usando la fórmula de Newton-Gregory Descendente.
    
    La fórmula de Newton-Gregory Descendente es:
    P(x) = yₙ + v∇yₙ + v(v+1)/2!·∇²yₙ + v(v+1)(v+2)/3!·∇³yₙ + ...
    
    donde:
    - v = (x - xₙ) / h
    - h = espaciamiento entre puntos (constante)
    - xₙ = último punto de los datos
    - ∇ⁿyₙ = diferencia finita retrógrada de orden n en el último punto
    
    Parámetros:
    -----------
    x : array_like
        Vector de valores x (deben estar equiespaciados)
    y : array_like
        Vector de valores y = f(x)
    x_interpolar : float
        Punto donde se desea calcular el valor interpolado
    
    Retorna:
    --------
    dict
        Diccionario con los siguientes campos:
        - 'valor': valor interpolado P(x)
        - 'tabla_diferencias': matriz de diferencias finitas retrógradas
        - 'v': parámetro de interpolación
        - 'h': espaciamiento entre puntos
        - 'terminos': lista de tuplas (coeficiente, diferencia, valor_termino)
    """
    n = len(x)
    
    # Calcular el espaciamiento h (asumiendo puntos equiespaciados)
    h = x[1] - x[0]
    
    # Calcular el parámetro v = (x - xₙ) / h
    # Este parámetro normaliza la posición de x_interpolar respecto a xₙ (último punto)
    # Nota: v será negativo si x_interpolar está antes del último punto
    v = (x_interpolar - x[-1]) / h
    
    # Calcular la tabla completa de diferencias finitas retrógradas
    tabla_diff = calcular_diferencias_finitas_retrogradas(y)
    
    # Inicializar el resultado con yₙ (último valor)
    resultado = y[-1]
    
    # Lista para almacenar información de cada término
    terminos = [(1.0, y[-1], y[-1])]  # (coeficiente, diferencia, valor)
    
    # Sumar los términos de la serie de Newton-Gregory Descendente
    for i in range(1, n):
        # Calcular el coeficiente binomial generalizado C(v, i)
        coef = coeficiente_binomial_generalizado(v, i)
        
        # Obtener la i-ésima diferencia finita retrógrada en el último punto
        diferencia = tabla_diff[n - 1, i]
        
        # Calcular el término: C(v, i) × ∇ⁱyₙ
        termino = coef * diferencia
        
        # Acumular en el resultado
        resultado += termino
        
        # Guardar información del término
        terminos.append((coef, diferencia, termino))
    
    # Retornar todos los resultados en un diccionario
    return {
        'valor': resultado,
        'tabla_diferencias': tabla_diff,
        'v': v,
        'h': h,
        'terminos': terminos,
        'xn': x[-1],
        'yn': y[-1]
    }


# ============================================================================
# MÓDULO DE INTERFAZ: Interacción con el usuario por terminal
# ============================================================================

def mostrar_encabezado():
    """Muestra el encabezado del programa."""
    print("=" * 70)
    print("INTERPOLACIÓN DE NEWTON-GREGORY DESCENDENTE".center(70))
    print("=" * 70)


def solicitar_puntos():
    """
    Solicita al usuario que ingrese los puntos de datos.
    
    Retorna:
    --------
    tuple
        (x, y) arrays de numpy con los puntos ingresados
    """
    # Solicitar cantidad de puntos
    while True:
        try:
            n = int(input("¿Cuántos puntos de datos tienes? "))
            if n < 2:
                print("⚠️  Necesitas al menos 2 puntos para interpolar.")
                continue
            break
        except ValueError:
            print("⚠️  Por favor ingresa un número entero válido.")
    
    x = []
    y = []
    
    print("\n" + "-" * 70)
    print("Ingresa los puntos (x, y):")
    print("NOTA: Los valores de x deben estar equiespaciados para mejor precisión")
    print("-" * 70)
    
    # Solicitar cada punto
    for i in range(n):
        while True:
            try:
                xi = float(input(f"x[{i}] = "))
                yi = float(input(f"y[{i}] = "))
                x.append(xi)
                y.append(yi)
                break
            except ValueError:
                print("⚠️  Por favor ingresa números válidos.")
    
    return np.array(x), np.array(y)


def verificar_espaciamiento(x):
    """
    Verifica si los puntos están equiespaciados.
    
    Parámetros:
    -----------
    x : array_like
        Vector de valores x
    
    Retorna:
    --------
    bool
        True si los puntos están equiespaciados, False en caso contrario
    """
    espaciamientos = np.diff(x)
    equiespaciado = np.allclose(espaciamientos, espaciamientos[0], rtol=1e-9)
    
    if not equiespaciado:
        print("\n" + "⚠️  " * 20)
        print("ADVERTENCIA: Los puntos NO están equiespaciados.")
        print("Espaciamientos detectados:", espaciamientos)
        print("La fórmula de Newton-Gregory funciona mejor con puntos equiespaciados.")
        print("Los resultados pueden ser menos precisos.")
        print("⚠️  " * 20 + "\n")
    
    return equiespaciado


def solicitar_punto_interpolar(x):
    """
    Solicita al usuario el punto donde desea interpolar.
    
    Parámetros:
    -----------
    x : array_like
        Vector de valores x (para verificar si es extrapolación)
    
    Retorna:
    --------
    float
        Valor de x donde se desea interpolar
    """
    while True:
        try:
            x_interpolar = float(input("¿Qué valor de x deseas interpolar? "))
            
            # Verificar si está fuera del rango (extrapolación)
            if x_interpolar < x[0] or x_interpolar > x[-1]:
                print("\n⚠️  ADVERTENCIA: Estás extrapolando (fuera del rango de datos).")
                print(f"Rango de datos: [{x[0]}, {x[-1]}]")
                print("Los resultados pueden ser menos precisos.\n")
                
                confirmar = input("¿Deseas continuar de todos modos? (s/n): ")
                if confirmar.lower() != 's':
                    continue
            
            # Sugerencia sobre qué método usar
            mitad = (x[0] + x[-1]) / 2
            if x_interpolar >= mitad:
                print("💡 Buena elección: El método descendente es ideal para puntos")
                print("   cercanos al final de la tabla.\n")
            else:
                print("💡 Nota: Para puntos cercanos al inicio, el método ascendente")
                print("   podría ser más preciso.\n")
            
            return x_interpolar
        except ValueError:
            print("⚠️  Por favor ingresa un número válido.")


def mostrar_tabla_diferencias(x, tabla_diff):
    """
    Muestra la tabla de diferencias finitas retrógradas de forma formateada.
    
    Parámetros:
    -----------
    x : array_like
        Vector de valores x
    tabla_diff : numpy.ndarray
        Matriz de diferencias finitas retrógradas
    """
    n = len(x)
    
    print("\n" + "=" * 70)
    print("TABLA DE DIFERENCIAS FINITAS RETRÓGRADAS".center(70))
    print("=" * 70)
    
    # Encabezados de columnas
    print(f"{'i':<5}{'x':<12}{'y':<14}", end='')
    for j in range(1, n):
        print(f"∇^{j}y{'':<12}", end='')
    print()
    print("-" * 70)
    
    # Filas de la tabla
    for i in range(n):
        print(f"{i:<5}{x[i]:<12.6f}{tabla_diff[i, 0]:<14.6f}", end='')
        # Solo mostramos las diferencias que existen (i >= j)
        for j in range(1, min(i + 1, n)):
            print(f"{tabla_diff[i, j]:<14.6f}", end='')
        print()


def mostrar_calculo_detallado(resultado, x_interpolar):
    """
    Muestra el cálculo paso a paso de la interpolación.
    
    Parámetros:
    -----------
    resultado : dict
        Diccionario con los resultados de la interpolación
    x_interpolar : float
        Punto donde se interpoló
    """
    print("\n" + "=" * 70)
    print("CÁLCULO DETALLADO DE LA INTERPOLACIÓN".center(70))
    print("=" * 70)
    
    # Mostrar parámetros básicos
    print(f"\nÚltimo punto: xₙ = {resultado['xn']}")
    print(f"Espaciamiento: h = {resultado['h']}")
    print(f"Parámetro:     v = (x - xₙ)/h = ({x_interpolar} - {resultado['xn']})/{resultado['h']}")
    print(f"                 = {resultado['v']:.8f}")
    
    if resultado['v'] < 0:
        print(f"\n💡 v < 0 indica que interpolamos hacia ATRÁS desde xₙ")
    else:
        print(f"\n💡 v > 0 indica extrapolación hacia ADELANTE desde xₙ")
    
    # Mostrar la fórmula
    print("\nFórmula de Newton-Gregory Descendente:")
    print("P(x) = yₙ + C(v,1)·∇yₙ + C(v,2)·∇²yₙ + C(v,3)·∇³yₙ + ...")
    print("donde C(v,n) = v(v+1)(v+2)...(v+n-1) / n!")
    
    # Mostrar cada término
    print("\n" + "-" * 70)
    print("Desarrollo término a término:")
    print("-" * 70)
    
    terminos = resultado['terminos']
    suma_acumulada = 0
    
    for i, (coef, diferencia, valor) in enumerate(terminos):
        if i == 0:
            print(f"Término 0: yₙ = {valor:.8f}")
            suma_acumulada = valor
        else:
            print(f"Término {i}: C(v,{i}) × ∇^{i}yₙ")
            print(f"          = {coef:.8f} × {diferencia:.8f}")
            print(f"          = {valor:.8f}")
            suma_acumulada += valor
        
        print(f"Suma acumulada: {suma_acumulada:.8f}")
        print()


def mostrar_resultado_final(resultado, x_interpolar):
    """
    Muestra el resultado final de la interpolación.
    
    Parámetros:
    -----------
    resultado : dict
        Diccionario con los resultados de la interpolación
    x_interpolar : float
        Punto donde se interpoló
    """
    print("=" * 70)
    print("RESULTADO FINAL".center(70))
    print("=" * 70)
    print(f"\nP({x_interpolar}) = {resultado['valor']:.10f}")
    print("\n" + "=" * 70)


def main():
   
    mostrar_encabezado()
    
    x, y = solicitar_puntos()
    
    verificar_espaciamiento(x)
    
    x_interpolar = solicitar_punto_interpolar(x)
    
    resultado = interpolar_newton_gregory_descendente(x, y, x_interpolar)
    
    mostrar_tabla_diferencias(x, resultado['tabla_diferencias'])
    mostrar_calculo_detallado(resultado, x_interpolar)
    mostrar_resultado_final(resultado, x_interpolar)



if __name__ == "__main__":
    main()