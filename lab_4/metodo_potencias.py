import numpy as np
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# ============================================================================
# LÓGICA DEL MÉTODO DE LAS POTENCIAS (Separada de la interfaz)
# ============================================================================

class MetodoPotencias:
    """Clase que contiene toda la lógica del método de las potencias"""
    
    @staticmethod
    def calcular_autovalor_maximo(A, tol, max_iter):
        """
        Calcula el autovalor máximo (dominante) usando el método de las potencias
        
        [Teórico] Este método converge al autovalor con el mayor valor absoluto.
        
        Returns:
            tuple: (lambda_max, vector_propio, iteraciones_info)
        """
        # Define la dimensión del espacio vectorial para el cálculo de autovalores.
        n = A.shape[0]
        # Establece el vector inicial arbitrario (x^(0)) necesario para el proceso iterativo.
        x = np.ones(n)
        # Inicializa el autovalor previo para poder calcular la convergencia en el siguiente paso.
        lambda_old = 0.0
        # Almacena el historial de las iteraciones para mostrar la traza completa de la convergencia.
        iteraciones_info = []
        
        # Inicia el proceso iterativo, buscando la convergencia del autovalor dominante.
        for k in range(max_iter):
            # Realiza la potencia: la multiplicación (y = A * x^(k)) que acerca y al vector propio dominante.
            y = np.dot(A, x)
            # Estima el autovalor actual (λ^(k+1)) tomando la norma infinito del vector resultante (y).
            lambda_new = np.max(np.abs(y))
            # Normaliza el nuevo vector (x^(k+1)) para evitar el desbordamiento y preparar el siguiente paso.
            x_normalizado = y / lambda_new
            
            # Calcular error
            # Inicializa la variable de error para el criterio de parada.
            error = None
            # Calcula el error solo si ya existe una estimación anterior (k > 0).
            if k > 0:
                # Mide el error relativo porcentual entre las estimaciones del autovalor para juzgar la convergencia.
                error = abs(lambda_new - lambda_old) / abs(lambda_new) * 100
            
            # Guardar información de la iteración
            # Guarda todos los resultados y vectores de la iteración para el reporte final.
            iteraciones_info.append({
                'iteracion': k + 1,
                'y': y.copy(),
                'lambda': lambda_new,
                'x_normalizado': x_normalizado.copy(),
                'x_anterior': x.copy(),
                'error': error
            })
            
            # Verificar convergencia
            # Detiene el proceso si el error relativo cae por debajo de la tolerancia definida (convergencia).
            if k > 0 and error < tol:
                # Finaliza el bucle al alcanzar la precisión deseada.
                break
            
            # El autovalor actual pasa a ser el anterior para la siguiente comparación de error.
            lambda_old = lambda_new
            # El vector normalizado se convierte en el vector inicial (x^(k+1)) de la próxima iteración.
            x = x_normalizado
        
        # Retorna la mejor estimación del autovalor dominante y su vector propio asociado.
        return lambda_new, x, iteraciones_info
    
    @staticmethod
    def calcular_autovalor_minimo(A, tol, max_iter):
        """
        Calcula el autovalor mínimo (de menor magnitud) usando el método de las potencias inverso
        
        [Teórico] Consiste en aplicar el método de las potencias a la matriz inversa (A⁻¹), 
        cuyos autovalores son los inversos (1/λ) de A. El máximo de A⁻¹ es 1/λ_min.
        
        Returns:
            tuple: (lambda_min, vector_propio, iteraciones_info, A_inv) o (None, None, None, None)
        """
        try:
            # Calcula la matriz inversa (A⁻¹), cuyos autovalores son los inversos (1/λ).
            A_inv = np.linalg.inv(A)
        # Maneja el error si la matriz A es singular (determinante cero).
        except np.linalg.LinAlgError:
            # Devuelve error si la matriz no es invertible, impidiendo el método inverso.
            return None, None, None, None
        
        # Define la dimensión de la matriz para los cálculos vectoriales.
        n = A.shape[0]
        # Establece el vector inicial arbitrario (x^(0)) para el método de las potencias inverso.
        x = np.ones(n)
        # Inicializa la estimación previa del autovalor de A⁻¹ (1/λ) para el cálculo de error.
        lambda_inv_old = 0.0
        # Almacena el historial de las iteraciones para trazar la convergencia de λ_min.
        iteraciones_info = []
        
        # Inicia el proceso iterativo aplicando el método de las potencias a la matriz inversa.
        for k in range(max_iter):
            # Realiza la multiplicación (y = A⁻¹ * x^(k)), buscando el autovalor dominante de A⁻¹.
            y = np.dot(A_inv, x)
            # Estima el autovalor dominante de A⁻¹, que es el inverso del autovalor mínimo de A (1/λ_min).
            lambda_inv_new = np.max(np.abs(y))
            # Normaliza el vector para obtener la nueva estimación del vector propio asociado a λ_min.
            x_normalizado = y / lambda_inv_new
            
            # Calcula la estimación actual del autovalor mínimo de A invirtiendo el valor obtenido de A⁻¹.
            lambda_min_actual = 1 / lambda_inv_new
            
            # Calcular error
            # Inicializa el error para el criterio de convergencia.
            error = None
            # Prepara el cálculo del error relativo solo a partir de la segunda iteración.
            if k > 0:
                # Recupera el autovalor mínimo anterior de A para calcular el error de convergencia.
                lambda_min_old = 1 / lambda_inv_old
                # Mide la precisión de la estimación de λ_min comparándolo con el valor de la iteración anterior.
                error = abs(lambda_min_actual - lambda_min_old) / abs(lambda_min_actual) * 100
            
            # Guardar información de la iteración
            # Guarda los resultados clave (λ_inv y λ_min) para trazar la historia de la convergencia.
            iteraciones_info.append({
                'iteracion': k + 1,
                'y': y.copy(),
                'lambda_inv': lambda_inv_new,
                'lambda_min': lambda_min_actual,
                'x_normalizado': x_normalizado.copy(),
                'x_anterior': x.copy(),
                'error': error
            })
            
            # Verificar convergencia
            # Detiene el proceso si el error relativo de λ_min es menor que la tolerancia.
            if k > 0 and error < tol:
                # Finaliza el bucle al alcanzar la precisión deseada.
                break
            
            # El autovalor inverso actual pasa a ser el anterior para la siguiente comparación de error.
            lambda_inv_old = lambda_inv_new
            # El vector normalizado se convierte en el vector inicial (x^(k+1)) para la próxima iteración.
            x = x_normalizado
        
        # Calcula el resultado final del autovalor mínimo a partir de la última estimación inversa.
        lambda_min = 1 / lambda_inv_new
        
        # Retorna la mejor estimación del autovalor mínimo y su vector propio asociado.
        return lambda_min, x, iteraciones_info, A_inv


