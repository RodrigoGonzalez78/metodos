import math
from typing import List, Tuple, Callable, Optional


# ============================================================================
# MÓDULO DE LÓGICA: Método de Milne
# ============================================================================

def metodo_runge_kutta_4_inicial(f: Callable[[float, float], float], 
                                 x0: float, y0: float, h: float, n: int = 3) -> Tuple[List[float], List[float]]:
    """
    Calcula valores iniciales usando Runge-Kutta 4° orden.
    Se usa para obtener los primeros puntos necesarios para Milne.
    
    Args:
        f: Función f(x, y)
        x0: Valor inicial de x
        y0: Valor inicial de y
        h: Tamaño del paso
        n: Número de pasos adicionales (default 3)
    
    Returns:
        Tupla (x_values, y_values)
    """
    x_values = [x0]
    y_values = [y0]
    
    x = x0
    y = y0
    
    for _ in range(n):
        k1 = h * f(x, y)
        k2 = h * f(x + h/2, y + k1/2)
        k3 = h * f(x + h/2, y + k2/2)
        k4 = h * f(x + h, y + k3)
        
        y_nuevo = y + (k1 + 2*k2 + 2*k3 + k4) / 6
        x_nuevo = x + h
        
        x_values.append(x_nuevo)
        y_values.append(y_nuevo)
        
        x = x_nuevo
        y = y_nuevo
    
    return x_values, y_values


def metodo_milne(f: Callable[[float, float], float], 
                 x_inicial: List[float], y_inicial: List[float], 
                 h: float, n: int, tolerancia: float = 1e-6) -> Tuple[List[float], List[float], List[dict]]:
    """
    Resuelve una EDO usando el Método de Milne (Predictor-Corrector).
    
    Requiere 4 valores iniciales (índices 0, 1, 2, 3).
    
    PREDICTOR:
      y(n+1)_p = y(n-3) + (4h/3) * [2*f(n) - f(n-1) + 2*f(n-2)]
    
    CORRECTOR:
      y(n+1)_c = y(n-1) + (h/3) * [f(n+1)_p + 4*f(n) + f(n-1)]
    
    Args:
        f: Función f(x, y) que define dy/dx = f(x, y)
        x_inicial: Lista con al menos 4 valores iniciales de x
        y_inicial: Lista con al menos 4 valores iniciales de y
        h: Tamaño del paso
        n: Número de pasos adicionales a calcular
        tolerancia: Tolerancia para convergencia del corrector
    
    Returns:
        Tupla (x_values, y_values, detalles)
    """
    if len(x_inicial) < 4 or len(y_inicial) < 4:
        raise ValueError("Se necesitan al menos 4 valores iniciales")
    
    # Copiar valores iniciales
    x_values = x_inicial.copy()
    y_values = y_inicial.copy()
    
    # Calcular f en los puntos iniciales
    f_values = [f(x, y) for x, y in zip(x_inicial, y_inicial)]
    
    detalles = []
    
    for i in range(n):
        # Índices relativos
        n_idx = len(y_values) - 1  # último punto calculado
        
        # PASO PREDICTOR
        # y(n+1)_p = y(n-3) + (4h/3) * [2*f(n) - f(n-1) + 2*f(n-2)]
        y_predicho = y_values[n_idx - 3] + (4*h/3) * (
            2*f_values[n_idx] - f_values[n_idx - 1] + 2*f_values[n_idx - 2]
        )
        
        x_nuevo = x_values[n_idx] + h
        f_predicho = f(x_nuevo, y_predicho)
        
        # PASO CORRECTOR (iterativo hasta convergencia)
        # y(n+1)_c = y(n-1) + (h/3) * [f(n+1)_p + 4*f(n) + f(n-1)]
        y_corregido = y_predicho
        iteraciones = 0
        max_iter = 10
        
        while iteraciones < max_iter:
            y_anterior = y_corregido
            
            y_corregido = y_values[n_idx - 1] + (h/3) * (
                f(x_nuevo, y_corregido) + 4*f_values[n_idx] + f_values[n_idx - 1]
            )
            
            # Verificar convergencia
            if abs(y_corregido - y_anterior) < tolerancia:
                break
            
            iteraciones += 1
        
        # Calcular f en el punto corregido
        f_nuevo = f(x_nuevo, y_corregido)
        
        # Guardar valores
        x_values.append(x_nuevo)
        y_values.append(y_corregido)
        f_values.append(f_nuevo)
        
        # Guardar detalles
        detalles.append({
            'paso': len(x_values) - 5,  # Paso relativo (después de los 4 iniciales)
            'x': x_nuevo,
            'y_predicho': y_predicho,
            'y_corregido': y_corregido,
            'f_predicho': f_predicho,
            'f_corregido': f_nuevo,
            'iteraciones': iteraciones + 1,
            'error_pc': abs(y_corregido - y_predicho)  # Error predictor-corrector
        })
    
    return x_values, y_values, detalles


