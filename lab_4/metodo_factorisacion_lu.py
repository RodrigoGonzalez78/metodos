
import numpy as np

class FactorizacionLU:
    """
    Clase que encapsula toda la lógica de factorización LU
    No contiene ninguna lógica de presentación
    """
    
    def __init__(self, A, b):
        """
        Inicializa con la matriz A y el vector b
        
        Args:
            A: Matriz de coeficientes (lista de listas o numpy array)
            b: Vector de términos independientes (lista o numpy array)
        """
        self.A_original = np.array(A, dtype=float)
        self.b_original = np.array(b, dtype=float)
        self.n = len(A)
        
        # Matrices resultado
        self.L = None
        self.U = None
        self.y = None
        self.x = None
        
        # Historial de operaciones
        self.pasos_eliminacion = []
        self.pasos_sustitucion_adelante = []
        self.pasos_sustitucion_atras = []
    
    def factorizar(self):
        """
        Realiza la factorización A = LU usando eliminación de Gauss
        
        Returns:
            tuple: (L, U) matrices triangulares
            
        Raises:
            ValueError: Si se encuentra un pivote cero
        """
        self.L = np.eye(self.n)
        self.U = self.A_original.copy()
        self.pasos_eliminacion = []
        
        for k in range(self.n - 1):
            # Registrar estado antes de la eliminación
            paso = {
                'columna': k,
                'matriz_antes': self.U.copy(),
                'factores': []
            }
            
            for i in range(k + 1, self.n):
                # Verificar pivote
                if self.U[k, k] == 0:
                    raise ValueError(
                        f"Pivote cero encontrado en posición ({k},{k}). "
                        "Se requiere pivoteo parcial o total."
                    )
                
                # Calcular factor de eliminación
                factor = self.U[i, k] / self.U[k, k]
                self.L[i, k] = factor
                
                # Registrar información del factor
                paso['factores'].append({
                    'fila_destino': i,
                    'fila_pivote': k,
                    'factor': factor,
                    'numerador': self.U[i, k],
                    'denominador': self.U[k, k]
                })
                
                # Aplicar eliminación: Fila_i = Fila_i - factor * Fila_k
                self.U[i, k:] = self.U[i, k:] - factor * self.U[k, k:]
            
            # Registrar estado después de la eliminación
            paso['matriz_despues'] = self.U.copy()
            self.pasos_eliminacion.append(paso)
        
        return self.L, self.U
    
    def resolver_ly_b(self):
        """
        Resuelve el sistema triangular inferior Ly = b
        mediante sustitución hacia adelante
        
        Returns:
            numpy.ndarray: Vector y
            
        Raises:
            ValueError: Si no se ha ejecutado factorizar() primero
        """
        if self.L is None:
            raise ValueError("Debe ejecutar factorizar() antes de resolver Ly=b")
        
        self.y = np.zeros(self.n)
        self.pasos_sustitucion_adelante = []
        
        for i in range(self.n):
            # Calcular suma de términos ya conocidos
            suma = sum(self.L[i, j] * self.y[j] for j in range(i))
            
            # Calcular y_i
            self.y[i] = (self.b_original[i] - suma) / self.L[i, i]
            
            # Registrar paso
            self.pasos_sustitucion_adelante.append({
                'indice': i,
                'suma_terminos': suma,
                'termino_independiente': self.b_original[i],
                'coeficiente_diagonal': self.L[i, i],
                'resultado': self.y[i],
                'ecuacion': f"y[{i}] = ({self.b_original[i]} - {suma}) / {self.L[i, i]}"
            })
        
        return self.y
    
    def resolver_ux_y(self):
        """
        Resuelve el sistema triangular superior Ux = y
        mediante sustitución hacia atrás
        
        Returns:
            numpy.ndarray: Vector x (solución del sistema original)
            
        Raises:
            ValueError: Si no se ha ejecutado resolver_ly_b() primero
        """
        if self.y is None:
            raise ValueError("Debe ejecutar resolver_ly_b() antes de resolver Ux=y")
        
        self.x = np.zeros(self.n)
        self.pasos_sustitucion_atras = []
        
        for i in range(self.n - 1, -1, -1):
            # Calcular suma de términos ya conocidos
            suma = sum(self.U[i, j] * self.x[j] for j in range(i + 1, self.n))
            
            # Calcular x_i
            self.x[i] = (self.y[i] - suma) / self.U[i, i]
            
            # Registrar paso
            self.pasos_sustitucion_atras.append({
                'indice': i,
                'suma_terminos': suma,
                'termino_independiente': self.y[i],
                'coeficiente_diagonal': self.U[i, i],
                'resultado': self.x[i],
                'ecuacion': f"x[{i}] = ({self.y[i]} - {suma}) / {self.U[i, i]}"
            })
        
        return self.x
    
    def resolver_completo(self):
        """
        Ejecuta el proceso completo de factorización y resolución
        
        Returns:
            tuple: (L, U, x) - Matrices L, U y vector solución x
        """
        self.factorizar()
        self.resolver_ly_b()
        self.resolver_ux_y()
        return self.L, self.U, self.x
    
    def verificar_factorizacion(self):
        """
        Verifica que L * U = A
        
        Returns:
            numpy.ndarray: Producto L*U o None si no se ha factorizado
        """
        if self.L is None or self.U is None:
            return None
        return np.matmul(self.L, self.U)
    
    def verificar_solucion(self):
        """
        Verifica que A * x = b
        
        Returns:
            numpy.ndarray: Producto A*x o None si no hay solución
        """
        if self.x is None:
            return None
        return np.matmul(self.A_original, self.x)
    
    def calcular_error(self):
        """
        Calcula la norma del error ||A*x - b||
        
        Returns:
            float: Norma del error o None si no hay solución
        """
        verificacion = self.verificar_solucion()
        if verificacion is None:
            return None
        return np.linalg.norm(verificacion - self.b_original)
    
    def obtener_resultados(self):
        """
        Retorna un diccionario con todos los resultados
        
        Returns:
            dict: Diccionario con todos los resultados y matrices
        """
        return {
            'A': self.A_original,
            'b': self.b_original,
            'L': self.L,
            'U': self.U,
            'y': self.y,
            'x': self.x,
            'verificacion_LU': self.verificar_factorizacion(),
            'verificacion_Ax': self.verificar_solucion(),
            'error': self.calcular_error(),
            'pasos_eliminacion': self.pasos_eliminacion,
            'pasos_sustitucion_adelante': self.pasos_sustitucion_adelante,
            'pasos_sustitucion_atras': self.pasos_sustitucion_atras
        }


