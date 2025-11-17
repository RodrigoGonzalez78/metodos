import numpy as np
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# ============================================================================
# LÓGICA DEL MÉTODO DE LAS POTENCIAS
# ============================================================================

class MetodoPotencias:
    """Clase que contiene toda la lógica del método de las potencias"""
    
    @staticmethod
    def calcular_autovalor_maximo(A, x0, tol, max_iter):
        """
        Calcula el autovalor máximo (dominante) usando el método de las potencias
        
        [Teórico] Este método converge al autovalor con el mayor valor absoluto.
        
        Returns:
            tuple: (lambda_max, vector_propio, iteraciones_info)
        """
        # Establece el vector inicial (x^(0)) necesario para el proceso iterativo.
        x = x0.copy() 
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
            
            # Prevenir división por cero si el método converge a un vector nulo
            if lambda_new == 0:
                iteraciones_info.append({
                    'iteracion': k + 1,
                    'y': y.copy(),
                    'lambda': 0.0,
                    'x_normalizado': x.copy(),
                    'x_anterior': x.copy(),
                    'error': 0.0,
                    'convergencia_cero': True
                })
                # Finaliza el bucle
                break
            
            # Normaliza el nuevo vector (x^(k+1)) para evitar el desbordamiento y preparar el siguiente paso.
            x_normalizado = y / lambda_new
            
            # Calcular error
            # Inicializa la variable de error para el criterio de parada.
            error = None
            # Calcula el error solo si ya existe una estimación anterior (k > 0).
            if k > 0:
                # Evitar división por cero en el cálculo de error
                if abs(lambda_new) < 1e-10: 
                    error = 0.0 if abs(lambda_new - lambda_old) < 1e-10 else 100.0
                else:
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
                'error': error,
                'convergencia_cero': False
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
    def calcular_autovalor_minimo(A, x0, tol, max_iter):
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
        
        # Establece el vector inicial arbitrario (x^(0)) para el método de las potencias inverso.
        x = x0.copy()
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
            
            # Prevenir división por cero
            if lambda_inv_new == 0:
                iteraciones_info.append({
                    'iteracion': k + 1,
                    'y': y.copy(),
                    'lambda_inv': 0.0,
                    'lambda_min': np.inf, # Si 1/lambda es 0, lambda es inf
                    'x_normalizado': x.copy(),
                    'x_anterior': x.copy(),
                    'error': 0.0,
                    'convergencia_cero': True
                })
                break
                
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
                if abs(lambda_min_actual) < 1e-10:
                    error = 0.0 if abs(lambda_min_actual - lambda_min_old) < 1e-10 else 100.0
                else:
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
                'error': error,
                'convergencia_cero': False
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
        # Asegurarse de que el vector sea iterable (para 1D)
        vector_iterable = np.atleast_1d(vector)
        for valor in vector_iterable:
            texto += f"{valor:8.3f} "
        texto += "│"
        return texto


# ============================================================================
# INTERFAZ GRÁFICA
# ============================================================================

class MetodoPotenciasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de las Potencias")
        self.root.geometry("950x650") 
        self.root.minsize(800, 600)  
        
        self.details_window = None
        self.detalles_text = None
        
        # Configurar estilo
        self.configurar_estilos()
        
        # Configurar grid para que sea responsive
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Crear matriz inicial
        self.crear_interfaz()
        
        # Crear matriz y vector inicial
        self.crear_entradas_dinamicas()
    
    def configurar_estilos(self):
        """Configura los estilos personalizados para los widgets"""
        style = ttk.Style()
        style.configure('Primary.TButton',
                        foreground='white',
                        background='#2196F3',
                        font=('Arial', 10, 'bold'),
                        padding=10)
        style.configure('Secondary.TButton',
                        foreground='white',
                        background='#4CAF50',
                        font=('Arial', 9),
                        padding=5)
        style.configure('Card.TFrame',
                        background='#f5f5f5',
                        relief='raised')
    
    def crear_interfaz(self,):
        """Crea toda la interfaz gráfica"""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        
        titulo = ttk.Label(main_frame, 
                             text="🔢 Método de las Potencias",
                             font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, pady=(0, 15), sticky=tk.W)
        
        # Frame de configuración de matriz
        self.crear_frame_configuracion(main_frame)
        
        # Frame para la matriz
        self.crear_frame_matriz(main_frame)
        
        # Frame para el vector inicial
        self.crear_frame_vector_inicial(main_frame)
        
        # Frame de parámetros
        self.crear_frame_parametros(main_frame)
        
        # Botón calcular
        self.crear_boton_calcular(main_frame)
    
    def crear_frame_configuracion(self, parent):
        """Crea el frame de configuración del tamaño de matriz"""
        config_frame = ttk.LabelFrame(parent, text="⚙️ Configuración", 
                                     padding="10")
        config_frame.grid(row=1, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        config_frame.columnconfigure(1, weight=1)
        
        ttk.Label(config_frame, text="Tamaño (n):").grid(
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
        
        btn_crear = tk.Button(config_frame, 
                              text="Crear Matriz y Vector",
                              command=self.crear_entradas_dinamicas,
                              bg='#4CAF50',
                              fg='white',
                              font=('Arial', 9, 'bold'),
                              relief=tk.RAISED, # <-- CORREGIDO
                              cursor='hand2',
                              padx=15,
                              pady=5)
        btn_crear.grid(row=0, column=2, padx=10)
        
        btn_crear.bind('<Enter>', lambda e: btn_crear.config(bg='#45a049'))
        btn_crear.bind('<Leave>', lambda e: btn_crear.config(bg='#4CAF50'))
    
    def validar_tamano(self, valor):
        if valor == "": return True
        try:
            n = int(valor)
            return 2 <= n <= 10
        except ValueError:
            return False
    
    def crear_frame_matriz(self, parent):
        """Crea el frame para ingresar la matriz"""
        self.matrix_frame = ttk.LabelFrame(parent, 
                                             text="📊 Ingrese la Matriz (A)", 
                                             padding="10")
        self.matrix_frame.grid(row=2, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        self.matriz_entries = []
    
    def crear_frame_vector_inicial(self, parent):
        """Crea el frame para ingresar el vector inicial"""
        self.vector_frame = ttk.LabelFrame(parent,
                                            text="🚀 Vector Inicial (x₀)",
                                            padding="10")
        self.vector_frame.grid(row=3, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        self.vector_entries = []

    def crear_frame_parametros(self, parent):
        """Crea el frame de parámetros"""
        params_frame = ttk.LabelFrame(parent, text="⚡ Parámetros de Cálculo", 
                                     padding="10")
        params_frame.grid(row=4, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        params_frame.columnconfigure(1, weight=1)
        params_frame.columnconfigure(3, weight=1)
        
        ttk.Label(params_frame, text="Tolerancia (%):").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tol_var = tk.DoubleVar(value=2.0)
        ttk.Entry(params_frame, textvariable=self.tol_var, width=15).grid(
            row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(params_frame, text="Iteraciones máx:").grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.max_iter_var = tk.IntVar(value=100)
        ttk.Entry(params_frame, textvariable=self.max_iter_var, width=15).grid(
            row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
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
                                 relief=tk.RAISED, # <-- CORREGIDO
                                 cursor='hand2',
                                 padx=30,
                                 pady=10)
        btn_calcular.grid(row=5, column=0, pady=15)
        
        btn_calcular.bind('<Enter>', lambda e: btn_calcular.config(bg='#1976D2'))
        btn_calcular.bind('<Leave>', lambda e: btn_calcular.config(bg='#2196F3'))
    
    def crear_entradas_dinamicas(self):
        """Crea la cuadrícula de entrada de la matriz y el vector"""
        try:
            n = self.size_var.get()
        except tk.TclError:
            n = 3
            self.size_var.set(3)
            
        if n < 2:
            messagebox.showwarning("Advertencia", 
                                 "El tamaño debe ser mayor o igual a 2")
            self.size_var.set(2)
            n = 2
        
        # Limpiar frame de matriz
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.matriz_entries = []
        for i in range(n):
            fila = []
            for j in range(n):
                entry = ttk.Entry(self.matrix_frame, width=8, justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                fila.append(entry)
            self.matriz_entries.append(fila)

        # Limpiar frame de vector
        for widget in self.vector_frame.winfo_children():
            widget.destroy()
        self.vector_entries = []
        for i in range(n):
            entry = ttk.Entry(self.vector_frame, width=8, justify='center')
            entry.grid(row=0, column=i, padx=2, pady=2) # En una sola fila
            entry.insert(0, "1") # Default a 1
            self.vector_entries.append(entry)
    
    def obtener_matriz(self):
        """Obtiene la matriz desde los campos de entrada"""
        n = self.size_var.get()
        A = np.zeros((n, n))
        try:
            for i in range(n):
                for j in range(n):
                    A[i][j] = float(self.matriz_entries[i][j].get())
            return A
        except ValueError:
            messagebox.showerror("Error", 
                                 "Matriz: Por favor ingrese valores numéricos válidos")
            return None

    def obtener_vector_inicial(self):
        """Obtiene el vector inicial desde los campos de entrada"""
        n = self.size_var.get()
        x0 = np.zeros(n)
        try:
            for i in range(n):
                x0[i] = float(self.vector_entries[i].get())
            
            # Validar que no sea un vector cero
            if np.all(x0 == 0):
                messagebox.showerror("Error", 
                                     "El vector inicial no puede ser un vector cero.")
                return None
            return x0
        except ValueError:
            messagebox.showerror("Error", 
                                 "Vector Inicial: Por favor ingrese valores numéricos válidos")
            return None

    def crear_ventana_detalles(self):
        """Crea o enfoca la ventana de Toplevel para los detalles"""
        if self.details_window is None or not self.details_window.winfo_exists():
            self.details_window = tk.Toplevel(self.root)
            self.details_window.title("Detalle de Iteraciones y Resultados")
            self.details_window.geometry("800x600")
            
            self.detalles_text = scrolledtext.ScrolledText(
                self.details_window,
                font=('Courier', 9),
                wrap=tk.WORD,
                bg='#f0f0f0')
            self.detalles_text.pack(expand=True, fill='both', padx=10, pady=10)
            
            # Manejar el cierre de la ventana
            self.details_window.protocol("WM_DELETE_WINDOW", self.on_details_close)
        else:
            self.details_window.lift() # Traer al frente
    
    def on_details_close(self):
        """Maneja el evento de cierre de la ventana de detalles"""
        if self.details_window:
            self.details_window.destroy()
        self.details_window = None
        self.detalles_text = None

    def mostrar_iteracion_maxima(self, A, info, target_widget):
        """Muestra los detalles de una iteración del autovalor máximo"""
        if target_widget is None: return
        
        fmt = FormateadorResultados
        
        target_widget.insert(tk.END, f"{'─'*80}\n")
        target_widget.insert(tk.END, f"ITERACIÓN {info['iteracion']}:\n")
        target_widget.insert(tk.END, f"{'─'*80}\n\n")
        
        target_widget.insert(tk.END, "A × x⁽ᵏ⁾ = y\n\n")
        target_widget.insert(tk.END, fmt.formatear_matriz(A))
        target_widget.insert(tk.END, "    ×\n")
        target_widget.insert(tk.END, fmt.formatear_vector(info['x_anterior']) + "\n")
        target_widget.insert(tk.END, "    =\n")
        target_widget.insert(tk.END, fmt.formatear_vector(info['y']) + "\n\n")
        
        if info.get('convergencia_cero', False):
            target_widget.insert(tk.END, "El método convergió a un autovalor de 0.\n\n")
            return

        target_widget.insert(tk.END, 
            f"Valor máximo (λ⁽ᵏ⁺¹⁾): {info['lambda']:.3f}\n\n")
        target_widget.insert(tk.END, 
            f"Normalización: y / {info['lambda']:.3f} = x⁽ᵏ⁺¹⁾\n")
        target_widget.insert(tk.END, 
            f"Vector normalizado: {fmt.formatear_vector(info['x_normalizado'])}\n\n")
        
        if info['error'] is not None:
            target_widget.insert(tk.END, 
                f"Error relativo: {info['error']:.2f}%\n\n")
        else:
            target_widget.insert(tk.END, 
                f"Primera estimación del valor propio: {info['lambda']:.3f}\n\n")
    
    def mostrar_iteracion_minima(self, A_inv, info, target_widget):
        """Muestra los detalles de una iteración del autovalor mínimo"""
        if target_widget is None: return
        
        fmt = FormateadorResultados
        
        target_widget.insert(tk.END, f"{'─'*80}\n")
        target_widget.insert(tk.END, f"ITERACIÓN {info['iteracion']}:\n")
        target_widget.insert(tk.END, f"{'─'*80}\n\n")
        
        target_widget.insert(tk.END, "A⁻¹ × x⁽ᵏ⁾ = y\n\n")
        target_widget.insert(tk.END, fmt.formatear_matriz(A_inv))
        target_widget.insert(tk.END, "    ×\n")
        target_widget.insert(tk.END, fmt.formatear_vector(info['x_anterior']) + "\n")
        target_widget.insert(tk.END, "    =\n")
        target_widget.insert(tk.END, fmt.formatear_vector(info['y']) + "\n\n")
        
        if info.get('convergencia_cero', False):
            target_widget.insert(tk.END, "El método inverso convergió a 1/lambda = 0.\n")
            target_widget.insert(tk.END, "Esto implica que el autovalor mínimo es infinito (matriz singular).\n\n")
            return

        target_widget.insert(tk.END, 
            f"Valor máximo: 1/λ⁽ᵏ⁺¹⁾ = {info['lambda_inv']:.3f}\n")
        target_widget.insert(tk.END, 
            f"Por lo tanto: λ⁽ᵏ⁺¹⁾ = 1/{info['lambda_inv']:.3f} = {info['lambda_min']:.3f}\n\n")
        target_widget.insert(tk.END, 
            f"Vector normalizado: {fmt.formatear_vector(info['x_normalizado'])}\n\n")
        
        if info['error'] is not None:
            target_widget.insert(tk.END, 
                f"Error relativo: {info['error']:.2f}%\n\n")
        else:
            target_widget.insert(tk.END, 
                f"Primera estimación del autovalor mínimo: {info['lambda_min']:.3f}\n\n")
    
    def calcular(self):
        """Ejecuta el cálculo del método de las potencias"""
        A = self.obtener_matriz()
        x0 = self.obtener_vector_inicial()
        
        if A is None or x0 is None:
            return
        
        # Crear o enfocar la ventana de detalles
        self.crear_ventana_detalles()
        
        # Limpiar área de texto de detalles
        self.detalles_text.delete(1.0, tk.END)
        
        tol = self.tol_var.get()
        max_iter = self.max_iter_var.get()
        fmt = FormateadorResultados
        
        # --- Salida en Ventana de Detalles (Iteraciones) ---
        
        self.detalles_text.insert(tk.END, "╔" + "═"*80 + "╗\n")
        self.detalles_text.insert(tk.END, 
            "║" + " "*25 + "MÉTODO DE LAS POTENCIAS" + " "*32 + "║\n")
        self.detalles_text.insert(tk.END, "╚" + "═"*80 + "╝\n\n")
        
        self.detalles_text.insert(tk.END, "Matriz A:\n")
        self.detalles_text.insert(tk.END, fmt.formatear_matriz(A))
        self.detalles_text.insert(tk.END, "\nVector Inicial x₀:\n")
        self.detalles_text.insert(tk.END, fmt.formatear_vector(x0) + "\n\n")
        
        # Calcular autovalor máximo
        self.detalles_text.insert(tk.END, "╔" + "═"*80 + "╗\n")
        self.detalles_text.insert(tk.END, 
            "║" + " "*15 + "AUTOVALOR MÁXIMO - MÉTODO DE LAS POTENCIAS" + " "*23 + "║\n")
        self.detalles_text.insert(tk.END, "╚" + "═"*80 + "╝\n\n")
        
        lambda_max, vec_max, iter_max = MetodoPotencias.calcular_autovalor_maximo(
            A, x0, tol, max_iter)
        
        # Mostrar iteraciones
        for info in iter_max:
            self.mostrar_iteracion_maxima(A, info, self.detalles_text)
            if info['error'] is not None and info['error'] < tol:
                self.detalles_text.insert(tk.END, 
                    f"✅ Convergencia alcanzada (Error < {tol}%) en la iteración {info['iteracion']}\n\n")
                break
        
        # --- Salida en Ventana de Detalles (Resumen Máximo) ---
        
        self.detalles_text.insert(tk.END, "╔" + "═"*80 + "╗\n")
        self.detalles_text.insert(tk.END, 
            "║" + " "*19 + "RESULTADO FINAL - AUTOVALOR MÁXIMO" + " "*24 + "║\n")
        self.detalles_text.insert(tk.END, "╚" + "═"*80 + "╝\n\n")
        self.detalles_text.insert(tk.END, 
            f"Autovalor máximo: λ = {lambda_max:.6f}\n")
        self.detalles_text.insert(tk.END, 
            f"Vector propio asociado: {fmt.formatear_vector(vec_max)}\n")
        self.detalles_text.insert(tk.END,
            f"Iteraciones realizadas: {len(iter_max)}\n\n")

        
        # Calcular autovalor mínimo si está seleccionado
        if self.calc_min_var.get():
            # --- Salida en Ventana de Detalles ---
            self.detalles_text.insert(tk.END, "\n" + "="*80 + "\n")
            self.detalles_text.insert(tk.END, "╔" + "═"*80 + "╗\n")
            self.detalles_text.insert(tk.END, 
                "║" + " "*15 + "AUTOVALOR MÍNIMO - MÉTODO DE LAS POTENCIAS INVERSO" + " "*14 + "║\n")
            self.detalles_text.insert(tk.END, "╚" + "═"*80 + "╝\n\n")
            
            resultado = MetodoPotencias.calcular_autovalor_minimo(A, x0, tol, max_iter)
            lambda_min, vec_min, iter_min, A_inv = resultado
            
            if lambda_min is None:
                self.detalles_text.insert(tk.END, 
                    "❌ La matriz no es invertible (determinante cero). No se puede aplicar el método inverso.\n")
            else:
                self.detalles_text.insert(tk.END, 
                    "Paso 1: Calcular la matriz inversa A⁻¹\n\n")
                self.detalles_text.insert(tk.END, "A⁻¹ =\n")
                self.detalles_text.insert(tk.END, fmt.formatear_matriz(A_inv))
                self.detalles_text.insert(tk.END, "\n")
                
                for info in iter_min:
                    self.mostrar_iteracion_minima(A_inv, info, self.detalles_text)
                    if info['error'] is not None and info['error'] < tol:
                        self.detalles_text.insert(tk.END, 
                            f"✅ Convergencia alcanzada (Error < {tol}%) en la iteración {info['iteracion']}\n\n")
                        break
                
                # --- Salida en Ventana de Detalles (Resumen Mínimo) ---
                self.detalles_text.insert(tk.END, "\n" + "="*80 + "\n")
                self.detalles_text.insert(tk.END, "╔" + "═"*80 + "╗\n")
                self.detalles_text.insert(tk.END, 
                    "║" + " "*19 + "RESULTADO FINAL - AUTOVALOR MÍNIMO" + " "*24 + "║\n")
                self.detalles_text.insert(tk.END, "╚" + "═"*80 + "╝\n\n")
                self.detalles_text.insert(tk.END, 
                    f"Autovalor mínimo: λ = {lambda_min:.6f}\n")
                self.detalles_text.insert(tk.END, 
                    f"Vector propio asociado: {fmt.formatear_vector(vec_min)}\n")
                self.detalles_text.insert(tk.END,
                    f"Iteraciones realizadas: {len(iter_min)}\n\n")
        
        self.detalles_text.see(tk.END)


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    root = tk.Tk()
    app = MetodoPotenciasGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()