import math
from typing import List, Tuple, Callable, Optional


# ============================================================================
# MÓDULO DE LÓGICA: Métodos de Euler
# ============================================================================

def metodo_euler(f: Callable[[float, float], float], 
                 x0: float, y0: float, h: float, n: int) -> Tuple[List[float], List[float]]:
    """
    Resuelve una EDO usando el Método de Euler.
    Fórmula: y(n+1) = y(n) + h * f(x(n), y(n))
    
    Args:
        f: Función f(x, y) que define dy/dx = f(x, y)
        x0: Valor inicial de x
        y0: Valor inicial de y (condición inicial)
        h: Tamaño del paso
        n: Número de pasos
    
    Returns:
        Tupla (x_values, y_values) con los puntos calculados
    """
    x_values = [x0]
    y_values = [y0]
    
    x_actual = x0
    y_actual = y0
    
    for i in range(n):
        # Calcular f(x, y) en el punto actual
        pendiente = f(x_actual, y_actual)
        
        # Aplicar fórmula de Euler
        y_nuevo = y_actual + h * pendiente
        x_nuevo = x_actual + h
        
        x_values.append(x_nuevo)
        y_values.append(y_nuevo)
        
        x_actual = x_nuevo
        y_actual = y_nuevo
    
    return x_values, y_values


def metodo_euler_modificado(f: Callable[[float, float], float], 
                            x0: float, y0: float, h: float, n: int) -> Tuple[List[float], List[float]]:
    """
    Resuelve una EDO usando el Método de Euler Modificado (Heun).
    Este método usa un predictor-corrector para mayor precisión.
    
    Fórmulas:
      k1 = f(x(n), y(n))
      k2 = f(x(n) + h, y(n) + h*k1)
      y(n+1) = y(n) + (h/2) * (k1 + k2)
    
    Args:
        f: Función f(x, y) que define dy/dx = f(x, y)
        x0: Valor inicial de x
        y0: Valor inicial de y (condición inicial)
        h: Tamaño del paso
        n: Número de pasos
    
    Returns:
        Tupla (x_values, y_values) con los puntos calculados
    """
    x_values = [x0]
    y_values = [y0]
    
    x_actual = x0
    y_actual = y0
    
    for i in range(n):
        # Paso 1: Calcular k1 (pendiente al inicio del intervalo)
        k1 = f(x_actual, y_actual)
        
        # Paso 2: Estimar y en el siguiente punto usando Euler
        y_predicho = y_actual + h * k1
        x_siguiente = x_actual + h
        
        # Paso 3: Calcular k2 (pendiente al final del intervalo)
        k2 = f(x_siguiente, y_predicho)
        
        # Paso 4: Usar promedio de pendientes para calcular y(n+1)
        y_nuevo = y_actual + (h / 2) * (k1 + k2)
        
        x_values.append(x_siguiente)
        y_values.append(y_nuevo)
        
        x_actual = x_siguiente
        y_actual = y_nuevo
    
    return x_values, y_values


def calcular_error_local(y_aproximado: float, y_exacto: float) -> Tuple[float, float]:
    """
    Calcula el error absoluto y relativo entre valor aproximado y exacto.
    
    Args:
        y_aproximado: Valor calculado por el método numérico
        y_exacto: Valor exacto (si se conoce)
    
    Returns:
        Tupla (error_absoluto, error_relativo_porcentaje)
    """
    error_abs = abs(y_aproximado - y_exacto)
    error_rel = (error_abs / abs(y_exacto) * 100) if y_exacto != 0 else 0
    return error_abs, error_rel


# ============================================================================
# FUNCIONES PARA EVALUACIÓN DE EXPRESIONES
# ============================================================================

def crear_funcion_desde_expresion(expresion: str) -> Callable[[float, float], float]:
    """
    Crea una función f(x, y) a partir de una expresión en texto.
    Permite usar: x, y, sin, cos, tan, exp, log, sqrt, pi, e
    
    Args:
        expresion: String con la expresión, ej: "x + y", "x**2 + y"
    
    Returns:
        Función evaluable f(x, y)
    """
    # Preparar namespace con funciones matemáticas
    namespace = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'ln': math.log,
        'sqrt': math.sqrt,
        'pi': math.pi,
        'e': math.e,
        'abs': abs,
        'pow': pow
    }
    
    def f(x: float, y: float) -> float:
        namespace['x'] = x
        namespace['y'] = y
        try:
            return eval(expresion, {"__builtins__": {}}, namespace)
        except Exception as e:
            raise ValueError(f"Error al evaluar expresión: {e}")
    
    return f


