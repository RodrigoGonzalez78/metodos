import math
from typing import List, Tuple, Callable, Optional

# ============================================================================
# MÓDULO DE LÓGICA: Cálculos de diferencias finitas y derivadas
# ============================================================================

def validar_puntos(x_values: List[float], y_values: List[float]) -> float:
    """
    Valida que los puntos sean correctos y estén equiespaciados.
    
    Args:
        x_values: Lista de valores x
        y_values: Lista de valores y
    
    Returns:
        El espaciado h entre puntos
    
    Raises:
        ValueError: Si los datos no son válidos
    """
    if len(x_values) != len(y_values):
        raise ValueError("x_values e y_values deben tener la misma longitud")
    
    if len(x_values) < 2:
        raise ValueError("Se necesitan al menos 2 puntos")
    
    # Calcular el espaciado h
    h = x_values[1] - x_values[0]
    
    # Verificar que los puntos estén equiespaciados
    for i in range(1, len(x_values) - 1):
        diff = abs((x_values[i+1] - x_values[i]) - h)
        if diff > 1e-10:
            raise ValueError("Los puntos deben estar equiespaciados")
    
    return h


def calcular_diferencias_ascendentes(y_values: List[float]) -> List[List[float]]:
    """
    Calcula la tabla de diferencias finitas ascendentes (Δ).
    La diferencia ascendente es: Δf(x) = f(x+h) - f(x)
    
    Args:
        y_values: Lista de valores y
    
    Returns:
        Tabla de diferencias donde tabla[i][j] es la i-ésima diferencia
        del j-ésimo punto
    """
    n = len(y_values)
    tabla = [y_values.copy()]
    
    # Calcular diferencias sucesivas
    for orden in range(1, n):
        diferencias = []
        fila_anterior = tabla[orden - 1]
        
        for i in range(len(fila_anterior) - 1):
            # Δf(x) = f(x+h) - f(x)
            diff = fila_anterior[i + 1] - fila_anterior[i]
            diferencias.append(diff)
        
        if not diferencias:
            break
        
        tabla.append(diferencias)
    
    return tabla


def calcular_diferencias_descendentes(y_values: List[float]) -> List[List[float]]:
    """
    Calcula la tabla de diferencias finitas descendentes (∇).
    La diferencia descendente es: ∇f(x) = f(x) - f(x-h)
    
    Args:
        y_values: Lista de valores y
    
    Returns:
        Tabla de diferencias donde tabla[i][j] es la i-ésima diferencia
        del j-ésimo punto
    """
    n = len(y_values)
    tabla = [y_values.copy()]
    
    # Calcular diferencias sucesivas
    for orden in range(1, n):
        diferencias = []
        fila_anterior = tabla[orden - 1]
        
        for i in range(1, len(fila_anterior)):
            # ∇f(x) = f(x) - f(x-h)
            diff = fila_anterior[i] - fila_anterior[i - 1]
            diferencias.append(diff)
        
        if not diferencias:
            break
        
        tabla.append(diferencias)
    
    return tabla


def encontrar_indice(x_values: List[float], x: float) -> int:
    """
    Encuentra el índice del punto más cercano a x.
    
    Args:
        x_values: Lista de valores x
        x: Valor a buscar
    
    Returns:
        Índice del punto más cercano
    """
    idx = min(range(len(x_values)), 
              key=lambda i: abs(x_values[i] - x))
    return idx


def derivada_ascendente(x_values: List[float], y_values: List[float], 
                       x: float, orden: int = 1) -> float:
    """
    Calcula la derivada usando la fórmula de Newton-Gregory Ascendente.
    Útil para puntos al inicio del intervalo.
    
    Fórmulas:
    - Primera derivada: f'(x₀) ≈ (1/h)[Δf₀ - (1/2)Δ²f₀ + (1/3)Δ³f₀ - ...]
    - Segunda derivada: f''(x₀) ≈ (1/h²)[Δ²f₀ - Δ³f₀ + (11/12)Δ⁴f₀ - ...]
    
    Args:
        x_values: Lista de valores x
        y_values: Lista de valores y
        x: Punto donde calcular la derivada
        orden: Orden de la derivada (1 o 2)
    
    Returns:
        Valor de la derivada
    """
    if orden < 1 or orden > 2:
        raise ValueError("Solo se soportan derivadas de orden 1 y 2")
    
    # Validar y obtener espaciado
    h = validar_puntos(x_values, y_values)
    
    # Encontrar índice más cercano
    idx = encontrar_indice(x_values, x)
    
    # Calcular diferencias ascendentes
    tabla = calcular_diferencias_ascendentes(y_values)
    
    if orden == 1:
        # Primera derivada usando diferencias ascendentes
        # f'(x₀) ≈ (1/h)[Δf₀ - (1/2)Δ²f₀ + (1/3)Δ³f₀ - (1/4)Δ⁴f₀]
        derivada = 0.0
        signo = 1
        
        for k in range(1, min(len(tabla), 5)):  # Hasta 4to orden
            if idx < len(tabla[k]):
                coef = signo / k
                derivada += coef * tabla[k][idx]
                signo *= -1
        
        return derivada / h
    
    else:  # orden == 2
        # Segunda derivada usando diferencias ascendentes
        # f''(x₀) ≈ (1/h²)[Δ²f₀ - Δ³f₀ + (11/12)Δ⁴f₀]
        if len(tabla) < 3:
            raise ValueError("Se necesitan más puntos para la 2da derivada")
        
        derivada = tabla[2][idx]
        
        if len(tabla) > 3 and idx < len(tabla[3]):
            derivada -= tabla[3][idx]
        
        if len(tabla) > 4 and idx < len(tabla[4]):
            derivada += (11/12) * tabla[4][idx]
        
        return derivada / (h ** 2)


