
import numpy as np


# ========================================================================
# Módulo de cálculo - Funciones principales
# ========================================================================

def factorizar_lu(A):
    """
    Realiza la factorización A = LU usando eliminación de Gauss
    
    Args:
        A: Matriz de coeficientes (numpy array o lista de listas)
        
    Returns:
        tuple: (L, U, pasos_eliminacion)
            - L: Matriz triangular inferior
            - U: Matriz triangular superior
            - pasos_eliminacion: Lista de diccionarios con el historial
            
    Raises:
        ValueError: Si se encuentra un pivote cero
    """
    A = np.array(A, dtype=float)
    n = len(A)
    
    L = np.eye(n)
    U = A.copy()
    pasos_eliminacion = []
    
    for k in range(n - 1):
        # Registrar estado antes de la eliminación
        paso = {
            'columna': k,
            'matriz_antes': U.copy(),
            'factores': []
        }
        
        for i in range(k + 1, n):
            # Verificar pivote
            if U[k, k] == 0:
                raise ValueError(
                    f"Pivote cero encontrado en posición ({k},{k}). "
                    "Se requiere pivoteo parcial o total."
                )
            
            # Calcular factor de eliminación
            factor = U[i, k] / U[k, k]
            L[i, k] = factor
            
            # Registrar información del factor
            paso['factores'].append({
                'fila_destino': i,
                'fila_pivote': k,
                'factor': factor,
                'numerador': U[i, k],
                'denominador': U[k, k]
            })
            
            # Aplicar eliminación: Fila_i = Fila_i - factor * Fila_k
            U[i, k:] = U[i, k:] - factor * U[k, k:]
        
        # Registrar estado después de la eliminación
        paso['matriz_despues'] = U.copy()
        pasos_eliminacion.append(paso)
    
    return L, U, pasos_eliminacion