# ============================================================================
# MÓDULO DE INTERFAZ
# ============================================================================

def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    print("\n" * 2)


def mostrar_titulo():
    """Muestra el título de la aplicación."""
    print("=" * 70)
    print(" " * 18 + "MÉTODOS DE EULER")
    print(" " * 10 + "Resolución de Ecuaciones Diferenciales")
    print("=" * 70)
    print()
    print("Método de Euler: y(n+1) = y(n) + h*f(x(n), y(n))")
    print("Euler Modificado: y(n+1) = y(n) + (h/2)*(k1 + k2)")
    print("=" * 70)
    print()


def leer_entero(mensaje: str, minimo: Optional[int] = None, 
                maximo: Optional[int] = None) -> int:
    """
    Lee un entero del usuario con validación.
    
    Args:
        mensaje: Mensaje a mostrar
        minimo: Valor mínimo aceptable
        maximo: Valor máximo aceptable
    
    Returns:
        Entero validado
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
        Número flotante validado
    """
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Ingrese un número válido")


def leer_si_no(mensaje: str) -> bool:
    """
    Lee una respuesta sí/no del usuario.
    
    Args:
        mensaje: Mensaje a mostrar
    
    Returns:
        True si es sí, False si es no
    """
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            return True
        elif respuesta in ['n', 'no']:
            return False
        else:
            print("Error: Ingrese 's' para sí o 'n' para no")


def solicitar_edo() -> Tuple[Callable[[float, float], float], str]:
    """
    Solicita al usuario que ingrese la EDO a resolver.
    
    Returns:
        Tupla (funcion, expresion_string)
    """
    print("\nIngrese la ecuación diferencial dy/dx = f(x, y)")
    print("\nPuede usar:")
    print("  - Variables: x, y")
    print("  - Operaciones: +, -, *, /, ** (potencia)")
    print("  - Funciones: sin, cos, tan, exp, log, sqrt")
    print("  - Constantes: pi, e")
    print("\nEjemplos:")
    print("  x + y")
    print("  x**2 - y")
    print("  sin(x) + cos(y)")
    print("  x*y")
    print()
    
    while True:
        expresion = input("f(x, y) = ").strip()
        if not expresion:
            print("Error: Debe ingresar una expresión")
            continue
        
        try:
            # Intentar crear y probar la función
            f = crear_funcion_desde_expresion(expresion)
            # Probar con valores de prueba
            test = f(1.0, 1.0)
            return f, expresion
        except Exception as e:
            print(f"Error en la expresión: {e}")
            print("Por favor, intente nuevamente")


def solicitar_condiciones_iniciales() -> Tuple[float, float]:
    """
    Solicita las condiciones iniciales del problema.
    
    Returns:
        Tupla (x0, y0)
    """
    print("\nCondiciones iniciales:")
    x0 = leer_float("x0 = ")
    y0 = leer_float("y0 = ")
    return x0, y0


def solicitar_parametros() -> Tuple[float, float, int]:
    """
    Solicita los parámetros del método numérico.
    
    Returns:
        Tupla (h, xf, n) donde:
        - h: tamaño del paso
        - xf: valor final de x
        - n: número de pasos (calculado)
    """
    print("\nParámetros del método:")
    
    opcion = leer_entero("¿Cómo desea especificar? (1: paso h, 2: número de pasos): ", 1, 2)
    
    if opcion == 1:
        h = leer_float("Tamaño del paso h = ")
        xf = leer_float("Valor final xf = ")
        n = int((xf - 0) / h)  # Se calculará correctamente con x0
        return h, xf, n
    else:
        xf = leer_float("Valor final xf = ")
        n = leer_entero("Número de pasos n = ", minimo=1)
        h = 0  # Se calculará en main
        return h, xf, n


def mostrar_tabla_resultados(titulo: str, x_values: List[float], 
                            y_values: List[float], 
                            y_exactos: Optional[List[float]] = None):
    """
    Muestra una tabla con los resultados del método.
    
    Args:
        titulo: Título de la tabla
        x_values: Lista de valores x
        y_values: Lista de valores y calculados
        y_exactos: Lista de valores y exactos (opcional)
    """
    print(f"\n{titulo}")
    print("=" * 90)
    
    if y_exactos:
        print(f"{'i':>3} {'x':>12} {'y (aprox)':>15} {'y (exacto)':>15} {'Error abs':>15} {'Error rel %':>12}")
        print("=" * 90)
        
        for i, (x, y_aprox, y_exact) in enumerate(zip(x_values, y_values, y_exactos)):
            error_abs, error_rel = calcular_error_local(y_aprox, y_exact)
            print(f"{i:>3} {x:>12.6f} {y_aprox:>15.8f} {y_exact:>15.8f} {error_abs:>15.8e} {error_rel:>12.6f}")
    else:
        print(f"{'i':>3} {'x':>15} {'y':>20}")
        print("=" * 90)
        
        for i, (x, y) in enumerate(zip(x_values, y_values)):
            print(f"{i:>3} {x:>15.6f} {y:>20.10f}")
    
    print("=" * 90)
    print()