def calcular_error_local(y_aproximado: float, y_exacto: float) -> Tuple[float, float]:
    """Calcula el error absoluto y relativo."""
    error_abs = abs(y_aproximado - y_exacto)
    error_rel = (error_abs / abs(y_exacto) * 100) if y_exacto != 0 else 0
    return error_abs, error_rel


# ============================================================================
# FUNCIONES PARA EVALUACIÓN DE EXPRESIONES
# ============================================================================

def crear_funcion_desde_expresion(expresion: str) -> Callable[[float, float], float]:
    """Crea una función f(x, y) a partir de una expresión en texto."""
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
    print(" " * 20 + "MÉTODO DE MILNE")
    print(" " * 15 + "Predictor-Corrector de 4° Orden")
    print("=" * 70)
    print()
    print("PREDICTOR:")
    print("  y(n+1)_p = y(n-3) + (4h/3)*[2*f(n) - f(n-1) + 2*f(n-2)]")
    print()
    print("CORRECTOR:")
    print("  y(n+1)_c = y(n-1) + (h/3)*[f(n+1)_p + 4*f(n) + f(n-1)]")
    print()
    print("Requiere 4 valores iniciales (se calculan con RK4)")
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
    """Solicita al usuario que ingrese la EDO a resolver."""
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
            f = crear_funcion_desde_expresion(expresion)
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
    """Solicita los parámetros del método."""
    print("\nParámetros del método:")
    
    opcion = leer_entero("¿Cómo desea especificar? (1: paso h, 2: número de pasos): ", 1, 2)
    
    if opcion == 1:
        h = leer_float("Tamaño del paso h = ")
        xf = leer_float("Valor final xf = ")
        n = 0
        return h, xf, n
    else:
        xf = leer_float("Valor final xf = ")
        n = leer_entero("Número de pasos n = ", minimo=4)
        h = 0
        return h, xf, n


def mostrar_valores_iniciales(x_inicial: List[float], y_inicial: List[float]):
    """Muestra los valores iniciales calculados con RK4."""
    print("\n" + "=" * 70)
    print("VALORES INICIALES (calculados con Runge-Kutta 4)")
    print("=" * 70)
    print(f"{'i':>3} {'x':>15} {'y':>20}")
    print("-" * 70)
    
    for i, (x, y) in enumerate(zip(x_inicial, y_inicial)):
        print(f"{i:>3} {x:>15.6f} {y:>20.12f}")
    
    print("=" * 70)
    print()


def mostrar_tabla_resultados(titulo: str, x_values: List[float], 
                            y_values: List[float], 
                            inicio_idx: int = 4):
    """Muestra tabla con resultados del método de Milne."""
    print(f"\n{titulo}")
    print("=" * 70)
    print(f"{'i':>3} {'x':>15} {'y':>20}")
    print("=" * 70)
    
    for i in range(inicio_idx, len(x_values)):
        print(f"{i:>3} {x_values[i]:>15.6f} {y_values[i]:>20.12f}")
    
    print("=" * 70)
    print()


def mostrar_pasos_detallados_milne(detalles: List[dict], f_values: List[float], 
                                   num_pasos: int = 2):
    """Muestra los primeros pasos del método de Milne en detalle."""
    print("\n" + "=" * 70)
    print("PRIMEROS PASOS DETALLADOS - MÉTODO DE MILNE")
    print("=" * 70)
    
    for i in range(min(num_pasos, len(detalles))):
        det = detalles[i]
        paso_abs = det['paso'] + 4  # Paso absoluto
        
        print(f"\nPaso {det['paso']} (índice {paso_abs}):")
        print(f"  x = {det['x']:.6f}")
        print()
        
        # Predictor
        print("  PREDICTOR:")
        print(f"  y_p = y({paso_abs-3}) + (4h/3)*[2*f({paso_abs}) - f({paso_abs-1}) + 2*f({paso_abs-2})]")
        print(f"  y_p = {det['y_predicho']:.12f}")
        print(f"  f(x, y_p) = {det['f_predicho']:.12f}")
        print()
        
        # Corrector
        print("  CORRECTOR:")
        print(f"  y_c = y({paso_abs-1}) + (h/3)*[f_p + 4*f({paso_abs}) + f({paso_abs-1})]")
        print(f"  Iteraciones: {det['iteraciones']}")
        print(f"  y_c = {det['y_corregido']:.12f}")
        print(f"  f(x, y_c) = {det['f_corregido']:.12f}")
        print()
        
        print(f"  Error P-C: {det['error_pc']:.12e}")
        print("-" * 70)
    
    print()


