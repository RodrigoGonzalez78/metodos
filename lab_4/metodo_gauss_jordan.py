import numpy as np

def imprimir_matriz(matriz, titulo=""):
    """Imprime la matriz de forma legible"""
    if titulo:
        print(f"\n{titulo}")
    filas, cols = matriz.shape
    for i in range(filas):
        # Imprime la parte de coeficientes
        for j in range(cols - 1):
            print(f"{matriz[i][j]:10.4f}", end=" ")
        # Imprime la parte de términos independientes
        print(f"| {matriz[i][cols-1]:10.4f}")
    print()

def gauss_jordan(matriz_ampliada):
    """
    Aplica el método de Gauss-Jordan a una matriz ampliada para encontrar
    la forma escalonada reducida por filas (RREF).
    
    Parámetros:
    matriz_ampliada: numpy array de dimensión n x (n+1)
    
    Retorna:
    soluciones: array con los valores de x1, x2, ..., xn
    """
    # Crear una copia para no modificar la original
    A = matriz_ampliada.copy().astype(float)
    n = A.shape[0]
    
    print("="*60)
    print("MÉTODO DE GAUSS-JORDAN (CORREGIDO)")
    print("="*60)
    imprimir_matriz(A, "Matriz ampliada inicial:")
    
    # Iterar por cada fila (que actuará como pivote)
    for i in range(n):
        
        # --- 1. Pivoteo (Para estabilidad numérica) ---
        # Buscar el máximo en la columna actual (desde la fila i)
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k, i]) > abs(A[max_row, i]):
                max_row = k
        
        # Intercambiar la fila actual (i) con la fila del máximo (max_row)
        if max_row != i:
            A[[i, max_row]] = A[[max_row, i]]
            print(f"\n-> INTERCAMBIO: Fila {i+1} <-> Fila {max_row+1}")
            imprimir_matriz(A)

        # --- 2. Normalización (Hacer que el pivote A[i, i] sea 1) ---
        pivote = A[i, i]
        if abs(pivote) < 1e-10:
            print("Error: La matriz es singular, el sistema no tiene solución única.")
            return None # No se puede dividir por cero
            
        # Dividir toda la fila del pivote por el valor del pivote
        A[i, :] = A[i, :] / pivote
        print(f"\n-> NORMALIZACIÓN: Fila {i+1} = Fila {i+1} / {pivote:.4f}")
        imprimir_matriz(A)
        
        # --- 3. Eliminación (Hacer ceros arriba y abajo del pivote) ---
        # Iterar por todas las demás filas (k)
        for k in range(n):
            if k == i:
                continue # Omitir la fila pivote
                
            # Factor por el que multiplicar la fila pivote
            factor = A[k, i]
            
            if abs(factor) > 1e-10: # Si no es ya cero
                # Restar (factor * fila_pivote) a la fila k
                A[k, :] = A[k, :] - factor * A[i, :]
                print(f"\n-> ELIMINACIÓN: Fila {k+1} = Fila {k+1} - ({factor:.4f}) * Fila {i+1}")
        
        imprimir_matriz(A, f"Matriz después de procesar Columna {i+1}:")

    # Al final del bucle, la matriz de coeficientes (izquierda)
    # debe ser la matriz identidad.
    # La última columna (derecha) contendrá las soluciones.
    
    soluciones = A[:, -1]
    
    print("\n" + "="*60)
    print("SOLUCIÓN DEL SISTEMA")
    print("="*60)
    print("La matriz de coeficientes es ahora la Identidad.")
    print("La última columna contiene la solución:")
    for i, sol in enumerate(soluciones):
        print(f"x{i + 1} = {sol:.4f}")
    
    return soluciones

def ingresar_matriz():
    """Permite ingresar la matriz ampliada por terminal"""
    print("\n" + "="*60)
    print("INGRESO DE DATOS")
    print("="*60)
    
    n = int(input("Ingrese el número de ecuaciones (variables): "))
    
    print(f"\nIngrese la matriz ampliada {n}x{n+1}")
    print("(Coeficientes de las variables y términos independientes)")
    
    matriz = []
    for i in range(n):
        print(f"\nEcuación {i + 1}:")
        fila = []
        for j in range(n):
            valor = float(input(f"  Coeficiente de x{j + 1}: "))
            fila.append(valor)
        termino = float(input(f"  Término independiente: "))
        fila.append(termino)
        matriz.append(fila)
    
    return np.array(matriz)

def verificar_solucion(matriz_original, soluciones):
    """Verifica la solución sustituyendo en las ecuaciones originales"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE LA SOLUCIÓN")
    print("="*60)
    
    n = len(soluciones)
    for i in range(n):
        suma = 0
        terminos = []
        for j in range(n):
            producto = matriz_original[i, j] * soluciones[j]
            suma += producto
            terminos.append(f"{matriz_original[i, j]:.2f}*{soluciones[j]:.4f}")
        
        print(f"\nEcuación {i + 1}:")
        print(f"  {' + '.join(terminos)}")
        print(f"  = {suma:.4f} ≈ {matriz_original[i, -1]:.4f}")
        diferencia = abs(suma - matriz_original[i, -1])
        print(f"  (Diferencia: {diferencia:.6f})")

# Programa principal
if __name__ == "__main__":
    print("\n" + "="*60)
    print("RESOLUCIÓN DE SISTEMAS DE ECUACIONES")
    print("MÉTODO DE GAUSS-JORDAN")
    print("="*60)
    
    opcion = input("\n¿Desea usar el ejemplo del documento? (s/n): ").lower()
    
    if opcion == 's':
        # Ejemplo del documento (el que tenías en tu código)
        matriz_ejemplo = np.array([
            [18.72, 8.2, 8.76, 121.280],
            [6.4, 15.9, 7.18, 126.321],
            [5.22, 6.4, 14.31, 118.522]
        ])
        matriz_original = matriz_ejemplo.copy()
        soluciones = gauss_jordan(matriz_ejemplo)
    else:
        # Ingresar la matriz de la imagen (4.3, 3, 2, 960...)
        matriz = ingresar_matriz()
        matriz_original = matriz.copy()
        soluciones = gauss_jordan(matriz)
    
    # Solo verificar si se encontró una solución
    if soluciones is not None:
        verificar_solucion(matriz_original, soluciones)
    
    print("\n" + "="*60)
    print("Proceso completado")
    print("="*60)