def resolver_ly_b(L, b):
    """
    Resuelve el sistema triangular inferior Ly = b
    mediante sustitución hacia adelante
    
    Args:
        L: Matriz triangular inferior
        b: Vector de términos independientes
        
    Returns:
        tuple: (y, pasos_sustitucion_adelante)
            - y: Vector solución
            - pasos_sustitucion_adelante: Lista con el historial
    """
    L = np.array(L, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    
    y = np.zeros(n)
    pasos_sustitucion_adelante = []
    
    for i in range(n):
        # Calcular suma de términos ya conocidos
        suma = sum(L[i, j] * y[j] for j in range(i))
        
        # Calcular y_i
        y[i] = (b[i] - suma) / L[i, i]
        
        # Registrar paso
        pasos_sustitucion_adelante.append({
            'indice': i,
            'suma_terminos': suma,
            'termino_independiente': b[i],
            'coeficiente_diagonal': L[i, i],
            'resultado': y[i],
            'ecuacion': f"y[{i}] = ({b[i]} - {suma}) / {L[i, i]}"
        })
    
    return y, pasos_sustitucion_adelante


def resolver_ux_y(U, y):
    """
    Resuelve el sistema triangular superior Ux = y
    mediante sustitución hacia atrás
    
    Args:
        U: Matriz triangular superior
        y: Vector de términos independientes
        
    Returns:
        tuple: (x, pasos_sustitucion_atras)
            - x: Vector solución del sistema original
            - pasos_sustitucion_atras: Lista con el historial
    """
    U = np.array(U, dtype=float)
    y = np.array(y, dtype=float)
    n = len(y)
    
    x = np.zeros(n)
    pasos_sustitucion_atras = []
    
    for i in range(n - 1, -1, -1):
        # Calcular suma de términos ya conocidos
        suma = sum(U[i, j] * x[j] for j in range(i + 1, n))
        
        # Calcular x_i
        x[i] = (y[i] - suma) / U[i, i]
        
        # Registrar paso
        pasos_sustitucion_atras.append({
            'indice': i,
            'suma_terminos': suma,
            'termino_independiente': y[i],
            'coeficiente_diagonal': U[i, i],
            'resultado': x[i],
            'ecuacion': f"x[{i}] = ({y[i]} - {suma}) / {U[i, i]}"
        })
    
    return x, pasos_sustitucion_atras


def resolver_completo(A, b):
    """
    Ejecuta el proceso completo de factorización y resolución
    
    Args:
        A: Matriz de coeficientes
        b: Vector de términos independientes
        
    Returns:
        dict: Diccionario con todos los resultados:
            - 'A': Matriz original
            - 'b': Vector original
            - 'L': Matriz triangular inferior
            - 'U': Matriz triangular superior
            - 'y': Vector intermedio
            - 'x': Vector solución
            - 'pasos_eliminacion': Historial de eliminación
            - 'pasos_sustitucion_adelante': Historial sustitución adelante
            - 'pasos_sustitucion_atras': Historial sustitución atrás
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    # Paso 1: Factorización
    L, U, pasos_eliminacion = factorizar_lu(A)
    
    # Paso 2: Resolver Ly = b
    y, pasos_sustitucion_adelante = resolver_ly_b(L, b)
    
    # Paso 3: Resolver Ux = y
    x, pasos_sustitucion_atras = resolver_ux_y(U, y)
    
    return {
        'A': A,
        'b': b,
        'L': L,
        'U': U,
        'y': y,
        'x': x,
        'pasos_eliminacion': pasos_eliminacion,
        'pasos_sustitucion_adelante': pasos_sustitucion_adelante,
        'pasos_sustitucion_atras': pasos_sustitucion_atras
    }


# ========================================================================
# Módulo de verificación
# ========================================================================

def verificar_factorizacion(L, U):
    """
    Verifica que L * U = A
    
    Args:
        L: Matriz triangular inferior
        U: Matriz triangular superior
        
    Returns:
        numpy.ndarray: Producto L*U
    """
    return np.matmul(L, U)


def verificar_solucion(A, x, b):
    """
    Verifica que A * x = b y calcula el error
    
    Args:
        A: Matriz de coeficientes
        x: Vector solución
        b: Vector de términos independientes
        
    Returns:
        tuple: (Ax, error)
            - Ax: Producto A*x
            - error: Norma del error ||A*x - b||
    """
    Ax = np.matmul(A, x)
    error = np.linalg.norm(Ax - b)
    return Ax, error


# ========================================================================
# Módulo de presentación
# ========================================================================

def imprimir_matriz(matriz, precision=4):
    """Imprime una matriz con formato"""
    if matriz is None:
        print("  [No calculada]")
        return
    
    for fila in matriz:
        valores = "  ".join(f"{val:>{precision+4}.{precision}f}" for val in fila)
        print(f"  [{valores}]")


def imprimir_vector(vector, precision=4):
    """Imprime un vector con formato"""
    if vector is None:
        print("  [No calculado]")
        return
    
    valores = "  ".join(f"{val:.{precision}f}" for val in vector)
    print(f"  [{valores}]")


def mostrar_sistema_original(A, b):
    """Muestra el sistema de ecuaciones original"""
    print("=" * 60)
    print("FACTORIZACIÓN LU - SISTEMA DE ECUACIONES")
    print("=" * 60)
    print("\n📋 SISTEMA ORIGINAL Ax = b:")
    print("\nMatriz A:")
    imprimir_matriz(A)
    print("\nVector b:")
    imprimir_vector(b)


def mostrar_factorizacion(L, U, pasos_eliminacion):
    """Muestra el proceso completo de factorización"""
    print("\n" + "=" * 60)
    print("PASO 1: FACTORIZACIÓN A = LU")
    print("=" * 60)
    print("\n🔧 Aplicando Eliminación de Gauss...\n")
    
    for paso in pasos_eliminacion:
        k = paso['columna']
        print(f"{'─' * 60}")
        print(f"Eliminando columna {k + 1}")
        print(f"{'─' * 60}")
        print("\nMatriz actual:")
        imprimir_matriz(paso['matriz_antes'])
        
        for info in paso['factores']:
            i = info['fila_destino']
            k = info['fila_pivote']
            factor = info['factor']
            num = info['numerador']
            den = info['denominador']
            
            print(f"\n  Factor f[{i+1},{k+1}] = {num:.4f} / {den:.4f} = {factor:.6f}")
            print(f"  Operación: Fila[{i+1}] = Fila[{i+1}] - ({factor:.6f}) × Fila[{k+1}]")
    
    print(f"\n{'─' * 60}")
    print("✅ FACTORIZACIÓN COMPLETADA")
    print(f"{'─' * 60}")
    
    print("\n📐 Matriz L (triangular inferior unitaria):")
    imprimir_matriz(L)
    
    print("\n📐 Matriz U (triangular superior):")
    imprimir_matriz(U)
    
    # Verificación
    verificacion = verificar_factorizacion(L, U)
    print("\n🔍 Verificación L × U:")
    imprimir_matriz(verificacion)


def mostrar_sustitucion_adelante(y, pasos_sustitucion_adelante):
    """Muestra la sustitución hacia adelante"""
    print("\n" + "=" * 60)
    print("PASO 2: RESOLVER Ly = b (Sustitución hacia adelante)")
    print("=" * 60)
    print("\n🔽 Resolviendo desde arriba hacia abajo...\n")
    
    for paso in pasos_sustitucion_adelante:
        i = paso['indice']
        print(f"  y[{i+1}] = ({paso['termino_independiente']:.4f} - {paso['suma_terminos']:.4f}) / "
              f"{paso['coeficiente_diagonal']:.4f} = {paso['resultado']:.6f}")
    
    print("\n✅ Vector y:")
    imprimir_vector(y)


def mostrar_sustitucion_atras(x, pasos_sustitucion_atras):
    """Muestra la sustitución hacia atrás"""
    print("\n" + "=" * 60)
    print("PASO 3: RESOLVER Ux = y (Sustitución hacia atrás)")
    print("=" * 60)
    print("\n🔼 Resolviendo desde abajo hacia arriba...\n")
    
    # Invertir para mostrar en orden de ejecución
    for paso in reversed(pasos_sustitucion_atras):
        i = paso['indice']
        print(f"  x[{i+1}] = ({paso['termino_independiente']:.4f} - {paso['suma_terminos']:.4f}) / "
              f"{paso['coeficiente_diagonal']:.4f} = {paso['resultado']:.6f}")


def mostrar_solucion(A, b, x):
    """Muestra la solución final y verificaciones"""
    print("\n" + "=" * 60)
    print("✅ SOLUCIÓN DEL SISTEMA")
    print("=" * 60)
    
    n = len(x)
    print("\n🎯 Vector solución x:")
    for i in range(n):
        print(f"  x[{i+1}] = {x[i]:.8f}")
    
    # Verificación
    Ax, error = verificar_solucion(A, x, b)
    
    print("\n🔍 Verificación A × x:")
    imprimir_vector(Ax)
    
    print("\n📊 Vector b original:")
    imprimir_vector(b)
    
    print(f"\n📉 Error ||Ax - b||: {error:.2e}")
    
    if error < 1e-10:
        print("✅ Solución exacta (error despreciable)")
    elif error < 1e-6:
        print("✅ Solución aceptable")
    else:
        print("⚠️ Error significativo detectado")


def mostrar_todo(resultados):
    """Muestra el proceso completo"""
    mostrar_sistema_original(resultados['A'], resultados['b'])
    mostrar_factorizacion(resultados['L'], resultados['U'], resultados['pasos_eliminacion'])
    mostrar_sustitucion_adelante(resultados['y'], resultados['pasos_sustitucion_adelante'])
    mostrar_sustitucion_atras(resultados['x'], resultados['pasos_sustitucion_atras'])
    mostrar_solucion(resultados['A'], resultados['b'], resultados['x'])


# ========================================================================
# Módulo de entrada/salida
# ========================================================================

def leer_sistema_por_teclado():
    """
    Solicita al usuario ingresar la matriz A y el vector b desde teclado.
    
    Returns:
        tuple: (A, b) como listas de listas y lista
    """
    print("=" * 60)
    print("🔢 INGRESO DE DATOS PARA SISTEMA Ax = b")
    print("=" * 60)
    
    # Leer tamaño del sistema
    n = int(input("Ingrese el tamaño del sistema (número de ecuaciones): "))
    
    A = []
    print("\nIngrese los coeficientes de la matriz A fila por fila:")
    for i in range(n):
        fila = input(f"  Fila {i+1} (separe los valores por espacios): ").split()
        A.append([float(x) for x in fila])
    
    print("\nIngrese los valores del vector b:")
    b = [float(x) for x in input("  Valores de b (separe por espacios): ").split()]
    
    # Validaciones básicas
    if len(b) != n:
        raise ValueError("El tamaño del vector b debe coincidir con el de la matriz A.")
    
    return A, b


def resolver_sistema_lu(A, b, mostrar_pasos=True):
    """
    Función de conveniencia para resolver un sistema Ax=b
    
    Args:
        A: Matriz de coeficientes
        b: Vector de términos independientes
        mostrar_pasos: Si True, muestra el proceso completo en terminal
    
    Returns:
        tuple: (L, U, x) o None si hay error
    """
    try:
        resultados = resolver_completo(A, b)
        
        if mostrar_pasos:
            mostrar_todo(resultados)
        
        return resultados['L'], resultados['U'], resultados['x']
    
    except ValueError as e:
        print(f"❌ Error: {e}")
        return None, None, None


# ========================================================================
# Programa principal
# ========================================================================

if __name__ == "__main__":
    
    try:
        A, b = leer_sistema_por_teclado()
        print("\n✅ Sistema cargado correctamente.\n")
        
        # Resolver el sistema ingresado
        resolver_sistema_lu(A, b, mostrar_pasos=True)
        
    except ValueError as e:
        print(f"❌ Error en los datos: {e}")
    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")