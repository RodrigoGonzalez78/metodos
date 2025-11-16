import math
from typing import List, Tuple, Callable, Optional


# ============================================================================
# MÓDULO DE LÓGICA: Método de Runge-Kutta de 2° Orden
# ============================================================================

def metodo_runge_kutta_2(f: Callable[[float, float], float], 
                         x0: float, y0: float, h: float, n: int) -> Tuple[List[float], List[float], List[dict]]:
    """
    Resuelve una EDO usando el Método de Runge-Kutta de 2° Orden.
    
    Fórmulas:
      k1 = h * f(x(n), y(n))
      k2 = h * f(x(n) + h, y(n) + k1)
      y(n+1) = y(n) + (1/2) * (k1 + k2)
    
    Args:
        f: Función f(x, y) que define dy/dx = f(x, y)
        x0: Valor inicial de x
        y0: Valor inicial de y (condición inicial)
        h: Tamaño del paso
        n: Número de pasos
    
    Returns:
        Tupla (x_values, y_values, detalles) donde detalles contiene k1, k2 para cada paso
    """
    x_values = [x0]
    y_values = [y0]
    detalles = []
    
    x_actual = x0
    y_actual = y0
    
    for i in range(n):
        # Paso 1: Calcular k1 en el punto actual
        k1 = h * f(x_actual, y_actual)
        
        # Paso 2: Calcular k2 en el punto siguiente usando k1
        k2 = h * f(x_actual + h, y_actual + k1)
        
        # Paso 3: Calcular y(n+1) usando promedio ponderado
        y_nuevo = y_actual + (k1 + k2) / 2
        x_nuevo = x_actual + h
        
        # Guardar valores
        x_values.append(x_nuevo)
        y_values.append(y_nuevo)
        
        # Guardar detalles del paso
        detalles.append({
            'paso': i,
            'x_n': x_actual,
            'y_n': y_actual,
            'k1': k1,
            'k2': k2,
            'x_n1': x_nuevo,
            'y_n1': y_nuevo
        })
        
        x_actual = x_nuevo
        y_actual = y_nuevo
    
    return x_values, y_values, detalles


def metodo_runge_kutta_2_punto_medio(f: Callable[[float, float], float], 
                                     x0: float, y0: float, h: float, n: int) -> Tuple[List[float], List[float], List[dict]]:
    """
    Variante del RK2: Método del Punto Medio.
    
    Fórmulas:
      k1 = h * f(x(n), y(n))
      k2 = h * f(x(n) + h/2, y(n) + k1/2)
      y(n+1) = y(n) + k2
    
    Args:
        f: Función f(x, y) que define dy/dx = f(x, y)
        x0: Valor inicial de x
        y0: Valor inicial de y
        h: Tamaño del paso
        n: Número de pasos
    
    Returns:
        Tupla (x_values, y_values, detalles)
    """
    x_values = [x0]
    y_values = [y0]
    detalles = []
    
    x_actual = x0
    y_actual = y0
    
    for i in range(n):
        # Paso 1: Calcular k1 en el punto actual
        k1 = h * f(x_actual, y_actual)
        
        # Paso 2: Calcular k2 en el punto medio
        k2 = h * f(x_actual + h/2, y_actual + k1/2)
        
        # Paso 3: Calcular y(n+1) usando k2
        y_nuevo = y_actual + k2
        x_nuevo = x_actual + h
        
        # Guardar valores
        x_values.append(x_nuevo)
        y_values.append(y_nuevo)
        
        # Guardar detalles del paso
        detalles.append({
            'paso': i,
            'x_n': x_actual,
            'y_n': y_actual,
            'k1': k1,
            'k2': k2,
            'x_medio': x_actual + h/2,
            'y_medio': y_actual + k1/2,
            'x_n1': x_nuevo,
            'y_n1': y_nuevo
        })
        
        x_actual = x_nuevo
        y_actual = y_nuevo
    
    return x_values, y_values, detalles


def calcular_error_local(y_aproximado: float, y_exacto: float) -> Tuple[float, float]:
    """
    Calcula el error absoluto y relativo.
    
    Args:
        y_aproximado: Valor calculado
        y_exacto: Valor exacto
    
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
    
    Args:
        expresion: String con la expresión
    
    Returns:
        Función evaluable f(x, y)
    """
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
# MÓDULO DE INTERFAZ: Terminal y entrada/salida
# ============================================================================

def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    print("\n" * 2)


def mostrar_titulo():
    """Muestra el título de la aplicación."""
    print("=" * 70)
    print(" " * 12 + "MÉTODO DE RUNGE-KUTTA DE 2° ORDEN")
    print(" " * 10 + "Resolución de Ecuaciones Diferenciales")
    print("=" * 70)
    print()
    print("Fórmula RK2 estándar:")
    print("  k1 = h * f(x(n), y(n))")
    print("  k2 = h * f(x(n) + h, y(n) + k1)")
    print("  y(n+1) = y(n) + (k1 + k2)/2")
    print()
    print("Método del Punto Medio:")
    print("  k1 = h * f(x(n), y(n))")
    print("  k2 = h * f(x(n) + h/2, y(n) + k1/2)")
    print("  y(n+1) = y(n) + k2")
    print("=" * 70)
    print()