def derivada_descendente(x_values: List[float], y_values: List[float], 
                        x: float, orden: int = 1) -> float:
    """
    Calcula la derivada usando la fórmula de Newton-Gregory Descendente.
    Útil para puntos al final del intervalo.
    
    Fórmulas:
    - Primera derivada: f'(xₙ) ≈ (1/h)[∇fₙ + (1/2)∇²fₙ + (1/3)∇³fₙ + ...]
    - Segunda derivada: f''(xₙ) ≈ (1/h²)[∇²fₙ + ∇³fₙ + (11/12)∇⁴fₙ + ...]
    
    Args:
        x_values: Lista de valores x
        y_values: Lista de valores y
        x: Punto donde calcular la derivada
        orden: Orden de la derivada (1 o 2)
    
    Returns:
        Valor de la derivada
    """
    if orden < 1 or orden > 2:
        raise ValueError("Solo se soportan derivadas de orden 1 y 2")
    
    # Validar y obtener espaciado
    h = validar_puntos(x_values, y_values)
    
    # Encontrar índice más cercano
    idx = encontrar_indice(x_values, x)
    
    # Calcular diferencias descendentes
    tabla = calcular_diferencias_descendentes(y_values)
    
    if orden == 1:
        # Primera derivada usando diferencias descendentes
        # f'(xₙ) ≈ (1/h)[∇fₙ + (1/2)∇²fₙ + (1/3)∇³fₙ + (1/4)∇⁴fₙ]
        derivada = 0.0
        
        for k in range(1, min(len(tabla), 5)):  # Hasta 4to orden
            idx_ajustado = idx - (k - 1)
            if idx_ajustado >= 0 and idx_ajustado < len(tabla[k]):
                coef = 1.0 / k
                derivada += coef * tabla[k][idx_ajustado]
        
        return derivada / h
    
    else:  # orden == 2
        # Segunda derivada usando diferencias descendentes
        # f''(xₙ) ≈ (1/h²)[∇²fₙ + ∇³fₙ + (11/12)∇⁴fₙ]
        if len(tabla) < 3:
            raise ValueError("Se necesitan más puntos para la 2da derivada")
        
        derivada = 0.0
        
        for k in range(2, min(len(tabla), 5)):
            idx_ajustado = idx - (k - 1)
            if idx_ajustado >= 0 and idx_ajustado < len(tabla[k]):
                if k == 2:
                    derivada += tabla[k][idx_ajustado]
                elif k == 3:
                    derivada += tabla[k][idx_ajustado]
                elif k == 4:
                    derivada += (11/12) * tabla[k][idx_ajustado]
        
        return derivada / (h ** 2)


# ============================================================================
# MÓDULO DE INTERFAZ: Terminal y entrada/salida
# ============================================================================

def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    print("\n" * 2)


def mostrar_titulo():
    """Muestra el título de la aplicación."""
    print("=" * 70)
    print(" " * 10 + "DERIVACIÓN CON NEWTON-GREGORY")
    print(" " * 10 + "Diferencias Finitas Ascendentes y Descendentes")
    print("=" * 70)
    print()


def leer_entero(mensaje: str, minimo: Optional[int] = None, 
                maximo: Optional[int] = None) -> int:
    """
    Lee un entero del usuario con validación.
    
    Args:
        mensaje: Mensaje a mostrar
        minimo: Valor mínimo aceptable (opcional)
        maximo: Valor máximo aceptable (opcional)
    
    Returns:
        Entero ingresado por el usuario
    """
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"Error: El valor debe ser >= {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"Error: El valor debe ser <= {maximo}")
                continue
            return valor
        except ValueError:
            print("Error: Ingrese un número entero válido")