# ============================================================================
# UTILIDADES DE FORMATEO
# ============================================================================

class FormateadorResultados:
    """Clase para formatear matrices y vectores para una presentación amigable en texto"""
    
    @staticmethod
    def formatear_matriz(matriz):
        # Formatea la matriz NumPy como texto para su visualización con 3 decimales.
        texto = ""
        for fila in matriz:
            texto += "│ "
            for valor in fila:
                texto += f"{valor:8.3f} "
            texto += "│\n"
        return texto
    
    @staticmethod
    def formatear_vector(vector):
        # Formatea el vector NumPy como texto para su visualización con 3 decimales.
        texto = "│ "
        for valor in vector:
            texto += f"{valor:8.3f} "
        texto += "│"
        return texto


# ============================================================================
# INTERFAZ GRÁFICA (Sin cambios en la lógica de GUI)
# ============================================================================

class MetodoPotenciasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de las Potencias")
        self.root.geometry("950x750")
        self.root.minsize(800, 600)
        
        # Configurar estilo
        self.configurar_estilos()
        
        # Configurar grid para que sea responsive
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Frame principal con scroll
        self.crear_interfaz()
        
        # Crear matriz inicial
        self.crear_matriz()
    
    def configurar_estilos(self):
        """Configura los estilos personalizados para los widgets"""
        style = ttk.Style()
        
        # Botón principal (Calcular)
        style.configure('Primary.TButton',
                        foreground='white',
                        background='#2196F3',
                        font=('Arial', 10, 'bold'),
                        padding=10)
        
        # Botón secundario (Crear Matriz)
        style.configure('Secondary.TButton',
                        foreground='white',
                        background='#4CAF50',
                        font=('Arial', 9),
                        padding=5)
        
        # Frames con bordes
        style.configure('Card.TFrame',
                        background='#f5f5f5',
                        relief='raised')
    
    def crear_interfaz(self,):
        """Crea toda la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, 
                             text="🔢 Método de las Potencias",
                             font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, pady=(0, 15))
        
        # Frame de configuración de matriz
        self.crear_frame_configuracion(main_frame)
        
        # Frame para la matriz
        self.crear_frame_matriz(main_frame)
        
        # Frame de parámetros
        self.crear_frame_parametros(main_frame)
        
        # Botón calcular
        self.crear_boton_calcular(main_frame)
        
        # Área de resultados
        self.crear_area_resultados(main_frame)
    
    def crear_frame_configuracion(self, parent):
        """Crea el frame de configuración del tamaño de matriz"""
        config_frame = ttk.LabelFrame(parent, text="⚙️ Configuración de Matriz", 
                                     padding="10")
        config_frame.grid(row=1, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        config_frame.columnconfigure(1, weight=1)
        
        ttk.Label(config_frame, text="Tamaño de la matriz (n × n):").grid(
            row=0, column=0, sticky=tk.W, padx=5)
        
        self.size_var = tk.IntVar(value=3)
        size_spinbox = ttk.Spinbox(config_frame, 
                                     from_=2, 
                                     to=10, 
                                     textvariable=self.size_var, 
                                     width=10,
                                     validate='key',
                                     validatecommand=(self.root.register(self.validar_tamano), '%P'))
        size_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Botón con color
        btn_crear = tk.Button(config_frame, 
                              text="Crear Matriz",
                              command=self.crear_matriz,
                              bg='#4CAF50',
                              fg='white',
                              font=('Arial', 9, 'bold'),
                              relief=tk.RAISED,
                              cursor='hand2',
                              padx=15,
                              pady=5)
        btn_crear.grid(row=0, column=2, padx=10)
        
        # Efectos hover
        btn_crear.bind('<Enter>', lambda e: btn_crear.config(bg='#45a049'))
        btn_crear.bind('<Leave>', lambda e: btn_crear.config(bg='#4CAF50'))
    
    def validar_tamano(self, valor):
        """Valida que el tamaño de la matriz sea >= 2"""
        if valor == "":
            return True
        try:
            n = int(valor)
            return 2 <= n <= 10
        except ValueError:
            return False
    
    def crear_frame_matriz(self, parent):
        """Crea el frame para ingresar la matriz"""
        self.matrix_frame = ttk.LabelFrame(parent, 
                                             text="📊 Ingrese los elementos de la matriz", 
                                             padding="10")
        self.matrix_frame.grid(row=2, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        self.entries = []
    
    def crear_frame_parametros(self, parent):
        """Crea el frame de parámetros"""
        params_frame = ttk.LabelFrame(parent, text="⚡ Parámetros de Cálculo", 
                                     padding="10")
        params_frame.grid(row=3, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        params_frame.columnconfigure(1, weight=1)
        params_frame.columnconfigure(3, weight=1)
        
        # Tolerancia
        ttk.Label(params_frame, text="Tolerancia (%):").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tol_var = tk.DoubleVar(value=2.0)
        ttk.Entry(params_frame, textvariable=self.tol_var, width=15).grid(
            row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Iteraciones máximas
        ttk.Label(params_frame, text="Iteraciones máx:").grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.max_iter_var = tk.IntVar(value=100)
        ttk.Entry(params_frame, textvariable=self.max_iter_var, width=15).grid(
            row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Checkbox
        self.calc_min_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(params_frame, 
                        text="✓ Calcular también autovalor mínimo", 
                        variable=self.calc_min_var).grid(
            row=1, column=0, columnspan=4, pady=5, sticky=tk.W)
    
    def crear_boton_calcular(self, parent):
        """Crea el botón de calcular con estilo"""
        btn_calcular = tk.Button(parent,
                                 text="🚀 CALCULAR",
                                 command=self.calcular,
                                 bg='#2196F3',
                                 fg='white',
                                 font=('Arial', 12, 'bold'),
                                 relief=tk.RAISED,
                                 cursor='hand2',
                                 padx=30,
                                 pady=10)
        btn_calcular.grid(row=4, column=0, pady=15)
        
        # Efectos hover
        btn_calcular.bind('<Enter>', lambda e: btn_calcular.config(bg='#1976D2'))
        btn_calcular.bind('<Leave>', lambda e: btn_calcular.config(bg='#2196F3'))
    
    def crear_area_resultados(self, parent):
        """Crea el área de resultados"""
        ttk.Label(parent, text="📋 Resultados:", 
                  font=('Arial', 10, 'bold')).grid(row=5, column=0, sticky=tk.W)
        
        self.resultado_text = scrolledtext.ScrolledText(
            parent, 
            height=20, 
            width=110,
            font=('Courier', 9),
            wrap=tk.WORD,
            bg='#f9f9f9')
        self.resultado_text.grid(row=6, column=0, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def crear_matriz(self):
        """Crea la cuadrícula de entrada de la matriz"""
        # Validar tamaño
        n = self.size_var.get()
        if n < 2:
            messagebox.showwarning("Advertencia", 
                                 "El tamaño de la matriz debe ser mayor o igual a 2")
            self.size_var.set(2)
            return
        
        # Limpiar frame
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        
        self.entries = []
        
        for i in range(n):
            fila = []
            for j in range(n):
                entry = ttk.Entry(self.matrix_frame, width=8, justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                fila.append(entry)
            self.entries.append(fila)
    
    def obtener_matriz(self):
        """Obtiene la matriz desde los campos de entrada"""
        n = self.size_var.get()
        A = np.zeros((n, n))
        try:
            for i in range(n):
                for j in range(n):
                    A[i][j] = float(self.entries[i][j].get())
            return A
        except ValueError:
            messagebox.showerror("Error", 
                                 "Por favor ingrese valores numéricos válidos")
            return None
    
    def mostrar_iteracion_maxima(self, A, info):
        """Muestra los detalles de una iteración del autovalor máximo"""
        fmt = FormateadorResultados
        
        self.resultado_text.insert(tk.END, f"{'─'*80}\n")
        self.resultado_text.insert(tk.END, f"ITERACIÓN {info['iteracion']}:\n")
        self.resultado_text.insert(tk.END, f"{'─'*80}\n\n")
        
        self.resultado_text.insert(tk.END, "A × x⁽ᵏ⁾ = y\n\n")
        self.resultado_text.insert(tk.END, fmt.formatear_matriz(A))
        self.resultado_text.insert(tk.END, "    ×\n")
        self.resultado_text.insert(tk.END, fmt.formatear_vector(info['x_anterior']) + "\n")
        self.resultado_text.insert(tk.END, "    =\n")
        self.resultado_text.insert(tk.END, fmt.formatear_vector(info['y']) + "\n\n")
        
        self.resultado_text.insert(tk.END, 
            f"Valor máximo (λ⁽ᵏ⁺¹⁾): {info['lambda']:.3f}\n\n")
        self.resultado_text.insert(tk.END, 
            f"Normalización: y / {info['lambda']:.3f} = x⁽ᵏ⁺¹⁾\n")
        self.resultado_text.insert(tk.END, 
            f"Vector normalizado: {fmt.formatear_vector(info['x_normalizado'])}\n\n")
        
        if info['error'] is not None:
            self.resultado_text.insert(tk.END, 
                f"Error relativo: {info['error']:.2f}%\n\n")
        else:
            self.resultado_text.insert(tk.END, 
                f"Primera estimación del valor propio: {info['lambda']:.3f}\n\n")
    
    def mostrar_iteracion_minima(self, A_inv, info):
        """Muestra los detalles de una iteración del autovalor mínimo"""
        fmt = FormateadorResultados
        
        self.resultado_text.insert(tk.END, f"{'─'*80}\n")
        self.resultado_text.insert(tk.END, f"ITERACIÓN {info['iteracion']}:\n")
        self.resultado_text.insert(tk.END, f"{'─'*80}\n\n")
        
        self.resultado_text.insert(tk.END, "A⁻¹ × x⁽ᵏ⁾ = y\n\n")
        self.resultado_text.insert(tk.END, fmt.formatear_matriz(A_inv))
        self.resultado_text.insert(tk.END, "    ×\n")
        self.resultado_text.insert(tk.END, fmt.formatear_vector(info['x_anterior']) + "\n")
        self.resultado_text.insert(tk.END, "    =\n")
        self.resultado_text.insert(tk.END, fmt.formatear_vector(info['y']) + "\n\n")
        
        self.resultado_text.insert(tk.END, 
            f"Valor máximo: 1/λ⁽ᵏ⁺¹⁾ = {info['lambda_inv']:.3f}\n")
        self.resultado_text.insert(tk.END, 
            f"Por lo tanto: λ⁽ᵏ⁺¹⁾ = 1/{info['lambda_inv']:.3f} = {info['lambda_min']:.3f}\n\n")
        self.resultado_text.insert(tk.END, 
            f"Vector normalizado: {fmt.formatear_vector(info['x_normalizado'])}\n\n")
        
        if info['error'] is not None:
            self.resultado_text.insert(tk.END, 
                f"Error relativo: {info['error']:.2f}%\n\n")
        else:
            self.resultado_text.insert(tk.END, 
                f"Primera estimación del autovalor mínimo: {info['lambda_min']:.3f}\n\n")
    
    def calcular(self):
        """Ejecuta el cálculo del método de las potencias"""
        A = self.obtener_matriz()
        if A is None:
            return
        
        # Validar que el tamaño sea >= 2
        if self.size_var.get() < 2:
            messagebox.showerror("Error", 
                                 "El tamaño de la matriz debe ser mayor o igual a 2")
            return
        
        self.resultado_text.delete(1.0, tk.END)
        
        tol = self.tol_var.get()
        max_iter = self.max_iter_var.get()
        fmt = FormateadorResultados
        
        # Encabezado
        self.resultado_text.insert(tk.END, "╔" + "═"*80 + "╗\n")
        self.resultado_text.insert(tk.END, 
            "║" + " "*25 + "MÉTODO DE LAS POTENCIAS" + " "*32 + "║\n")
        self.resultado_text.insert(tk.END, "╚" + "═"*80 + "╝\n\n")
        
        self.resultado_text.insert(tk.END, "Matriz A:\n")
        self.resultado_text.insert(tk.END, fmt.formatear_matriz(A))
        self.resultado_text.insert(tk.END, "\n")
        
        # Calcular autovalor máximo
        self.resultado_text.insert(tk.END, "╔" + "═"*80 + "╗\n")
        self.resultado_text.insert(tk.END, 
            "║" + " "*15 + "AUTOVALOR MÁXIMO - MÉTODO DE LAS POTENCIAS" + " "*23 + "║\n")
        self.resultado_text.insert(tk.END, "╚" + "═"*80 + "╝\n\n")
        
        lambda_max, vec_max, iter_max = MetodoPotencias.calcular_autovalor_maximo(
            A, tol, max_iter)
        
        # Mostrar iteraciones
        for info in iter_max:
            self.mostrar_iteracion_maxima(A, info)
            if info['error'] is not None and info['error'] < tol:
                self.resultado_text.insert(tk.END, 
                    f"✅ Convergencia alcanzada (Error < {tol}%) en la iteración {info['iteracion']}\n\n")
                break
        
        # Resultado final máximo
        self.resultado_text.insert(tk.END, "╔" + "═"*80 + "╗\n")
        self.resultado_text.insert(tk.END, 
            "║" + " "*28 + "RESULTADO FINAL" + " "*37 + "║\n")
        self.resultado_text.insert(tk.END, "╚" + "═"*80 + "╝\n\n")
        self.resultado_text.insert(tk.END, 
            f"Autovalor máximo: λ = {lambda_max:.3f}\n")
        self.resultado_text.insert(tk.END, 
            f"Vector propio asociado: {fmt.formatear_vector(vec_max)}\n\n")
        
        # Calcular autovalor mínimo si está seleccionado
        if self.calc_min_var.get():
            self.resultado_text.insert(tk.END, "\n" + "="*80 + "\n")
            self.resultado_text.insert(tk.END, "╔" + "═"*80 + "╗\n")
            self.resultado_text.insert(tk.END, 
                "║" + " "*15 + "AUTOVALOR MÍNIMO - MÉTODO DE LAS POTENCIAS INVERSO" + " "*14 + "║\n")
            self.resultado_text.insert(tk.END, "╚" + "═"*80 + "╝\n\n")
            
            resultado = MetodoPotencias.calcular_autovalor_minimo(A, tol, max_iter)
            lambda_min, vec_min, iter_min, A_inv = resultado
            
            if lambda_min is None:
                self.resultado_text.insert(tk.END, 
                    "❌ La matriz no es invertible (determinante cero). No se puede aplicar el método inverso.\n")
            else:
                self.resultado_text.insert(tk.END, 
                    "Paso 1: Calcular la matriz inversa A⁻¹\n\n")
                self.resultado_text.insert(tk.END, "A⁻¹ =\n")
                self.resultado_text.insert(tk.END, fmt.formatear_matriz(A_inv))
                self.resultado_text.insert(tk.END, "\n")
                
                # Mostrar iteraciones
                for info in iter_min:
                    self.mostrar_iteracion_minima(A_inv, info)
                    if info['error'] is not None and info['error'] < tol:
                        self.resultado_text.insert(tk.END, 
                            f"✅ Convergencia alcanzada (Error < {tol}%) en la iteración {info['iteracion']}\n\n")
                        break
                
                # Resultado final mínimo
                self.resultado_text.insert(tk.END, "╔" + "═"*80 + "╗\n")
                self.resultado_text.insert(tk.END, 
                    "║" + " "*28 + "RESULTADO FINAL" + " "*37 + "║\n")
                self.resultado_text.insert(tk.END, "╚" + "═"*80 + "╝\n\n")
                self.resultado_text.insert(tk.END, 
                    f"Autovalor mínimo: λ = {lambda_min:.3f}\n")
                self.resultado_text.insert(tk.END, 
                    f"Vector propio asociado: {fmt.formatear_vector(vec_min)}\n\n")
        
        self.resultado_text.see(tk.END)


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    root = tk.Tk()
    app = MetodoPotenciasGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()