def leer_entero(mensaje: str, minimo: Optional[int] = None, 
                maximo: Optional[int] = None) -> int:
    """Lee un entero con validación."""
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
    """Lee un número flotante con validación."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Ingrese un número válido")


def leer_si_no(mensaje: str) -> bool:
    """Lee una respuesta sí/no."""
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
    print("  -2*x*y")
    print()
    
    while True:
        expresion = input("f(x, y) = ").strip()
        if not expresion:
            print("Error: Debe ingresar una expresión")
            continue
        
        try:
            f = crear_funcion_desde_expresion(expresion)
            # Probar con valores de prueba
            test = f(1.0, 1.0)
            return f, expresion
        except Exception as e:
            print(f"Error en la expresión: {e}")
            print("Por favor, intente nuevamente")


def solicitar_condiciones_iniciales() -> Tuple[float, float]:
    """Solicita las condiciones iniciales."""
    print("\nCondiciones iniciales:")
    x0 = leer_float("x0 = ")
    y0 = leer_float("y0 = ")
    return x0, y0


def solicitar_parametros() -> Tuple[float, float, int]:
    """
    Solicita los parámetros del método.
    
    Returns:
        Tupla (h, xf, n)
    """
    print("\nParámetros del método:")
    
    opcion = leer_entero("¿Cómo desea especificar? (1: paso h, 2: número de pasos): ", 1, 2)
    
    if opcion == 1:
        h = leer_float("Tamaño del paso h = ")
        xf = leer_float("Valor final xf = ")
        n = 0  # Se calculará
        return h, xf, n
    else:
        xf = leer_float("Valor final xf = ")
        n = leer_entero("Número de pasos n = ", minimo=1)
        h = 0  # Se calculará
        return h, xf, n


def mostrar_tabla_resultados(titulo: str, x_values: List[float], 
                            y_values: List[float], 
                            y_exactos: Optional[List[float]] = None):
    """Muestra tabla con resultados."""
    print(f"\n{titulo}")
    print("=" * 90)
    
    if y_exactos:
        print(f"{'i':>3} {'x':>12} {'y (RK2)':>15} {'y (exacto)':>15} {'Error abs':>15} {'Error rel %':>12}")
        print("=" * 90)
        
        for i, (x, y_aprox, y_exact) in enumerate(zip(x_values, y_values, y_exactos)):
            error_abs, error_rel = calcular_error_local(y_aprox, y_exact)
            print(f"{i:>3} {x:>12.6f} {y_aprox:>15.10f} {y_exact:>15.10f} {error_abs:>15.8e} {error_rel:>12.6f}")
    else:
        print(f"{'i':>3} {'x':>15} {'y':>20}")
        print("=" * 90)
        
        for i, (x, y) in enumerate(zip(x_values, y_values)):
            print(f"{i:>3} {x:>15.6f} {y:>20.12f}")
    
    print("=" * 90)
    print()


def mostrar_pasos_detallados_rk2(detalles: List[dict], num_pasos: int = 3):
    """
    Muestra los primeros pasos del método RK2 en detalle.
    
    Args:
        detalles: Lista de diccionarios con detalles de cada paso
        num_pasos: Número de pasos a mostrar
    """
    print("\nPRIMEROS PASOS DETALLADOS - RUNGE-KUTTA 2° ORDEN")
    print("=" * 70)
    
    for i in range(min(num_pasos, len(detalles))):
        det = detalles[i]
        print(f"\nPaso {i}:")
        print(f"  x({i}) = {det['x_n']:.6f}")
        print(f"  y({i}) = {det['y_n']:.12f}")
        print()
        print(f"  k1 = h * f(x({i}), y({i}))")
        print(f"  k1 = {det['k1']:.12f}")
        print()
        print(f"  k2 = h * f(x({i}) + h, y({i}) + k1)")
        print(f"  k2 = h * f({det['x_n1']:.6f}, {det['y_n'] + det['k1']:.12f})")
        print(f"  k2 = {det['k2']:.12f}")
        print()
        print(f"  y({i+1}) = y({i}) + (k1 + k2)/2")
        print(f"  y({i+1}) = {det['y_n']:.12f} + ({det['k1']:.12f} + {det['k2']:.12f})/2")
        print(f"  y({i+1}) = {det['y_n']:.12f} + {(det['k1'] + det['k2'])/2:.12f}")
        print(f"  y({i+1}) = {det['y_n1']:.12f}")
        print("-" * 70)
    
    print()


def mostrar_pasos_detallados_punto_medio(detalles: List[dict], num_pasos: int = 3):
    """
    Muestra los primeros pasos del método del punto medio en detalle.
    
    Args:
        detalles: Lista de diccionarios con detalles de cada paso
        num_pasos: Número de pasos a mostrar
    """
    print("\nPRIMEROS PASOS DETALLADOS - MÉTODO DEL PUNTO MEDIO")
    print("=" * 70)
    
    for i in range(min(num_pasos, len(detalles))):
        det = detalles[i]
        print(f"\nPaso {i}:")
        print(f"  x({i}) = {det['x_n']:.6f}")
        print(f"  y({i}) = {det['y_n']:.12f}")
        print()
        print(f"  k1 = h * f(x({i}), y({i}))")
        print(f"  k1 = {det['k1']:.12f}")
        print()
        print(f"  Punto medio: x_medio = {det['x_medio']:.6f}, y_medio = {det['y_medio']:.12f}")
        print(f"  k2 = h * f(x({i}) + h/2, y({i}) + k1/2)")
        print(f"  k2 = h * f({det['x_medio']:.6f}, {det['y_medio']:.12f})")
        print(f"  k2 = {det['k2']:.12f}")
        print()
        print(f"  y({i+1}) = y({i}) + k2")
        print(f"  y({i+1}) = {det['y_n']:.12f} + {det['k2']:.12f}")
        print(f"  y({i+1}) = {det['y_n1']:.12f}")
        print("-" * 70)
    
    print()


def mostrar_comparacion(x_values: List[float], 
                       y_rk2: List[float], 
                       y_punto_medio: List[float]):
    """Muestra comparación entre ambas variantes."""
    print("\nCOMPARACIÓN DE VARIANTES RK2")
    print("=" * 90)
    print(f"{'i':>3} {'x':>12} {'RK2 Estándar':>20} {'Punto Medio':>20} {'Diferencia':>15}")
    print("=" * 90)
    
    for i, (x, y1, y2) in enumerate(zip(x_values, y_rk2, y_punto_medio)):
        diff = abs(y1 - y2)
        print(f"{i:>3} {x:>12.6f} {y1:>20.12f} {y2:>20.12f} {diff:>15.8e}")
    
    print("=" * 90)
    print()


def menu_principal() -> int:
    """Muestra el menú principal."""
    print("\nMENÚ PRINCIPAL")
    print("-" * 40)
    print("1. RK2 Estándar")
    print("2. RK2 Punto Medio")
    print("3. Comparar ambas variantes")
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
        
        # Calcular h o n según lo que falta
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
                # RK2 Estándar
                print("\n" + "=" * 70)
                print("MÉTODO DE RUNGE-KUTTA 2° ORDEN (ESTÁNDAR)")
                print("=" * 70)
                
                # Calcular
                x_values, y_values, detalles = metodo_runge_kutta_2(f, x0, y0, h, n)
                
                # Mostrar pasos detallados si se solicita
                if leer_si_no("\n¿Mostrar primeros pasos detallados? (s/n): "):
                    num_pasos = min(3, n)
                    mostrar_pasos_detallados_rk2(detalles, num_pasos)
                
                # Mostrar resultados
                mostrar_tabla_resultados("RESULTADOS - RK2 ESTÁNDAR", x_values, y_values)
                
            elif opcion == 2:
                # RK2 Punto Medio
                print("\n" + "=" * 70)
                print("MÉTODO DEL PUNTO MEDIO (RK2)")
                print("=" * 70)
                
                # Calcular
                x_values, y_values, detalles = metodo_runge_kutta_2_punto_medio(f, x0, y0, h, n)
                
                # Mostrar pasos detallados si se solicita
                if leer_si_no("\n¿Mostrar primeros pasos detallados? (s/n): "):
                    num_pasos = min(3, n)
                    mostrar_pasos_detallados_punto_medio(detalles, num_pasos)
                
                # Mostrar resultados
                mostrar_tabla_resultados("RESULTADOS - PUNTO MEDIO", x_values, y_values)
                
            else:  # opcion == 3
                # Comparar ambas variantes
                print("\n" + "=" * 70)
                print("COMPARACIÓN DE VARIANTES RK2")
                print("=" * 70)
                
                # Calcular con ambos métodos
                x_values, y_rk2, _ = metodo_runge_kutta_2(f, x0, y0, h, n)
                _, y_punto_medio, _ = metodo_runge_kutta_2_punto_medio(f, x0, y0, h, n)
                
                # Mostrar comparación
                mostrar_comparacion(x_values, y_rk2, y_punto_medio)
                
                # Análisis
                print("\nANÁLISIS:")
                diferencia_final = abs(y_rk2[-1] - y_punto_medio[-1])
                print(f"Valores finales en x = {xf:.6f}:")
                print(f"  RK2 Estándar: {y_rk2[-1]:.12f}")
                print(f"  Punto Medio:  {y_punto_medio[-1]:.12f}")
                print(f"  Diferencia:   {diferencia_final:.12e}")
                
        except Exception as e:
            print(f"\nError: {e}")
        
        input("\nPresione Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    main()