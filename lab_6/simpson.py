"""
Aplicación para calcular integrales usando las Fórmulas de Simpson.

Fórmula de Simpson 1/3: A = (h/3)(E + 2P + 4I)
donde:
  E = suma de valores extremos (primer y último punto)
  P = suma de valores pares (índices 2, 4, 6, ...)
  I = suma de valores impares (índices 1, 3, 5, ...)
  h = espaciado entre puntos
  Requiere número impar de puntos (n par de intervalos)

Fórmula de Simpson 3/8: A = (3h/8)(y₀ + 3y₁ + 3y₂ + y₃)
  Se aplica a grupos de 4 puntos consecutivos
  Útil cuando el número de puntos no es apropiado para 1/3
"""

import math
from typing import List, Tuple, Optional


# ============================================================================
# MÓDULO DE LÓGICA: Cálculo de integrales por Simpson
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
    
    if len(x_values) < 3:
        raise ValueError("Se necesitan al menos 3 puntos")
    
    # Calcular el espaciado h
    h = x_values[1] - x_values[0]
    
    # Verificar que los puntos estén equiespaciados
    for i in range(1, len(x_values) - 1):
        diff = abs((x_values[i+1] - x_values[i]) - h)
        if diff > 1e-10:
            raise ValueError("Los puntos deben estar equiespaciados")
    
    return h


def calcular_simpson_1_3(x_values: List[float], y_values: List[float]) -> Tuple[float, dict]:
    """
    Calcula la integral usando la fórmula de Simpson 1/3.
    Fórmula: A = (h/3)(E + 2P + 4I)
    
    Requiere un número impar de puntos (número par de intervalos).
    
    Args:
        x_values: Lista de valores x (equiespaciados)
        y_values: Lista de valores y correspondientes
    
    Returns:
        Tupla con (área_calculada, diccionario_con_detalles)
    
    Raises:
        ValueError: Si el número de puntos es par
    """
    n = len(y_values)
    
    # Verificar que hay número impar de puntos
    if n % 2 == 0:
        raise ValueError("Simpson 1/3 requiere número impar de puntos (número par de intervalos)")
    
    # Validar y obtener espaciado
    h = validar_puntos(x_values, y_values)
    
    # Calcular E (extremos): primer y último valor
    E = y_values[0] + y_values[-1]
    extremos_idx = [0, n-1]
    
    # Calcular P (pares): valores en índices pares, excluyendo extremos
    # Índices: 2, 4, 6, ... (pero no 0 ni el último)
    P = 0.0
    pares_idx = []
    for i in range(2, n-1, 2):
        P += y_values[i]
        pares_idx.append(i)
    
    # Calcular I (impares): valores en índices impares
    # Índices: 1, 3, 5, ...
    I = 0.0
    impares_idx = []
    for i in range(1, n, 2):
        I += y_values[i]
        impares_idx.append(i)
    
    # Aplicar fórmula: A = (h/3)(E + 2P + 4I)
    area = (h / 3) * (E + 2*P + 4*I)
    
    # Preparar detalles
    detalles = {
        'h': h,
        'E': E,
        'P': P,
        'I': I,
        'extremos_idx': extremos_idx,
        'pares_idx': pares_idx,
        'impares_idx': impares_idx,
        'metodo': 'Simpson 1/3',
        'formula': f"({h}/3) * ({E} + 2*{P} + 4*{I})"
    }
    
    return area, detalles


def calcular_simpson_3_8(x_values: List[float], y_values: List[float]) -> Tuple[float, dict]:
    """
    Calcula la integral usando la fórmula de Simpson 3/8.
    Fórmula: A = (3h/8)(y₀ + 3y₁ + 3y₂ + y₃)
    
    Se aplica a grupos de 4 puntos consecutivos.
    Si hay más de 4 puntos, se aplica múltiples veces.
    
    Args:
        x_values: Lista de valores x (equiespaciados)
        y_values: Lista de valores y correspondientes
    
    Returns:
        Tupla con (área_calculada, diccionario_con_detalles)
    
    Raises:
        ValueError: Si el número de intervalos no es múltiplo de 3
    """
    n = len(y_values)
    
    # Validar y obtener espaciado
    h = validar_puntos(x_values, y_values)
    
    # Número de intervalos debe ser múltiplo de 3
    num_intervalos = n - 1
    if num_intervalos % 3 != 0:
        raise ValueError("Simpson 3/8 requiere que (n-1) sea múltiplo de 3")
    
    area_total = 0.0
    grupos = []
    
    # Aplicar fórmula por grupos de 4 puntos
    i = 0
    while i < n - 1:
        if i + 3 < n:
            # Grupo completo de 4 puntos
            y0, y1, y2, y3 = y_values[i], y_values[i+1], y_values[i+2], y_values[i+3]
            area_grupo = (3 * h / 8) * (y0 + 3*y1 + 3*y2 + y3)
            area_total += area_grupo
            
            grupos.append({
                'indices': [i, i+1, i+2, i+3],
                'valores': [y0, y1, y2, y3],
                'area': area_grupo
            })
            
            i += 3  # Avanzar 3 intervalos
        else:
            break
    
    # Preparar detalles
    detalles = {
        'h': h,
        'grupos': grupos,
        'num_grupos': len(grupos),
        'metodo': 'Simpson 3/8',
        'formula': '(3h/8) * (y₀ + 3y₁ + 3y₂ + y₃)'
    }
    
    return area_total, detalles


