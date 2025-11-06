import numpy as np

def es_diagonalmente_dominante(A):
    """
    Verifica si la matriz es diagonalmente dominante.
    Una matriz es diagonalmente dominante si para cada fila,
    el valor absoluto del elemento diagonal es mayor que la suma
    de los valores absolutos de los demás elementos de la fila.
    """
    n = A.shape[0]
    print("\n" + "="*60)
    print("VERIFICACIÓN DE CONVERGENCIA")
    print("="*60)
    print("\nCondición: La matriz debe ser DIAGONALMENTE DOMINANTE")
    print("Es decir: |a[i,i]| > suma(|a[i,j]|) para j != i\n")
    
    es_dominante = True
    for i in range(n):
        diagonal = abs(A[i, i])
        suma_otros = sum(abs(A[i, j]) for j in range(n) if j != i)
        
        cumple = diagonal > suma_otros
        simbolo = ">" if cumple else "<="
        
        print(f"Fila {i+1}: |{A[i,i]:.2f}| = {diagonal:.2f} {simbolo} {suma_otros:.2f} = ", end="")
        print(" + ".join([f"|{A[i,j]:.2f}|" for j in range(n) if j != i]), end="")
        print(f"  {'✓' if cumple else '✗'}")
        
        if not cumple:
            es_dominante = False
    
    print("\n" + "="*60)
    if es_dominante:
        print("✓ La matriz ES diagonalmente dominante")
        print("∴ Cumple con la condición de convergencia")
    else:
        print("✗ La matriz NO es diagonalmente dominante")
        print("⚠ El método puede NO converger")
    print("="*60)
    
    return es_dominante

def gauss_seidel(A, b, x0=None, tolerancia=0.01, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Seidel.
    
    Parámetros:
    A: matriz de coeficientes (n x n)
    b: vector de términos independientes (n)
    x0: vector inicial (si es None, se usa [1, 1, ..., 1])
    tolerancia: criterio de parada (máxima diferencia entre iteraciones)
    max_iter: número máximo de iteraciones
    
    Retorna:
    x: vector solución
    iteraciones: número de iteraciones realizadas
    """
    n = len(b)
    
    # Verificar convergencia
    if not es_diagonalmente_dominante(A):
        respuesta = input("\n¿Desea continuar de todas formas? (s/n): ").lower()
        if respuesta != 's':
            return None, 0
    
    # Vector inicial
    if x0 is None:
        x = np.ones(n)
    else:
        x = np.array(x0, dtype=float)
    
    print("\n" + "="*60)
    print("APLICACIÓN DEL MÉTODO DE GAUSS-SEIDEL")
    print("="*60)
    
    # Mostrar las ecuaciones despejadas
    print("\nEcuaciones despejadas:")
    variables = ['x', 'y', 'z', 'w', 'v'] if n <= 5 else [f'x{i+1}' for i in range(n)]
    for i in range(n):
        var = variables[i]
        print(f"\n{var} = (", end="")
        print(f"{b[i]:.3f}", end="")
        for j in range(n):
            if i != j:
                print(f" - {A[i,j]:.2f}*{variables[j]}", end="")
        print(f") / {A[i,i]:.2f}")
    
    print(f"\nValor inicial: ", end="")
    for i in range(n):
        print(f"{variables[i]}₀ = {x[i]:.3f}", end="  ")
    print("\n")
    
    x_anterior = x.copy()
    
    # Iteraciones
    for iteracion in range(max_iter):
        print("="*60)
        print(f"ITERACIÓN {iteracion + 1}")
        print("="*60 + "\n")
        
        # Guardar valores anteriores para calcular el error
        x_anterior = x.copy()
        
        # Calcular cada variable
        for i in range(n):
            suma = b[i]
            
            # Mostrar el cálculo paso a paso
            print(f"{variables[i]}_{iteracion+1} = (", end="")
            print(f"{b[i]:.3f}", end="")
            
            # Restar los términos
            for j in range(n):
                if i != j:
                    suma -= A[i, j] * x[j]
                    print(f" - {A[i,j]:.2f} * {x[j]:.3f}", end="")
            
            x[i] = suma / A[i, i]
            print(f") / {A[i,i]:.2f}")
            print(f"{variables[i]}_{iteracion+1} = {x[i]:.3f}\n")
        
        # Calcular errores
        print("Errores:")
        errores = []
        for i in range(n):
            error = abs(x[i] - x_anterior[i])
            errores.append(error)
            print(f"E({variables[i]}) = |{x[i]:.3f} - {x_anterior[i]:.3f}| = {error:.3f}")
        
        error_max = max(errores)
        print(f"\nError máximo: {error_max:.3f}")
        
        # Verificar convergencia
        if error_max < tolerancia:
            print(f"\n✓ Convergencia alcanzada (error < {tolerancia})")
            print("="*60)
            return x, iteracion + 1
        
        print()
    
    print(f"\n⚠ Se alcanzó el número máximo de iteraciones ({max_iter})")
    print("="*60)
    return x, max_iter

def imprimir_solucion(x):
    """Imprime la solución final"""
    variables = ['x', 'y', 'z', 'w', 'v'] if len(x) <= 5 else [f'x{i+1}' for i in range(len(x))]
    
    print("\n" + "="*60)
    print("SOLUCIÓN FINAL")
    print("="*60)
    for i, val in enumerate(x):
        print(f"{variables[i]} = {val:.4f}")
    print("="*60)

def verificar_solucion(A, b, x):
    """Verifica la solución sustituyendo en las ecuaciones originales"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE LA SOLUCIÓN")
    print("="*60)
    
    n = len(x)
    for i in range(n):
        resultado = sum(A[i, j] * x[j] for j in range(n))
        print(f"\nEcuación {i + 1}:")
        print(f"  Resultado: {resultado:.3f}")
        print(f"  Esperado:  {b[i]:.3f}")
        print(f"  Error:     {abs(resultado - b[i]):.6f}")

