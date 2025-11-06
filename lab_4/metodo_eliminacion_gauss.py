import numpy as np

def eliminacion_gauss(matriz, decimales=3):
    """
    Realiza la eliminación de Gauss en una matriz aumentada.
    
    Parámetros:
    -----------
    matriz : list o numpy.array
        Matriz aumentada [A|b] del sistema de ecuaciones
    decimales : int
        Número de decimales para el redondeo
    
    Retorna:
    --------
    pasos : list
        Lista con cada paso del proceso de escalonamiento
    """
    
    # Convertir a numpy array y hacer una copia
    A = np.array(matriz, dtype=float)
    n = len(A)
    
    # Lista para guardar todos los pasos
    pasos = []
    
    # Guardar matriz original
    pasos.append({
        'paso': 0,
        'descripcion': 'Matriz original (Sistema aumentado [A|b])',
        'matriz': np.round(A.copy(), decimales),
        'operaciones': []
    })
    
    # Proceso de eliminación hacia adelante
    for k in range(n - 1):
        operaciones = []
        
        # Para cada fila debajo de la fila pivote
        for i in range(k + 1, n):
            # Calcular el multiplicador
            multiplicador = A[i, k] / A[k, k]
            multiplicador = np.round(multiplicador, decimales)
            
            # Guardar operación realizada
            operaciones.append(f"F{i+1} = F{i+1} - ({multiplicador}) × F{k+1}")
            
            # Aplicar la operación a toda la fila
            for j in range(n + 1):
                if j < k:
                    # Mantener elementos anteriores
                    pass
                elif j == k:
                    # Hacer cero en la columna pivote
                    A[i, j] = 0
                else:
                    # Restar multiplicador por elemento de fila pivote
                    A[i, j] = A[i, j] - multiplicador * A[k, j]
                    A[i, j] = np.round(A[i, j], decimales)
        
        # Guardar el paso
        pasos.append({
            'paso': k + 1,
            'descripcion': f'Eliminación en columna {k+1} (hacer ceros debajo del pivote a{k+1}{k+1})',
            'matriz': np.round(A.copy(), decimales),
            'operaciones': operaciones
        })
    
    return pasos


def sustitucion_atras(matriz_escalonada, decimales=3):
    """
    Resuelve el sistema usando sustitución hacia atrás.
    
    Parámetros:
    -----------
    matriz_escalonada : numpy.array
        Matriz triangular superior aumentada
    decimales : int
        Número de decimales para el redondeo
    
    Retorna:
    --------
    solucion : numpy.array
        Vector solución [x1, x2, ..., xn]
    """
    n = len(matriz_escalonada)
    x = np.zeros(n)
    
    # Desde la última fila hacia arriba
    for i in range(n - 1, -1, -1):
        suma = matriz_escalonada[i, n]  # Término independiente
        
        # Restar los términos ya conocidos
        for j in range(i + 1, n):
            suma -= matriz_escalonada[i, j] * x[j]
        
        # Dividir por el coeficiente diagonal
        x[i] = suma / matriz_escalonada[i, i]
        x[i] = np.round(x[i], decimales)
    
    return x


def verificar_solucion(matriz_original, solucion, decimales=3):
    """
    Verifica la solución reemplazando en las ecuaciones originales.
    
    Parámetros:
    -----------
    matriz_original : numpy.array
        Matriz aumentada original
    solucion : numpy.array
        Vector solución
    decimales : int
        Número de decimales para el redondeo
    
    Retorna:
    --------
    verificacion : list
        Lista con resultados calculados vs originales
    """
    n = len(solucion)
    verificacion = []
    
    for i in range(n):
        resultado = 0
        for j in range(n):
            resultado += matriz_original[i, j] * solucion[j]
        resultado = np.round(resultado, decimales)
        
        verificacion.append({
            'ecuacion': i + 1,
            'calculado': resultado,
            'original': matriz_original[i, n]
        })
    
    return verificacion


def imprimir_paso(paso):
    """Imprime un paso del proceso de eliminación de forma legible."""
    print(f"\n{'='*70}")
    print(f"PASO {paso['paso']}: {paso['descripcion']}")
    print('='*70)
    
    if paso['operaciones']:
        print("\nOperaciones realizadas:")
        for op in paso['operaciones']:
            print(f"  • {op}")
    
    print("\nMatriz resultante:")
    matriz = paso['matriz']
    n = len(matriz)
    
    # Imprimir matriz con formato
    for i in range(n):
        fila = "[ "
        for j in range(n):
            fila += f"{matriz[i,j]:8.3f} "
        fila += f"| {matriz[i,n]:8.3f} ]"
        print(fila)