def calcular_simpson_combinado(x_values: List[float], y_values: List[float]) -> Tuple[float, dict]:
    """
    Calcula la integral usando una combinación de Simpson 1/3 y 3/8.
    Útil cuando el número de puntos no es apropiado para ninguna fórmula sola.
    
    Args:
        x_values: Lista de valores x
        y_values: Lista de valores y
    
    Returns:
        Tupla con (área_calculada, diccionario_con_detalles)
    """
    n = len(y_values)
    h = validar_puntos(x_values, y_values)
    
    num_intervalos = n - 1
    
    # Determinar estrategia
    if num_intervalos % 2 == 0:
        # Número par de intervalos -> usar Simpson 1/3
        return calcular_simpson_1_3(x_values, y_values)
    elif num_intervalos % 3 == 0:
        # Número múltiplo de 3 -> usar Simpson 3/8
        return calcular_simpson_3_8(x_values, y_values)
    else:
        # Combinar: usar 3/8 para los primeros 3 intervalos, 1/3 para el resto
        if num_intervalos >= 3 and (num_intervalos - 3) % 2 == 0:
            # Aplicar 3/8 a los primeros 4 puntos
            area_3_8, detalles_3_8 = calcular_simpson_3_8(x_values[:4], y_values[:4])
            
            # Aplicar 1/3 al resto
            area_1_3, detalles_1_3 = calcular_simpson_1_3(x_values[3:], y_values[3:])
            
            area_total = area_3_8 + area_1_3
            
            detalles = {
                'metodo': 'Simpson Combinado (3/8 + 1/3)',
                'area_3_8': area_3_8,
                'area_1_3': area_1_3,
                'puntos_3_8': 4,
                'puntos_1_3': len(x_values) - 3,
                'detalles_3_8': detalles_3_8,
                'detalles_1_3': detalles_1_3
            }
            
            return area_total, detalles
        else:
            raise ValueError(f"Número de intervalos ({num_intervalos}) no es apropiado para Simpson")


# ============================================================================
# MÓDULO DE INTERFAZ: Terminal y entrada/salida
# ============================================================================

def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    print("\n" * 2)


def mostrar_titulo():
    """Muestra el título de la aplicación."""
    print("=" * 70)
    print(" " * 15 + "INTEGRACIÓN POR SIMPSON")
    print(" " * 8 + "Simpson 1/3: A = (h/3)(E + 2P + 4I)")
    print(" " * 6 + "Simpson 3/8: A = (3h/8)(y₀ + 3y₁ + 3y₂ + y₃)")
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
    
    n = leer_entero("¿Cuántos puntos desea ingresar? (mínimo 3): ", minimo=3)
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


def mostrar_detalles_simpson_1_3(detalles: dict, y_values: List[float]):
    """
    Muestra los detalles del cálculo de Simpson 1/3.
    
    Args:
        detalles: Diccionario con los detalles del cálculo
        y_values: Lista de valores y
    """
    print("\n" + "=" * 70)
    print("DETALLES DEL CÁLCULO - SIMPSON 1/3")
    print("=" * 70)
    print(f"\nEspaciado: h = {detalles['h']:.6f}")
    print(f"Fórmula: A = (h/3)(E + 2P + 4I)")
    print()
    
    # Mostrar extremos (E)
    print(f"Extremos (E): y[0] + y[{len(y_values)-1}]")
    print(f"  E = {y_values[0]:.6f} + {y_values[-1]:.6f}")
    print(f"  E = {detalles['E']:.6f}")
    print()
    
    # Mostrar pares (P)
    if detalles['pares_idx']:
        print(f"Pares (P): suma de y en índices pares (2, 4, 6, ...)")
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
        print(f"Impares (I): suma de y en índices impares (1, 3, 5, ...)")
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
    print("Aplicando la fórmula: A = (h/3)(E + 2P + 4I)")
    E, P, I, h = detalles['E'], detalles['P'], detalles['I'], detalles['h']
    print(f"  A = ({h:.6f}/3) × ({E:.6f} + 2×{P:.6f} + 4×{I:.6f})")
    print(f"  A = {h/3:.6f} × ({E:.6f} + {2*P:.6f} + {4*I:.6f})")
    print(f"  A = {h/3:.6f} × {E + 2*P + 4*I:.6f}")
    print("=" * 70)
    print()