# ========================================================================
# ARCHIVO: presentador_terminal.py
# Módulo de presentación para terminal/consola
# ========================================================================

class PresentadorTerminal:
    """
    Clase responsable de presentar los resultados en la terminal
    Recibe una instancia de FactorizacionLU y formatea la salida
    """
    
    def __init__(self, factorizacion_lu):
        """
        Args:
            factorizacion_lu: Instancia de FactorizacionLU
        """
        self.flu = factorizacion_lu
    
    def mostrar_sistema_original(self):
        """Muestra el sistema de ecuaciones original"""
        print("=" * 60)
        print("FACTORIZACIÓN LU - SISTEMA DE ECUACIONES")
        print("=" * 60)
        print("\n📋 SISTEMA ORIGINAL Ax = b:")
        print("\nMatriz A:")
        self._imprimir_matriz(self.flu.A_original)
        print("\nVector b:")
        self._imprimir_vector(self.flu.b_original)
    
    def mostrar_factorizacion(self):
        """Muestra el proceso completo de factorización"""
        print("\n" + "=" * 60)
        print("PASO 1: FACTORIZACIÓN A = LU")
        print("=" * 60)
        print("\n🔧 Aplicando Eliminación de Gauss...\n")
        
        for paso in self.flu.pasos_eliminacion:
            k = paso['columna']
            print(f"{'─' * 60}")
            print(f"Eliminando columna {k + 1}")
            print(f"{'─' * 60}")
            print("\nMatriz actual:")
            self._imprimir_matriz(paso['matriz_antes'])
            
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
        self._imprimir_matriz(self.flu.L)
        
        print("\n📐 Matriz U (triangular superior):")
        self._imprimir_matriz(self.flu.U)
        
        # Verificación
        verificacion = self.flu.verificar_factorizacion()
        print("\n🔍 Verificación L × U:")
        self._imprimir_matriz(verificacion)
    
    def mostrar_sustitucion_adelante(self):
        """Muestra la sustitución hacia adelante"""
        print("\n" + "=" * 60)
        print("PASO 2: RESOLVER Ly = b (Sustitución hacia adelante)")
        print("=" * 60)
        print("\n🔽 Resolviendo desde arriba hacia abajo...\n")
        
        for paso in self.flu.pasos_sustitucion_adelante:
            i = paso['indice']
            print(f"  y[{i+1}] = ({paso['termino_independiente']:.4f} - {paso['suma_terminos']:.4f}) / "
                  f"{paso['coeficiente_diagonal']:.4f} = {paso['resultado']:.6f}")
        
        print("\n✅ Vector y:")
        self._imprimir_vector(self.flu.y)
    
    def mostrar_sustitucion_atras(self):
        """Muestra la sustitución hacia atrás"""
        print("\n" + "=" * 60)
        print("PASO 3: RESOLVER Ux = y (Sustitución hacia atrás)")
        print("=" * 60)
        print("\n🔼 Resolviendo desde abajo hacia arriba...\n")
        
        # Invertir para mostrar en orden de ejecución
        for paso in reversed(self.flu.pasos_sustitucion_atras):
            i = paso['indice']
            print(f"  x[{i+1}] = ({paso['termino_independiente']:.4f} - {paso['suma_terminos']:.4f}) / "
                  f"{paso['coeficiente_diagonal']:.4f} = {paso['resultado']:.6f}")
    
    def mostrar_solucion(self):
        """Muestra la solución final y verificaciones"""
        print("\n" + "=" * 60)
        print("✅ SOLUCIÓN DEL SISTEMA")
        print("=" * 60)
        
        print("\n🎯 Vector solución x:")
        for i in range(self.flu.n):
            print(f"  x[{i+1}] = {self.flu.x[i]:.8f}")
        
        # Verificación
        verificacion = self.flu.verificar_solucion()
        error = self.flu.calcular_error()
        
        print("\n🔍 Verificación A × x:")
        self._imprimir_vector(verificacion)
        
        print("\n📊 Vector b original:")
        self._imprimir_vector(self.flu.b_original)
        
        print(f"\n📉 Error ||Ax - b||: {error:.2e}")
        
        if error < 1e-10:
            print("✅ Solución exacta (error despreciable)")
        elif error < 1e-6:
            print("✅ Solución aceptable")
        else:
            print("⚠️ Error significativo detectado")
    
    def mostrar_todo(self):
        """Muestra el proceso completo"""
        self.mostrar_sistema_original()
        self.mostrar_factorizacion()
        self.mostrar_sustitucion_adelante()
        self.mostrar_sustitucion_atras()
        self.mostrar_solucion()
    
    def _imprimir_matriz(self, matriz, precision=4):
        """Imprime una matriz con formato"""
        if matriz is None:
            print("  [No calculada]")
            return
        
        for fila in matriz:
            valores = "  ".join(f"{val:>{precision+4}.{precision}f}" for val in fila)
            print(f"  [{valores}]")
    
    def _imprimir_vector(self, vector, precision=4):
        """Imprime un vector con formato"""
        if vector is None:
            print("  [No calculado]")
            return
        
        valores = "  ".join(f"{val:.{precision}f}" for val in vector)
        print(f"  [{valores}]")



