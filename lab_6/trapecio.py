"""
Aplicación para calcular integrales usando la Fórmula de los Trapecios.
Fórmula: A = (h/2)(E + 2P + 2I)
donde:
  E = suma de valores extremos (primer y último punto)
  P = suma de valores pares
  I = suma de valores impares
  h = espaciado entre puntos
"""

import math
from typing import List, Tuple, Callable, Optional


# ============================================================================
# MÓDULO DE LÓGICA: Cálculo de integrales por trapecios
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


def calcular_integral_trapecios(x_values: List[float], y_values: List[float]) -> Tuple[float, dict]:
    """
    Calcula la integral usando la fórmula de los trapecios.
    Fórmula: A = (h/2)(E + 2P + 2I)
    
    Args:
        x_values: Lista de valores x (equiespaciados)
        y_values: Lista de valores y correspondientes
    
    Returns:
        Tupla con (área_calculada, diccionario_con_detalles)
        donde el diccionario contiene: h, E, P, I, y los índices usados
    """
    # Validar y obtener espaciado
    h = validar_puntos(x_values, y_values)
    n = len(y_values)
    
    # Calcular E (extremos): primer y último valor
    E = y_values[0] + y_values[-1]
    extremos_idx = [0, n-1]
    
    # Calcular P (pares): valores en índices pares, excluyendo extremos
    P = 0.0
    pares_idx = []
    for i in range(2, n-1, 2):  # Índices 2, 4, 6, ...
        P += y_values[i]
        pares_idx.append(i)
    
    # Calcular I (impares): valores en índices impares
    I = 0.0
    impares_idx = []
    for i in range(1, n, 2):  # Índices 1, 3, 5, ...
        I += y_values[i]
        impares_idx.append(i)
    
    # Aplicar fórmula: A = (h/2)(E + 2P + 2I)
    area = (h / 2) * (E + 2*P + 2*I)
    
    # Preparar detalles para mostrar
    detalles = {
        'h': h,
        'E': E,
        'P': P,
        'I': I,
        'extremos_idx': extremos_idx,
        'pares_idx': pares_idx,
        'impares_idx': impares_idx,
        'formula': f"({h}/2) * ({E} + 2*{P} + 2*{I})"
    }
    
    return area, detalles


def calcular_trapecios_simple(x_values: List[float], y_values: List[float]) -> float:
    """
    Calcula la integral usando la regla del trapecio simple (suma de trapecios).
    Esta es una implementación alternativa más directa.
    
    Args:
        x_values: Lista de valores x
        y_values: Lista de valores y
    
    Returns:
        Área bajo la curva
    """
    h = validar_puntos(x_values, y_values)
    
    # Sumar áreas de trapecios individuales
    area = 0.0
    for i in range(len(y_values) - 1):
        # Área de trapecio = h * (y[i] + y[i+1]) / 2
        area += (y_values[i] + y_values[i+1]) * h / 2
    
    return area


def calcular_error_trapecios(x_values: List[float], f_segunda_derivada_max: float) -> float:
    """
    Calcula el error teórico del método de trapecios.
    Error ≤ ((b-a)³ / 12n²) * max|f''(x)|
    
    Args:
        x_values: Lista de valores x
        f_segunda_derivada_max: Valor máximo de |f''(x)| en el intervalo
    
    Returns:
        Cota superior del error
    """
    a = x_values[0]
    b = x_values[-1]
    n = len(x_values) - 1  # número de intervalos
    
    error = ((b - a) ** 3 / (12 * n ** 2)) * f_segunda_derivada_max
    return error


# ============================================================================
# MÓDULO DE INTERFAZ: Terminal y entrada/salida
# ============================================================================

def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    print("\n" * 2)


def mostrar_titulo():
    """Muestra el título de la aplicación."""
    print("=" * 70)
    print(" " * 15 + "INTEGRACIÓN POR TRAPECIOS")
    print(" " * 10 + "Fórmula: A = (h/2)(E + 2P + 2I)")
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





def mostrar_tabla(titulo: str, x_values: List[float], y_values: List[float]):
    """
    Muestra una tabla de puntos en formato tabular.
    
    Args:
        titulo: Título de la tabla
        x_values: Valores de x
        y_values: Valores de y
    """
    print(f"\n{titulo}")
    print("-" * 50)
    print(f"{'i':>3} {'x':>15} {'y':>15} {'Tipo':>12}")
    print("-" * 50)
    
    n = len(x_values)
    for i, (x, y) in enumerate(zip(x_values, y_values)):
        # Determinar tipo de punto
        if i == 0 or i == n-1:
            tipo = "Extremo (E)"
        elif i % 2 == 0:
            tipo = "Par (P)"
        else:
            tipo = "Impar (I)"
        
        print(f"{i:>3} {x:>15.6f} {y:>15.6f} {tipo:>12}")
    
    print("-" * 50)
    print()