def leer_float(mensaje: str) -> float:
    """
    Lee un número flotante del usuario con validación.
    
    Args:
        mensaje: Mensaje a mostrar
    
    Returns:
        Número flotante ingresado por el usuario
    """
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Ingrese un número válido")


def solicitar_puntos() -> Tuple[List[float], List[float]]:
    """
    Solicita al usuario los puntos de datos manualmente.
    
    Returns:
        Tupla (x_values, y_values)
    """
    print("Ingrese los puntos de datos (deben estar equiespaciados)")
    print()
    
    n = leer_entero("¿Cuántos puntos desea ingresar? (mínimo 2): ", minimo=2)
    print()
    
    x_values = []
    y_values = []
    
    for i in range(n):
        print(f"Punto {i+1}:")
        x = leer_float(f"  x[{i}] = ")
        y = leer_float(f"  y[{i}] = ")
        x_values.append(x)
        y_values.append(y)
    
    return x_values, y_values


def solicitar_funcion_conocida() -> Tuple[List[float], List[float], Callable]:
    """
    Permite al usuario usar una función conocida para generar puntos.
    
    Returns:
        Tupla (x_values, y_values, funcion)
    """
    print("Funciones disponibles:")
    print("1. sen(x)")
    print("2. cos(x)")
    print("3. e^x")
    print("4. x^2")
    print("5. x^3")
    print()
    
    opcion = leer_entero("Seleccione una función: ", 1, 5)
    
    # Definir funciones y sus nombres
    if opcion == 1:
        func = math.sin
        nombre = "sen(x)"
    elif opcion == 2:
        func = math.cos
        nombre = "cos(x)"
    elif opcion == 3:
        func = math.exp
        nombre = "e^x"
    elif opcion == 4:
        func = lambda x: x**2
        nombre = "x^2"
    else:  # opcion == 5
        func = lambda x: x**3
        nombre = "x^3"
    
    print(f"\nFunción seleccionada: {nombre}")
    
    x_min = leer_float("Valor inicial de x: ")
    x_max = leer_float("Valor final de x: ")
    n = leer_entero("Número de puntos: ", minimo=2)
    
    # Generar puntos equiespaciados
    h = (x_max - x_min) / (n - 1)
    x_values = [x_min + i * h for i in range(n)]
    y_values = [func(x) for x in x_values]
    
    return x_values, y_values, func


def mostrar_tabla(titulo: str, x_values: List[float], y_values: List[float]):
    """
    Muestra una tabla de puntos en formato tabular.
    
    Args:
        titulo: Título de la tabla
        x_values: Valores de x
        y_values: Valores de y
    """
    print(f"\n{titulo}")
    print("-" * 40)
    print(f"{'i':>3} {'x':>12} {'y':>12}")
    print("-" * 40)
    
    for i, (x, y) in enumerate(zip(x_values, y_values)):
        print(f"{i:>3} {x:>12.6f} {y:>12.6f}")
    
    print("-" * 40)
    print()


def mostrar_diferencias(titulo: str, tabla: List[List[float]]):
    """
    Muestra la tabla de diferencias finitas.
    
    Args:
        titulo: Título de la tabla
        tabla: Tabla de diferencias
    """
    print(f"\n{titulo}")
    print("-" * 70)
    
    # Determinar símbolo (Δ para ascendente, ∇ para descendente)
    simbolo = "Δ" if "Ascendente" in titulo else "∇"
    
    # Encabezado
    encabezado = f"{simbolo}⁰f"
    for i in range(1, len(tabla)):
        encabezado += f" {simbolo}^{i}f".ljust(12)
    print(encabezado)
    print("-" * 70)
    
    # Datos
    max_filas = len(tabla[0])
    for i in range(max_filas):
        fila = ""
        for orden in range(len(tabla)):
            if i < len(tabla[orden]):
                fila += f"{tabla[orden][i]:>12.6f}"
            else:
                fila += " " * 12
        print(fila)
    
    print("-" * 70)
    print()


def mostrar_resultado(x: float, derivada: float, orden: int, 
                     metodo: str, valor_real: Optional[float] = None):
    """
    Muestra el resultado de la derivada calculada.
    
    Args:
        x: Punto de evaluación
        derivada: Valor de la derivada calculada
        orden: Orden de la derivada
        metodo: Método usado (Ascendente/Descendente)
        valor_real: Valor real de la derivada (opcional)
    """
    print("\n" + "=" * 70)
    print(f"RESULTADO - Método {metodo}")
    print("=" * 70)
    print(f"Punto de evaluación: x = {x}")
    print(f"Derivada de orden {orden}: f^({orden})(x) = {derivada:.8f}")
    
    if valor_real is not None:
        error = abs(derivada - valor_real)
        error_rel = (error / abs(valor_real) * 100) if valor_real != 0 else 0
        print(f"Valor real: {valor_real:.8f}")
        print(f"Error absoluto: {error:.8e}")
        print(f"Error relativo: {error_rel:.4f}%")
    
    print("=" * 70)
    print()


