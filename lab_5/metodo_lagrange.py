import numpy as np

# ============================================================================
# MÓDULO DE LÓGICA: Interpolación de Lagrange
# ============================================================================

def calcular_polinomio_base_lagrange(x, i, x_interpolar):
    """
    Calcula el i-ésimo polinomio base de Lagrange L_i(x).

    
    Parámetros:
    -----------
    x : array_like
        Vector de valores x conocidos
    i : int
        Índice del polinomio base a calcular
    x_interpolar : float
        Punto donde se evalúa el polinomio base
    
    Retorna:
    --------
    float
        Valor del polinomio base L_i evaluado en x_interpolar

    """
    n = len(x)
    numerador = 1.0
    denominador = 1.0
    
    # Calcular el producto para todos los j ≠ i
    for j in range(n):
        if j != i:
            numerador *= (x_interpolar - x[j])
            denominador *= (x[i] - x[j])
    
    return numerador / denominador


def interpolar_lagrange(x, y, x_interpolar):
    """
    Realiza interpolación usando el Método de Lagrange.

    Parámetros:
    -----------
    x : array_like
        Vector de valores x conocidos (NO necesitan estar equiespaciados)
    y : array_like
        Vector de valores y = f(x)
    x_interpolar : float
        Punto donde se desea calcular el valor interpolado
    
    Retorna:
    --------
    dict
        Diccionario con los siguientes campos:
        - 'valor': valor interpolado P(x)
        - 'polinomios_base': lista de valores L_i(x) para cada i
        - 'terminos': lista de tuplas (L_i, y_i, termino_i)
        - 'puntos': número de puntos usados
    
    Ejemplo:
    --------
    x = [1, 2, 4, 5]  # ¡No equiespaciados!
    y = [1, 4, 16, 25]
    resultado = interpolar_lagrange(x, y, 3)
    # resultado['valor'] ≈ 9.0
    """
    n = len(x)
    
    # Inicializar el resultado
    resultado = 0.0
    
    # Listas para almacenar información de cada término
    polinomios_base = []
    terminos = []
    
    # Calcular cada término de la suma
    for i in range(n):
        # Calcular el i-ésimo polinomio base de Lagrange
        L_i = calcular_polinomio_base_lagrange(x, i, x_interpolar)
        polinomios_base.append(L_i)
        
        # Calcular el término: y_i * L_i(x)
        termino = y[i] * L_i
        terminos.append((L_i, y[i], termino))
        
        # Acumular en el resultado
        resultado += termino
    
    # Retornar todos los resultados en un diccionario
    return {
        'valor': resultado,
        'polinomios_base': polinomios_base,
        'terminos': terminos,
        'puntos': n
    }


def evaluar_polinomio_lagrange_completo(x, y, x_valores):
    """
    Evalúa el polinomio de Lagrange en múltiples puntos.
    
    Útil para graficar o analizar el polinomio interpolante en un rango.
    
    Parámetros:
    -----------
    x : array_like
        Vector de valores x conocidos
    y : array_like
        Vector de valores y = f(x)
    x_valores : array_like
        Vector de puntos donde se desea evaluar el polinomio
    
    Retorna:
    --------
    numpy.ndarray
        Vector con los valores del polinomio evaluado en cada punto
    """
    y_valores = []
    
    for x_eval in x_valores:
        resultado = interpolar_lagrange(x, y, x_eval)
        y_valores.append(resultado['valor'])
    
    return np.array(y_valores)


def obtener_formula_polinomio_lagrange(x, y):
    """
    Genera una representación simbólica del polinomio de Lagrange.
    
    Parámetros:
    -----------
    x : array_like
        Vector de valores x conocidos
    y : array_like
        Vector de valores y = f(x)
    
    Retorna:
    --------
    list
        Lista de strings, cada uno representando un término L_i(x)
    """
    n = len(x)
    terminos_texto = []
    
    for i in range(n):
        # Construir el polinomio base L_i(x)
        numerador_partes = []
        denominador_partes = []
        
        for j in range(n):
            if j != i:
                numerador_partes.append(f"(x - {x[j]})")
                denominador_partes.append(f"({x[i]} - {x[j]})")
        
        numerador = " × ".join(numerador_partes)
        denominador = " × ".join(denominador_partes)
        
        # Construir el término completo
        termino = f"{y[i]} × [{numerador}] / [{denominador}]"
        terminos_texto.append(termino)
    
    return terminos_texto