def mostrar_pasos_detallados_euler(f: Callable[[float, float], float], 
                                   x0: float, y0: float, h: float, pasos: int = 3):
    """
    Muestra los primeros pasos del método de Euler en detalle.
    
    Args:
        f: Función f(x, y)
        x0: Valor inicial de x
        y0: Valor inicial de y
        h: Tamaño del paso
        pasos: Número de pasos a mostrar
    """
    print("\nPRIMEROS PASOS DETALLADOS - MÉTODO DE EULER")
    print("-" * 70)
    
    x = x0
    y = y0
    
    for i in range(pasos):
        print(f"\nPaso {i}:")
        print(f"  x({i}) = {x:.6f}")
        print(f"  y({i}) = {y:.10f}")
        
        pendiente = f(x, y)
        print(f"  f(x({i}), y({i})) = {pendiente:.10f}")
        
        y_nuevo = y + h * pendiente
        x_nuevo = x + h
        
        print(f"  y({i+1}) = y({i}) + h * f(x({i}), y({i}))")
        print(f"  y({i+1}) = {y:.10f} + {h:.6f} * {pendiente:.10f}")
        print(f"  y({i+1}) = {y_nuevo:.10f}")
        
        x = x_nuevo
        y = y_nuevo
    
    print("-" * 70)
    print()


def mostrar_pasos_detallados_euler_modificado(f: Callable[[float, float], float], 
                                              x0: float, y0: float, h: float, pasos: int = 3):
    """
    Muestra los primeros pasos del método de Euler Modificado en detalle.
    
    Args:
        f: Función f(x, y)
        x0: Valor inicial de x
        y0: Valor inicial de y
        h: Tamaño del paso
        pasos: Número de pasos a mostrar
    """
    print("\nPRIMEROS PASOS DETALLADOS - MÉTODO DE EULER MODIFICADO")
    print("-" * 70)
    
    x = x0
    y = y0
    
    for i in range(pasos):
        print(f"\nPaso {i}:")
        print(f"  x({i}) = {x:.6f}")
        print(f"  y({i}) = {y:.10f}")
        
        k1 = f(x, y)
        print(f"  k1 = f(x({i}), y({i})) = {k1:.10f}")
        
        y_pred = y + h * k1
        x_sig = x + h
        print(f"  y_predicho = y({i}) + h*k1 = {y:.10f} + {h:.6f}*{k1:.10f} = {y_pred:.10f}")
        
        k2 = f(x_sig, y_pred)
        print(f"  k2 = f(x({i}) + h, y_predicho) = {k2:.10f}")
        
        y_nuevo = y + (h / 2) * (k1 + k2)
        print(f"  y({i+1}) = y({i}) + (h/2)*(k1 + k2)")
        print(f"  y({i+1}) = {y:.10f} + ({h:.6f}/2)*({k1:.10f} + {k2:.10f})")
        print(f"  y({i+1}) = {y:.10f} + {h/2:.6f}*{k1+k2:.10f}")
        print(f"  y({i+1}) = {y_nuevo:.10f}")
        
        x = x_sig
        y = y_nuevo
    
    print("-" * 70)
    print()


def mostrar_comparacion(x_values: List[float], 
                       y_euler: List[float], 
                       y_modificado: List[float],
                       y_exactos: Optional[List[float]] = None):
    """
    Muestra una comparación entre ambos métodos.
    
    Args:
        x_values: Lista de valores x
        y_euler: Resultados del método de Euler
        y_modificado: Resultados del método de Euler modificado
        y_exactos: Valores exactos (opcional)
    """
    print("\nCOMPARACIÓN DE MÉTODOS")
    print("=" * 100)
    
    if y_exactos:
        print(f"{'i':>3} {'x':>10} {'Euler':>15} {'Euler Mod':>15} {'Exacto':>15} {'Error E':>12} {'Error EM':>12}")
        print("=" * 100)
        
        for i, (x, ye, yem, yex) in enumerate(zip(x_values, y_euler, y_modificado, y_exactos)):
            err_e = abs(ye - yex)
            err_em = abs(yem - yex)
            print(f"{i:>3} {x:>10.6f} {ye:>15.8f} {yem:>15.8f} {yex:>15.8f} {err_e:>12.6e} {err_em:>12.6e}")
    else:
        print(f"{'i':>3} {'x':>12} {'Euler':>18} {'Euler Modificado':>18} {'Diferencia':>15}")
        print("=" * 100)
        
        for i, (x, ye, yem) in enumerate(zip(x_values, y_euler, y_modificado)):
            diff = abs(ye - yem)
            print(f"{i:>3} {x:>12.6f} {ye:>18.10f} {yem:>18.10f} {diff:>15.8e}")
    
    print("=" * 100)
    print()