def resolver_sistema_lu(A, b, mostrar_pasos=True):
    """
    Función de conveniencia para resolver un sistema Ax=b
    
    Args:
        A: Matriz de coeficientes
        b: Vector de términos independientes
        mostrar_pasos: Si True, muestra el proceso completo en terminal
    
    Returns:
        tuple: (L, U, x) o el objeto FactorizacionLU si se necesita más control
    """
    flu = FactorizacionLU(A, b)
    
    try:
        L, U, x = flu.resolver_completo()
        
        if mostrar_pasos:
            presentador = PresentadorTerminal(flu)
            presentador.mostrar_todo()
        
        return L, U, x
    
    except ValueError as e:
        print(f"❌ Error: {e}")
        return None, None, None





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
        tuple: (L, U, x) o el objeto FactorizacionLU si se necesita más control
    """
    flu = FactorizacionLU(A, b)
    
    try:
        L, U, x = flu.resolver_completo()
        
        if mostrar_pasos:
            presentador = PresentadorTerminal(flu)
            presentador.mostrar_todo()
        
        return L, U, x
    
    except ValueError as e:
        print(f"❌ Error: {e}")
        return None, None, None


if __name__ == "__main__":
    print("📘 FACTORIZACIÓN LU INTERACTIVA 📘")
    print("=====================================\n")
    
    try:
        A, b = leer_sistema_por_teclado()
        print("\n✅ Sistema cargado correctamente.\n")
        
        # Resolver el sistema ingresado
        resolver_sistema_lu(A, b, mostrar_pasos=True)
        
    except ValueError as e:
        print(f"❌ Error en los datos: {e}")
    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")