def mostrar_detalles_calculo(detalles: dict, y_values: List[float]):
    """
    Muestra los detalles del cálculo de la integral.
    
    Args:
        detalles: Diccionario con los detalles del cálculo
        y_values: Lista de valores y para mostrar cuáles se suman
    """
    print("\n" + "=" * 70)
    print("DETALLES DEL CÁLCULO")
    print("=" * 70)
    print(f"\nEspaciado: h = {detalles['h']:.6f}")
    print()
    
    # Mostrar extremos (E)
    print(f"Extremos (E): y[0] + y[{len(y_values)-1}]")
    print(f"  E = {y_values[0]:.6f} + {y_values[-1]:.6f}")
    print(f"  E = {detalles['E']:.6f}")
    print()
    
    # Mostrar pares (P)
    if detalles['pares_idx']:
        print(f"Pares (P): suma de y en índices pares (excepto extremos)")
        suma_str = " + ".join([f"y[{i}]" for i in detalles['pares_idx']])
        valores_str = " + ".join([f"{y_values[i]:.6f}" for i in detalles['pares_idx']])
        print(f"  P = {suma_str}")
        print(f"  P = {valores_str}")
        print(f"  P = {detalles['P']:.6f}")
    else:
        print("Pares (P): (no hay índices pares intermedios)")
        print(f"  P = 0")
    print()
    
    # Mostrar impares (I)
    if detalles['impares_idx']:
        print(f"Impares (I): suma de y en índices impares")
        suma_str = " + ".join([f"y[{i}]" for i in detalles['impares_idx']])
        valores_str = " + ".join([f"{y_values[i]:.6f}" for i in detalles['impares_idx']])
        print(f"  I = {suma_str}")
        print(f"  I = {valores_str}")
        print(f"  I = {detalles['I']:.6f}")
    else:
        print("Impares (I): (no hay índices impares)")
        print(f"  I = 0")
    print()
    
    # Mostrar fórmula aplicada
    print("Aplicando la fórmula: A = (h/2)(E + 2P + 2I)")
    E, P, I, h = detalles['E'], detalles['P'], detalles['I'], detalles['h']
    print(f"  A = ({h:.6f}/2) × ({E:.6f} + 2×{P:.6f} + 2×{I:.6f})")
    print(f"  A = {h/2:.6f} × ({E:.6f} + {2*P:.6f} + {2*I:.6f})")
    print(f"  A = {h/2:.6f} × {E + 2*P + 2*I:.6f}")
    print("=" * 70)
    print()


def mostrar_resultado(area: float, x_values: List[float], 
                     valor_real: Optional[float] = None):
    """
    Muestra el resultado de la integral calculada.
    
    Args:
        area: Área calculada por el método de trapecios
        x_values: Lista de valores x (para mostrar límites)
        valor_real: Valor real de la integral (opcional)
    """
    print("\n" + "=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)
    print(f"Integral en [{x_values[0]:.6f}, {x_values[-1]:.6f}]")
    print(f"Área calculada = {area:.10f}")
    
    if valor_real is not None:
        error = abs(area - valor_real)
        error_rel = (error / abs(valor_real) * 100) if valor_real != 0 else 0
        print(f"\nValor real = {valor_real:.10f}")
        print(f"Error absoluto = {error:.10e}")
        print(f"Error relativo = {error_rel:.6f}%")
    
    print("=" * 70)
    print()


def menu_principal() -> int:
    """
    Muestra el menú principal y retorna la opción seleccionada.
    
    Returns:
        Opción seleccionada (1 o 2)
    """
    print("\nMENÚ PRINCIPAL")
    print("-" * 40)
    print("1. Calcular integral por trapecios")
    print("2. Salir")
    print("-" * 40)
    
    return leer_entero("Seleccione una opción: ", 1, 2)


def calcular_integral_real(func: Callable, a: float, b: float) -> Optional[float]:
    """
    Calcula la integral real de una función conocida.
    (Función no utilizada en esta versión)
    
    Args:
        func: Función a integrar
        a: Límite inferior
        b: Límite superior
    
    Returns:
        None (función deshabilitada)
    """
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
        
        if opcion == 2:
            print("\n¡Gracias por usar el programa!")
            break
        
        # Obtener puntos manualmente
        x_values, y_values = solicitar_puntos()
        
        # Mostrar puntos ingresados con clasificación
        mostrar_tabla("Puntos ingresados:", x_values, y_values)
        
        try:
            # Calcular integral usando la fórmula de trapecios
            area, detalles = calcular_integral_trapecios(x_values, y_values)
            
            # Mostrar detalles del cálculo
            mostrar_detalles_calculo(detalles, y_values)
            
            # Mostrar resultado final
            mostrar_resultado(area, x_values)
            
            # Ofrecer comparación con método simple
            if leer_si_no("\n¿Desea ver el resultado con método simple? (s/n): "):
                area_simple = calcular_trapecios_simple(x_values, y_values)
                print(f"\nMétodo simple (suma de trapecios): {area_simple:.10f}")
                print(f"Diferencia: {abs(area - area_simple):.10e}")
            
        except Exception as e:
            print(f"\nError: {e}")
        
        input("\nPresione Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    main()