def mostrar_detalles_simpson_3_8(detalles: dict, y_values: List[float]):
    """
    Muestra los detalles del cálculo de Simpson 3/8.
    
    Args:
        detalles: Diccionario con los detalles del cálculo
        y_values: Lista de valores y
    """
    print("\n" + "=" * 70)
    print("DETALLES DEL CÁLCULO - SIMPSON 3/8")
    print("=" * 70)
    print(f"\nEspaciado: h = {detalles['h']:.6f}")
    print(f"Fórmula: A = (3h/8)(y₀ + 3y₁ + 3y₂ + y₃)")
    print(f"Número de grupos: {detalles['num_grupos']}")
    print()
    
    for idx, grupo in enumerate(detalles['grupos'], 1):
        print(f"Grupo {idx}: índices {grupo['indices']}")
        y0, y1, y2, y3 = grupo['valores']
        print(f"  A = (3×{detalles['h']:.6f}/8) × ({y0:.6f} + 3×{y1:.6f} + 3×{y2:.6f} + {y3:.6f})")
        print(f"  A = {3*detalles['h']/8:.6f} × ({y0:.6f} + {3*y1:.6f} + {3*y2:.6f} + {y3:.6f})")
        print(f"  A = {3*detalles['h']/8:.6f} × {y0 + 3*y1 + 3*y2 + y3:.6f}")
        print(f"  A = {grupo['area']:.10f}")
        print()
    
    print("=" * 70)
    print()


def mostrar_detalles_combinado(detalles: dict, y_values: List[float]):
    """
    Muestra los detalles del cálculo combinado.
    
    Args:
        detalles: Diccionario con los detalles del cálculo
        y_values: Lista de valores y
    """
    print("\n" + "=" * 70)
    print("DETALLES DEL CÁLCULO - SIMPSON COMBINADO")
    print("=" * 70)
    print(f"\nMétodo: {detalles['metodo']}")
    print(f"Primeros 4 puntos: Simpson 3/8")
    print(f"Puntos restantes: Simpson 1/3")
    print()
    
    print(f"Área (Simpson 3/8): {detalles['area_3_8']:.10f}")
    print(f"Área (Simpson 1/3): {detalles['area_1_3']:.10f}")
    print("=" * 70)
    print()


def mostrar_resultado(area: float, x_values: List[float], metodo: str):
    """
    Muestra el resultado de la integral calculada.
    
    Args:
        area: Área calculada
        x_values: Lista de valores x
        metodo: Método usado
    """
    print("\n" + "=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)
    print(f"Método: {metodo}")
    print(f"Integral en [{x_values[0]:.6f}, {x_values[-1]:.6f}]")
    print(f"Área calculada = {area:.10f}")
    print("=" * 70)
    print()


def menu_principal() -> int:
    """
    Muestra el menú principal y retorna la opción seleccionada.
    
    Returns:
        Opción seleccionada
    """
    print("\nMENÚ PRINCIPAL")
    print("-" * 40)
    print("1. Simpson 1/3 (requiere n impar)")
    print("2. Simpson 3/8 (requiere n-1 múltiplo de 3)")
    print("3. Simpson automático (elige el mejor)")
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
        
        # Obtener puntos manualmente
        x_values, y_values = solicitar_puntos()
        
        # Mostrar puntos ingresados con clasificación
        mostrar_tabla("Puntos ingresados:", x_values, y_values)
        
        try:
            # Calcular según el método seleccionado
            if opcion == 1:
                # Simpson 1/3
                area, detalles = calcular_simpson_1_3(x_values, y_values)
                mostrar_detalles_simpson_1_3(detalles, y_values)
                mostrar_resultado(area, x_values, "Simpson 1/3")
                
            elif opcion == 2:
                # Simpson 3/8
                area, detalles = calcular_simpson_3_8(x_values, y_values)
                mostrar_detalles_simpson_3_8(detalles, y_values)
                mostrar_resultado(area, x_values, "Simpson 3/8")
                
            else:  # opcion == 3
                # Simpson automático
                area, detalles = calcular_simpson_combinado(x_values, y_values)
                
                if 'Combinado' in detalles.get('metodo', ''):
                    mostrar_detalles_combinado(detalles, y_values)
                elif detalles.get('metodo') == 'Simpson 1/3':
                    mostrar_detalles_simpson_1_3(detalles, y_values)
                else:
                    mostrar_detalles_simpson_3_8(detalles, y_values)
                
                mostrar_resultado(area, x_values, detalles['metodo'])
            
        except Exception as e:
            print(f"\nError: {e}")
            print("\nSugerencias:")
            n = len(y_values)
            print(f"  - Número de puntos actual: {n}")
            print(f"  - Para Simpson 1/3: use {n+1 if n%2==0 else n} puntos (impar)")
            print(f"  - Para Simpson 3/8: use {n+((3-(n-1)%3)%3)} puntos (n-1 múltiplo de 3)")
        
        input("\nPresione Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    main()