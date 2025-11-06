import numpy as np

def imprimir_matriz(matriz, titulo=""):
    """Imprime la matriz de forma legible"""
    if titulo:
        print(f"\n{titulo}")
    filas, cols = matriz.shape
    for i in range(filas):
        for j in range(cols - 1):
            print(f"{matriz[i][j]:8.2f}", end=" ")
        print(f"| {matriz[i][cols-1]:8.2f}")
    print()

def imprimir_matriz_con_columnas(matriz, columnas_mostrar, titulo=""):
    """Imprime la matriz mostrando solo las columnas especificadas"""
    if titulo:
        print(f"\n{titulo}")
    filas, cols = matriz.shape
    for i in range(filas):
        for j in columnas_mostrar:
            if j < cols - 1:
                print(f"{matriz[i][j]:8.2f}", end=" ")
            else:
                print(f"| {matriz[i][j]:8.2f}", end="")
        print()
    print()

def gauss_jordan(matriz_ampliada):
    """
    Aplica el método de Gauss-Jordan a una matriz ampliada.
    
    Parámetros:
    matriz_ampliada: numpy array de dimensión n x (n+1)
    
    Retorna:
    soluciones: array con los valores de x1, x2, ..., xn
    """
    # Crear una copia para no modificar la original
    A = matriz_ampliada.copy().astype(float)
    n = A.shape[0]
    
    print("="*60)
    print("MÉTODO DE GAUSS-JORDAN")
    print("="*60)
    imprimir_matriz(A, "Matriz ampliada inicial:")
    
    iteracion = 1
    
    # Para cada columna (excepto la última que es el vector de términos independientes)
    for col in range(n):
        print(f"\n{'='*60}")
        print(f"ITERACIÓN {iteracion}: Eliminando columna {col + 1}")
        print(f"{'='*60}")
        
        # Elemento pivote (primera fila, columna actual)
        pivote = A[0, col]
        
        if abs(pivote) < 1e-10:
            print(f"Advertencia: Pivote muy pequeño en columna {col + 1}")
            continue
        
        print(f"\nPivote: a[1,{col+1}] = {pivote:.4f}")
        print(f"\nOperaciones para eliminar columna {col + 1}:")
        
        # Para cada fila (excepto la primera)
        for fila in range(1, n - col):
            factor = A[fila, col] / pivote
            print(f"\n  Fila {fila + 1}:")
            
            # Mostrar las operaciones elemento por elemento
            for j in range(col + 1, n + 1):
                valor_original = A[fila, j]
                valor_primera_fila = A[0, j]
                if j < n:
                    print(f"    a[{fila+1},{j+1}] = {valor_original:.2f} - {valor_primera_fila:.2f} * {A[fila, col]:.2f}/{pivote:.2f}", end="")
                else:
                    print(f"    b[{fila+1}] = {valor_original:.3f} - {valor_primera_fila:.3f} * {A[fila, col]:.2f}/{pivote:.2f}", end="")
                
                # Actualizar el elemento
                A[fila, j] = A[fila, j] - A[0, j] * factor
                print(f" = {A[fila, j]:.2f}")
        
        # Dividir la primera fila por el pivote
        print(f"\n  Normalizando primera fila (dividiendo por {pivote:.4f}):")
        for j in range(col + 1, n + 1):
            valor_original = A[0, j]
            A[0, j] = A[0, j] / pivote
            if j < n:
                print(f"    a[1,{j+1}] = {valor_original:.2f}/{pivote:.2f} = {A[0, j]:.4f}")
            else:
                print(f"    b[1] = {valor_original:.3f}/{pivote:.2f} = {A[0, j]:.4f}")
        
        # Mostrar matriz con columna eliminada (no se muestra la columna col)
        columnas_restantes = list(range(col + 1, n + 1))
        print(f"\nMatriz con columna {col + 1} eliminada:")
        imprimir_matriz_con_columnas(A, columnas_restantes, "")
        
        # Mover la primera fila al final
        primera_fila = A[0].copy()
        A = np.vstack([A[1:], primera_fila])
        
        print(f"Matriz después de mover la primera fila al final:")
        imprimir_matriz_con_columnas(A, columnas_restantes, "")
        
        iteracion += 1
    
    # Extraer soluciones (última columna)
    soluciones = A[:, -1]
    
    print("\n" + "="*60)
    print("SOLUCIÓN DEL SISTEMA")
    print("="*60)
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

# Programa principal
if __name__ == "__main__":
    print("\n" + "="*60)
    print("RESOLUCIÓN DE SISTEMAS DE ECUACIONES")
    print("MÉTODO DE GAUSS-JORDAN")
    print("="*60)
    
    opcion = input("\n¿Desea usar el ejemplo del documento? (s/n): ").lower()
    
    if opcion == 's':
        # Ejemplo del documento
        matriz_ejemplo = np.array([
            [18.72, 8.2, 8.76, 121.280],
            [6.4, 15.9, 7.18, 126.321],
            [5.22, 6.4, 14.31, 118.522]
        ])
        matriz_original = matriz_ejemplo.copy()
        soluciones = gauss_jordan(matriz_ejemplo)
    else:
        matriz = ingresar_matriz()
        matriz_original = matriz.copy()
        soluciones = gauss_jordan(matriz)
    
    verificar_solucion(matriz_original, soluciones)
    
    print("\n" + "="*60)
    print("Proceso completado")
    print("="*60)