# ============================================================================
# MÓDULO DE INTERFAZ: Interacción con el usuario por terminal
# ============================================================================

def mostrar_encabezado():
    """Muestra el encabezado del programa."""
    print("=" * 70)
    print("INTERPOLACIÓN DE LAGRANGE".center(70))
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
            if n > 10:
                print("⚠️  Con más de 10 puntos, el método puede volverse inestable.")
                confirmar = input("¿Deseas continuar? (s/n): ")
                if confirmar.lower() != 's':
                    continue
            break
        except ValueError:
            print("⚠️  Por favor ingresa un número entero válido.")
    
    x = []
    y = []
    
    print("\n" + "-" * 70)
    print("Ingresa los puntos (x, y):")
    print("NOTA: Los puntos NO necesitan estar equiespaciados")
    print("-" * 70)
    
    # Solicitar cada punto
    for i in range(n):
        while True:
            try:
                xi = float(input(f"x[{i}] = "))
                
                # Verificar que no haya valores duplicados de x
                if xi in x:
                    print("⚠️  Ya ingresaste ese valor de x. Debe ser único.")
                    continue
                
                yi = float(input(f"y[{i}] = "))
                x.append(xi)
                y.append(yi)
                break
            except ValueError:
                print("⚠️  Por favor ingresa números válidos.")
    
    return np.array(x), np.array(y)


def verificar_distribucion_puntos(x):
    """
    Analiza la distribución de los puntos y muestra información útil.
    
    Parámetros:
    -----------
    x : array_like
        Vector de valores x
    """
    # Ordenar para análisis
    x_sorted = np.sort(x)
    espaciamientos = np.diff(x_sorted)
    
    print("\n" + "=" * 70)
    print("ANÁLISIS DE LA DISTRIBUCIÓN DE PUNTOS".center(70))
    print("=" * 70)
    
    print(f"\nRango de datos: [{x_sorted[0]:.4f}, {x_sorted[-1]:.4f}]")
    print(f"Espaciamiento mínimo: {np.min(espaciamientos):.4f}")
    print(f"Espaciamiento máximo: {np.max(espaciamientos):.4f}")
    print(f"Espaciamiento promedio: {np.mean(espaciamientos):.4f}")
    
    # Verificar si están equiespaciados
    if np.allclose(espaciamientos, espaciamientos[0], rtol=1e-6):
        print("\n💡 Los puntos están equiespaciados.")
        print("   (Los métodos de Newton-Gregory también serían apropiados)")
    else:
        print("\n💡 Los puntos NO están equiespaciados.")
        print("   (El método de Lagrange es ideal para este caso)")


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
    x_min = np.min(x)
    x_max = np.max(x)
    
    while True:
        try:
            x_interpolar = float(input("\n¿Qué valor de x deseas interpolar? "))
            
            # Verificar si está fuera del rango (extrapolación)
            if x_interpolar < x_min or x_interpolar > x_max:
                print("\n⚠️  ADVERTENCIA: Estás extrapolando (fuera del rango de datos).")
                print(f"Rango de datos: [{x_min}, {x_max}]")
                print("La extrapolación con Lagrange puede ser muy imprecisa.\n")
                
                confirmar = input("¿Deseas continuar de todos modos? (s/n): ")
                if confirmar.lower() != 's':
                    continue
            
            return x_interpolar
        except ValueError:
            print("⚠️  Por favor ingresa un número válido.")