def menu_principal() -> int:
    """
    Muestra el menú principal y retorna la opción seleccionada.
    
    Returns:
        Opción seleccionada (1, 2 o 3)
    """
    print("\nMENÚ PRINCIPAL")
    print("-" * 40)
    print("1. Ingresar puntos manualmente")
    print("2. Usar función conocida")
    print("3. Salir")
    print("-" * 40)
    
    return leer_entero("Seleccione una opción: ", 1, 3)


def menu_derivacion() -> Tuple[int, int]:
    """
    Menú para seleccionar método y orden de derivación.
    
    Returns:
        Tupla (método, orden) donde método: 1=Ascendente, 2=Descendente
    """
    print("\nCONFIGURACIÓN DE DERIVACIÓN")
    print("-" * 40)
    print("Método:")
    print("1. Newton-Gregory Ascendente (mejor al inicio)")
    print("2. Newton-Gregory Descendente (mejor al final)")
    metodo = leer_entero("Seleccione método: ", 1, 2)
    
    orden = leer_entero("Orden de derivada (1 o 2): ", 1, 2)
    
    return metodo, orden


def calcular_derivada_real(func: Callable, x: float, orden: int) -> Optional[float]:
    """
    Calcula la derivada real de una función conocida.
    
    Args:
        func: Función original
        x: Punto de evaluación
        orden: Orden de la derivada
    
    Returns:
        Valor real de la derivada o None si no se puede calcular
    """
    if orden == 1:
        # Primera derivada de funciones conocidas
        if func == math.sin:
            return math.cos(x)
        elif func == math.cos:
            return -math.sin(x)
        elif func == math.exp:
            return math.exp(x)
        else:
            # Intentar identificar funciones lambda
            try:
                # Probar x^2
                if abs(func(2) - 4) < 1e-10 and abs(func(3) - 9) < 1e-10:
                    return 2 * x
                # Probar x^3
                elif abs(func(2) - 8) < 1e-10 and abs(func(3) - 27) < 1e-10:
                    return 3 * x ** 2
            except:
                pass
    
    elif orden == 2:
        # Segunda derivada de funciones conocidas
        if func == math.sin:
            return -math.sin(x)
        elif func == math.cos:
            return -math.cos(x)
        elif func == math.exp:
            return math.exp(x)
        else:
            try:
                # x^2 -> 2
                if abs(func(2) - 4) < 1e-10 and abs(func(3) - 9) < 1e-10:
                    return 2.0
                # x^3 -> 6x
                elif abs(func(2) - 8) < 1e-10 and abs(func(3) - 27) < 1e-10:
                    return 6 * x
            except:
                pass
    
    return None


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta la aplicación."""
    
    while True:
        limpiar_pantalla()
        mostrar_titulo()
        
        opcion = menu_principal()
        
        if opcion == 3:
            print("\n¡Gracias por usar el programa!")
            break
        
        # Obtener puntos
        func_real = None
        if opcion == 1:
            x_values, y_values = solicitar_puntos()
        else:
            x_values, y_values, func_real = solicitar_funcion_conocida()
        
        # Mostrar puntos ingresados
        mostrar_tabla("Puntos ingresados:", x_values, y_values)
        
        try:
            # Validar puntos
            h = validar_puntos(x_values, y_values)
            print(f"Espaciado h = {h:.6f}\n")
            
            # Calcular y mostrar diferencias ascendentes
            dif_asc = calcular_diferencias_ascendentes(y_values)
            mostrar_diferencias("Tabla de Diferencias Ascendentes:", dif_asc)
            
            # Calcular y mostrar diferencias descendentes
            dif_desc = calcular_diferencias_descendentes(y_values)
            mostrar_diferencias("Tabla de Diferencias Descendentes:", dif_desc)
            
            # Solicitar punto de evaluación y configuración
            x_eval = leer_float("\n¿En qué punto desea evaluar la derivada? x = ")
            metodo, orden = menu_derivacion()
            
            # Calcular derivada según el método seleccionado
            if metodo == 1:
                derivada = derivada_ascendente(x_values, y_values, x_eval, orden)
                metodo_nombre = "Newton-Gregory Ascendente"
            else:
                derivada = derivada_descendente(x_values, y_values, x_eval, orden)
                metodo_nombre = "Newton-Gregory Descendente"
            
            # Calcular valor real si se conoce la función
            valor_real = None
            if func_real is not None:
                valor_real = calcular_derivada_real(func_real, x_eval, orden)
            
            # Mostrar resultado
            mostrar_resultado(x_eval, derivada, orden, metodo_nombre, valor_real)
            
        except Exception as e:
            print(f"\nError: {e}")
        
        input("\nPresione Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    main()