def ingresar_sistema():
    """Permite ingresar el sistema de ecuaciones por terminal"""
    print("\n" + "="*60)
    print("INGRESO DEL SISTEMA DE ECUACIONES")
    print("="*60)
    
    n = int(input("\nNúmero de ecuaciones (variables): "))
    
    print(f"\nIngrese los coeficientes de la matriz A ({n}x{n}):")
    A = []
    for i in range(n):
        print(f"\nFila {i + 1}:")
        fila = []
        for j in range(n):
            valor = float(input(f"  a[{i+1},{j+1}]: "))
            fila.append(valor)
        A.append(fila)
    
    print(f"\nIngrese el vector de términos independientes:")
    b = []
    for i in range(n):
        valor = float(input(f"  b[{i+1}]: "))
        b.append(valor)
    
    print(f"\nValor inicial (dejar vacío para usar 1 en todas las variables):")
    x0_input = input("  Valores separados por coma (ej: 1,1,1): ").strip()
    if x0_input:
        x0 = [float(x) for x in x0_input.split(',')]
    else:
        x0 = None
    
    tolerancia = float(input("\nTolerancia (ej: 0.01): ") or "0.01")
    max_iter = int(input("Máximo de iteraciones (ej: 100): ") or "100")
    
    return np.array(A), np.array(b), x0, tolerancia, max_iter

# Programa principal
if __name__ == "__main__":
    print("\n" + "="*60)
    print("MÉTODO DE GAUSS-SEIDEL")
    print("Resolución de Sistemas de Ecuaciones Lineales")
    print("="*60)
    
    opcion = input("\n¿Desea usar el ejemplo del documento? (s/n): ").lower()
    
    if opcion == 's':
        # Ejemplo del documento
        A = np.array([
            [18.72, 8.2, 8.76],
            [6.4, 15.9, 7.18],
            [5.22, 6.4, 14.31]
        ])
        b = np.array([121.280, 126.321, 118.522])
        x0 = [1, 1, 1]
        tolerancia = 0.01
        max_iter = 100
    else:
        A, b, x0, tolerancia, max_iter = ingresar_sistema()
    
    # Resolver el sistema
    solucion, num_iter = gauss_seidel(A, b, x0, tolerancia, max_iter)
    
    if solucion is not None:
        imprimir_solucion(solucion)
        verificar_solucion(A, b, solucion)
        print(f"\nNúmero de iteraciones: {num_iter}")
    
    print("\n" + "="*60)
    print("Proceso completado")
    print("="*60)