def mostrar_analisis_errores(detalles: List[dict]):
    """Muestra análisis de errores predictor-corrector."""
    print("\n" + "=" * 70)
    print("ANÁLISIS DE ERRORES PREDICTOR-CORRECTOR")
    print("=" * 70)
    print(f"{'Paso':>6} {'x':>12} {'Error P-C':>15} {'Iteraciones':>13}")
    print("-" * 70)
    
    for det in detalles:
        print(f"{det['paso']:>6} {det['x']:>12.6f} {det['error_pc']:>15.8e} {det['iteraciones']:>13}")
    
    print("-" * 70)
    
    # Estadísticas
    errores = [d['error_pc'] for d in detalles]
    print(f"\nError P-C máximo: {max(errores):.8e}")
    print(f"Error P-C promedio: {sum(errores)/len(errores):.8e}")
    print(f"Error P-C mínimo: {min(errores):.8e}")
    print("=" * 70)
    print()


def menu_principal() -> int:
    """Muestra el menú principal."""
    print("\nMENÚ PRINCIPAL")
    print("-" * 40)
    print("1. Resolver EDO con Método de Milne")
    print("2. Salir")
    print("-" * 40)
    
    return leer_entero("Seleccione una opción: ", 1, 2)


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta la aplicación."""
    
    while True:
        limpiar_pantalla()
        mostrar_titulo()
        
        opcion = menu_principal()
        
        if opcion == 2:
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
        
        # Verificar que se puedan calcular al menos algunos pasos con Milne
        if n < 4:
            print(f"\nError: Se necesitan al menos 4 pasos (n >= 4)")
            input("\nPresione Enter para continuar...")
            continue
        
        print(f"\nParámetros finales:")
        print(f"  x0 = {x0}, y0 = {y0}")
        print(f"  xf = {xf}")
        print(f"  h = {h:.6f}")
        print(f"  n = {n} pasos totales")
        print(f"  - Primeros 3 pasos: Runge-Kutta 4")
        print(f"  - Siguientes {n-3} pasos: Método de Milne")
        
        try:
            print("\nCalculando valores iniciales con RK4...")
            
            # Calcular los primeros 4 valores con RK4
            x_inicial, y_inicial = metodo_runge_kutta_4_inicial(f, x0, y0, h, 3)
            
            # Mostrar valores iniciales
            mostrar_valores_iniciales(x_inicial, y_inicial)
            
            # Preguntar si continuar con Milne
            if n > 4:
                if not leer_si_no("\n¿Continuar con Método de Milne? (s/n): "):
                    input("\nPresione Enter para continuar...")
                    continue
                
                print("\nAplicando Método de Milne...")
                
                # Aplicar Milne para los pasos restantes
                pasos_milne = n - 3
                x_values, y_values, detalles = metodo_milne(f, x_inicial, y_inicial, 
                                                            h, pasos_milne)
                
                # Mostrar pasos detallados si se solicita
                if leer_si_no("\n¿Mostrar primeros pasos detallados de Milne? (s/n): "):
                    num_pasos = min(2, len(detalles))
                    f_values = [f(x, y) for x, y in zip(x_values, y_values)]
                    mostrar_pasos_detallados_milne(detalles, f_values, num_pasos)
                
                # Mostrar resultados
                mostrar_tabla_resultados("RESULTADOS - MÉTODO DE MILNE", 
                                       x_values, y_values, inicio_idx=4)
                
                # Mostrar análisis de errores P-C
                if leer_si_no("\n¿Mostrar análisis de errores P-C? (s/n): "):
                    mostrar_analisis_errores(detalles)
                
                # Resumen final
                print("\nRESUMEN:")
                print(f"  Valor final: y({xf:.6f}) = {y_values[-1]:.12f}")
                print(f"  Total de puntos calculados: {len(x_values)}")
                print(f"  Puntos con RK4: 4")
                print(f"  Puntos con Milne: {len(detalles)}")
                
            else:
                print("\nSolo se calcularon los valores iniciales con RK4.")
                print("Se necesitan más pasos para aplicar el Método de Milne.")
                
        except Exception as e:
            print(f"\nError: {e}")
        
        input("\nPresione Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    main()