def menu_principal() -> int:
    """
    Muestra el menú principal y retorna la opción seleccionada.
    
    Returns:
        Opción seleccionada
    """
    print("\nMENÚ PRINCIPAL")
    print("-" * 40)
    print("1. Método de Euler")
    print("2. Método de Euler Modificado")
    print("3. Comparar ambos métodos")
    print("4. Salir")
    print("-" * 40)
    
    return leer_entero("Seleccione una opción: ", 1, 4)


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta la aplicación."""
    
    while True:
        limpiar_pantalla()
        mostrar_titulo()
        
        opcion = menu_principal()
        
        if opcion == 4:
            print("\n¡Gracias por usar el programa!")
            break
        
        # Solicitar la EDO
        f, expresion = solicitar_edo()
        print(f"\nEcuación diferencial: dy/dx = {expresion}")
        
        # Solicitar condiciones iniciales
        x0, y0 = solicitar_condiciones_iniciales()
        
        # Solicitar parámetros
        h, xf, n = solicitar_parametros()
        
        # Calcular h si no fue especificado
        if h == 0:
            h = (xf - x0) / n
        else:
            n = int((xf - x0) / h)
        
        print(f"\nParámetros finales:")
        print(f"  x0 = {x0}, y0 = {y0}")
        print(f"  xf = {xf}")
        print(f"  h = {h:.6f}")
        print(f"  n = {n} pasos")
        
        try:
            if opcion == 1:
                # Método de Euler
                print("\n" + "=" * 70)
                print("MÉTODO DE EULER")
                print("=" * 70)
                
                # Mostrar pasos detallados
                if leer_si_no("\n¿Mostrar primeros pasos detallados? (s/n): "):
                    num_pasos = min(3, n)
                    mostrar_pasos_detallados_euler(f, x0, y0, h, num_pasos)
                
                # Calcular solución completa
                x_values, y_values = metodo_euler(f, x0, y0, h, n)
                
                # Mostrar resultados
                mostrar_tabla_resultados("RESULTADOS - MÉTODO DE EULER", x_values, y_values)
                
            elif opcion == 2:
                # Método de Euler Modificado
                print("\n" + "=" * 70)
                print("MÉTODO DE EULER MODIFICADO")
                print("=" * 70)
                
                # Mostrar pasos detallados
                if leer_si_no("\n¿Mostrar primeros pasos detallados? (s/n): "):
                    num_pasos = min(3, n)
                    mostrar_pasos_detallados_euler_modificado(f, x0, y0, h, num_pasos)
                
                # Calcular solución completa
                x_values, y_values = metodo_euler_modificado(f, x0, y0, h, n)
                
                # Mostrar resultados
                mostrar_tabla_resultados("RESULTADOS - MÉTODO DE EULER MODIFICADO", 
                                       x_values, y_values)
                
            else:  # opcion == 3
                # Comparar ambos métodos
                print("\n" + "=" * 70)
                print("COMPARACIÓN DE MÉTODOS")
                print("=" * 70)
                
                # Calcular con ambos métodos
                x_values, y_euler = metodo_euler(f, x0, y0, h, n)
                _, y_modificado = metodo_euler_modificado(f, x0, y0, h, n)
                
                # Mostrar comparación
                mostrar_comparacion(x_values, y_euler, y_modificado)
                
                # Análisis de convergencia
                print("\nANÁLISIS:")
                diferencia_final = abs(y_euler[-1] - y_modificado[-1])
                print(f"Diferencia en y({xf:.6f}):")
                print(f"  Euler: {y_euler[-1]:.10f}")
                print(f"  Euler Modificado: {y_modificado[-1]:.10f}")
                print(f"  Diferencia absoluta: {diferencia_final:.10e}")
                
        except Exception as e:
            print(f"\nError: {e}")
        
        input("\nPresione Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    main()