def mostrar_puntos_datos(x, y):
    """
    Muestra los puntos de datos en formato de tabla.
    
    Parámetros:
    -----------
    x : array_like
        Vector de valores x
    y : array_like
        Vector de valores y
    """
    print("\n" + "=" * 70)
    print("PUNTOS DE DATOS".center(70))
    print("=" * 70)
    
    print(f"\n{'i':<5}{'x':<20}{'y':<20}")
    print("-" * 70)
    
    for i in range(len(x)):
        print(f"{i:<5}{x[i]:<20.8f}{y[i]:<20.8f}")


def mostrar_polinomios_base(x, resultado, x_interpolar):
    """
    Muestra los polinomios base de Lagrange y sus valores.
    
    Parámetros:
    -----------
    x : array_like
        Vector de valores x
    resultado : dict
        Diccionario con los resultados de la interpolación
    x_interpolar : float
        Punto donde se interpoló
    """
    print("\n" + "=" * 70)
    print("POLINOMIOS BASE DE LAGRANGE".center(70))
    print("=" * 70)
    
    n = len(x)
    polinomios_texto = obtener_formula_polinomio_lagrange(x, np.ones(n))
    
    for i in range(n):
        print(f"\n--- Polinomio L_{i}(x) ---")
        
        # Mostrar fórmula
        numerador_partes = []
        denominador_partes = []
        
        for j in range(n):
            if j != i:
                numerador_partes.append(f"(x - {x[j]})")
                denominador_valor = x[i] - x[j]
                denominador_partes.append(f"{denominador_valor:.4f}")
        
        numerador = " × ".join(numerador_partes)
        denominador = " × ".join(denominador_partes)
        
        print(f"L_{i}(x) = [{numerador}] / [{denominador}]")
        print(f"L_{i}({x_interpolar}) = {resultado['polinomios_base'][i]:.10f}")


def mostrar_calculo_detallado(x, y, resultado, x_interpolar):
    """
    Muestra el cálculo paso a paso de la interpolación.
    
    Parámetros:
    -----------
    x : array_like
        Vector de valores x
    y : array_like
        Vector de valores y
    resultado : dict
        Diccionario con los resultados de la interpolación
    x_interpolar : float
        Punto donde se interpoló
    """
    print("\n" + "=" * 70)
    print("CÁLCULO DETALLADO DE LA INTERPOLACIÓN".center(70))
    print("=" * 70)
    
    print("\nFórmula de Lagrange:")
    print("P(x) = Σ y_i × L_i(x)")
    print(f"     = y₀×L₀({x_interpolar}) + y₁×L₁({x_interpolar}) + ... + yₙ×Lₙ({x_interpolar})")
    
    # Mostrar cada término
    print("\n" + "-" * 70)
    print("Desarrollo término a término:")
    print("-" * 70)
    
    suma_acumulada = 0
    
    for i, (L_i, y_i, termino) in enumerate(resultado['terminos']):
        print(f"\nTérmino {i}:")
        print(f"  y_{i} = {y_i:.8f}")
        print(f"  L_{i}({x_interpolar}) = {L_i:.10f}")
        print(f"  y_{i} × L_{i}({x_interpolar}) = {termino:.10f}")
        suma_acumulada += termino
        print(f"  Suma acumulada = {suma_acumulada:.10f}")


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
    print("\n" + "=" * 70)
    print("RESULTADO FINAL".center(70))
    print("=" * 70)
    print(f"\nP({x_interpolar}) = {resultado['valor']:.10f}")
    print(f"\nPolinomio de grado: {resultado['puntos'] - 1}")
    print("\n" + "=" * 70)


def main():
   
    mostrar_encabezado()
    
    x, y = solicitar_puntos()
    
    mostrar_puntos_datos(x, y)
    
    verificar_distribucion_puntos(x)
    
    x_interpolar = solicitar_punto_interpolar(x)
    
    resultado = interpolar_lagrange(x, y, x_interpolar)
    
    mostrar_polinomios_base(x, resultado, x_interpolar)
    mostrar_calculo_detallado(x, y, resultado, x_interpolar)
    mostrar_resultado_final(resultado, x_interpolar)


if __name__ == "__main__":
    main()