def resolver_sistema_completo(matriz, decimales=3, verbose=True):
    """
    Resuelve un sistema de ecuaciones completo mostrando todos los pasos.
    
    Parámetros:
    -----------
    matriz : list o numpy.array
        Matriz aumentada del sistema
    decimales : int
        Número de decimales para el redondeo
    verbose : bool
        Si True, imprime todos los pasos
    
    Retorna:
    --------
    dict con pasos, solución y verificación
    """
    matriz_original = np.array(matriz, dtype=float)
    
    # Realizar eliminación de Gauss
    pasos = eliminacion_gauss(matriz, decimales)
    
    if verbose:
        for paso in pasos:
            imprimir_paso(paso)
    
    # Obtener matriz escalonada final
    matriz_escalonada = pasos[-1]['matriz']
    
    # Resolver por sustitución hacia atrás
    solucion = sustitucion_atras(matriz_escalonada, decimales)
    
    if verbose:
        print(f"\n{'='*70}")
        print("SOLUCIÓN POR SUSTITUCIÓN HACIA ATRÁS")
        print('='*70)
        for i, valor in enumerate(solucion):
            print(f"  x{i+1} = {valor:.{decimales}f}")
    
    # Verificar solución
    verificacion = verificar_solucion(matriz_original, solucion, decimales)
    
    if verbose:
        print(f"\n{'='*70}")
        print("VERIFICACIÓN")
        print('='*70)
        for v in verificacion:
            print(f"  Ecuación {v['ecuacion']}: {v['calculado']:.{decimales}f} ≈ {v['original']:.{decimales}f}")
    
    return {
        'pasos': pasos,
        'solucion': solucion,
        'verificacion': verificacion
    }


def ingresar_matriz():
    """
    Permite al usuario ingresar una matriz por teclado.
    
    Retorna:
    --------
    matriz : list
        Matriz aumentada ingresada por el usuario
    decimales : int
        Número de decimales para redondeo
    """
    print("\n" + "="*70)
    print("INGRESO DE MATRIZ")
    print("="*70)
    
    # Solicitar tamaño del sistema
    while True:
        try:
            n = int(input("\n¿Cuántas ecuaciones tiene el sistema? (n): "))
            if n < 2:
                print("El sistema debe tener al menos 2 ecuaciones.")
                continue
            break
        except ValueError:
            print("Por favor ingrese un número válido.")
    
    # Solicitar decimales de redondeo
    while True:
        try:
            decimales = int(input("¿Cuántos decimales desea usar para el redondeo? (recomendado: 3): "))
            if decimales < 0:
                print("Los decimales deben ser positivos.")
                continue
            break
        except ValueError:
            print("Por favor ingrese un número válido.")
    
    print(f"\nIngrese los coeficientes de la matriz aumentada {n}x{n+1}")
    print("(Para cada ecuación: a1, a2, ..., an, b)")
    print("-" * 70)
    
    matriz = []
    
    for i in range(n):
        print(f"\nEcuación {i+1}:")
        while True:
            try:
                # Solicitar toda la fila
                entrada = input(f"  Ingrese {n+1} valores separados por espacio o coma: ")
                # Permitir separación por espacios o comas
                valores = entrada.replace(',', ' ').split()
                
                if len(valores) != n + 1:
                    print(f"  Error: Debe ingresar exactamente {n+1} valores.")
                    continue
                
                # Convertir a float
                fila = [float(v) for v in valores]
                matriz.append(fila)
                break
            except ValueError:
                print("  Error: Ingrese solo números válidos.")
    
    return matriz, decimales


def menu_principal():
    """
    Menú principal para interactuar con el programa.
    """
    while True:
        print("\n" + "="*70)
        print("MÉTODO DE ELIMINACIÓN DE GAUSS")
        print("="*70)
        print("\n1. Ingresar matriz por teclado")
        print("2. Usar ejemplo del PDF (sistema 3x3)")
        print("3. Usar ejemplo 2x2")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            # Ingresar por teclado
            matriz, decimales = ingresar_matriz()
            
            print("\n" + "="*70)
            print("MATRIZ INGRESADA")
            print("="*70)
            n = len(matriz)
            for i in range(n):
                fila = "[ "
                for j in range(n):
                    fila += f"{matriz[i][j]:8.3f} "
                fila += f"| {matriz[i][n]:8.3f} ]"
                print(fila)
            
            confirmar = input("\n¿Desea continuar con esta matriz? (s/n): ")
            if confirmar.lower() == 's':
                resultado = resolver_sistema_completo(matriz, decimales=decimales, verbose=True)
                
                print("\n" + "="*70)
                print("PROCESO COMPLETADO")
                print("="*70)
            
        elif opcion == "2":
            # Ejemplo del PDF
            print("\nUsando ejemplo del PDF:")
            matriz = [
                [18.72, 8.2, 8.76, 121.280],
                [6.4, 15.9, 7.18, 126.321],
                [5.22, 6.4, 14.31, 118.522]
            ]
            
            print("\nSistema de ecuaciones:")
            print("18.72x + 8.2y + 8.76z = 121.280")
            print("6.4x + 15.9y + 7.18z = 126.321")
            print("5.22x + 6.4y + 14.31z = 118.522")
            
            input("\nPresione Enter para continuar...")
            resultado = resolver_sistema_completo(matriz, decimales=3, verbose=True)
            
            print("\n" + "="*70)
            print("PROCESO COMPLETADO")
            print("="*70)
            
        elif opcion == "3":
            # Ejemplo 2x2
            print("\nUsando ejemplo 2x2:")
            matriz = [
                [2, 3, 8],
                [4, -1, 2]
            ]
            
            print("\nSistema de ecuaciones:")
            print("2x + 3y = 8")
            print("4x - y = 2")
            
            input("\nPresione Enter para continuar...")
            resultado = resolver_sistema_completo(matriz, decimales=3, verbose=True)
            
            print("\n" + "="*70)
            print("PROCESO COMPLETADO")
            print("="*70)
            
        elif opcion == "4":
            print("\n¡Hasta luego!")
            break
        else:
            print("\nOpción no válida. Por favor intente nuevamente.")
        
        input("\nPresione Enter para volver al menú principal...")


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    menu_principal()