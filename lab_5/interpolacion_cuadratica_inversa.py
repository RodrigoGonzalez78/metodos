import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math

# ===========================
# LÓGICA DEL ALGORITMO
# ===========================

class AlgoritmoInterpolacion:
    """Contiene la lógica del método de interpolación cuadrática inversa."""

    @staticmethod
    def encontrar_intervalo(y_vals, y_buscado):
        """
        Busca el intervalo donde se encuentra el valor y_buscado.
        Para interpolación cuadrática, necesitamos 3 puntos consecutivos.

        Args:
            y_vals (list): Lista de valores de Y conocidos.
            y_buscado (float): Valor de Y para el cual se quiere interpolar X.

        Returns:
            int: Índice del primer punto del intervalo (necesitamos i, i+1, i+2).
        """
        # Se asume que los datos están ordenados por X, lo cual es manejado en la interfaz.
        
        y_vals_list = list(y_vals)

        # Manejo de Extrapolación: Si el valor está fuera del rango min/max,
        # se toma el primer o último intervalo de 3 puntos.
        
        if not y_vals_list:
             return 0
             
        y_min_total = min(y_vals_list)
        y_max_total = max(y_vals_list)
        
        if y_buscado < y_min_total or y_buscado > y_max_total:
            if len(y_vals_list) >= 3:
                # Extrapolación: Elige el intervalo más cercano (inicio o final)
                if abs(y_buscado - y_vals_list[0]) < abs(y_buscado - y_vals_list[-1]):
                     return 0 
                else:
                     return len(y_vals_list) - 3
            else:
                 return 0 # No hay suficientes puntos
        
        # Búsqueda de Intervalo (Interpolación)
        for i in range(len(y_vals_list) - 2):
            # Encontrar el rango Y de los tres puntos consecutivos
            y_sub_vals = [y_vals_list[i], y_vals_list[i+1], y_vals_list[i+2]]
            y_min = min(y_sub_vals)
            y_max = max(y_sub_vals)
            
            # Verificar si y_buscado está dentro del rango Y de estos 3 puntos
            if y_min <= y_buscado <= y_max:
                return i
        return 0 # En caso de que no se encuentre un intervalo exacto (debería ser raro si se pasó la validación de rango)

    @staticmethod
    def calcular_interpolacion(x_vals, y_vals, y_buscado):
        """
        Calcula el valor de X correspondiente a un Y dado
        mediante interpolación cuadrática inversa.
        
        Args:
            x_vals (list): Valores de X conocidos.
            y_vals (list): Valores de Y conocidos.
            y_buscado (float): Valor de Y que se desea interpolar.

        Returns:
            dict: Resultados y valores intermedios del cálculo.
        """
        # Validar que haya al menos 3 puntos
        if len(x_vals) < 3 or len(y_vals) < 3:
             raise ValueError("Se requieren al menos 3 puntos para la interpolación cuadrática inversa.")

        # Encontrar el intervalo de 3 puntos que contiene y_buscado
        i = AlgoritmoInterpolacion.encontrar_intervalo(y_vals, y_buscado)

        # Asegurar que el índice no exceda los límites de la lista
        if i < 0 or i > len(x_vals) - 3:
            i = 0 

        # Extraer los tres puntos necesarios
        x0, x1, x2 = x_vals[i], x_vals[i+1], x_vals[i+2]
        y0, y1, y2 = y_vals[i], y_vals[i+1], y_vals[i+2]

        # Calcular el espaciamiento h
        h = x1 - x0
        
        # Usar tolerancia para cero
        if abs(h) < 1e-9: 
            raise ZeroDivisionError("Los puntos X seleccionados son idénticos o están demasiado cerca.")

        # Calcular las diferencias divididas
        delta_y0 = y1 - y0
        delta2_y0 = y2 - 2*y1 + y0
        diferencia_y = y_buscado - y0

        # Coeficientes de la ecuación cuadrática ax² + bu + c = 0 (donde u = x - x₀)
        # La ecuación es: y = y₀ + (Δy₀/h)*u + (Δ²y₀/2h²)*u*(u - h)
        # Reordenando para y - y_buscado = 0, y haciendo y = y_buscado
        
        # Coeficiente de u² (a)
        a = delta2_y0 / (2 * h * h)
        
        # Coeficiente de u (b)
        b = delta_y0 / h - (delta2_y0 / (2 * h))
        
        # Término independiente (c)
        c = -diferencia_y
        
        # Inicialización de resultados
        x_interpolado = float('nan')
        x_sol1 = float('nan')
        x_sol2 = float('nan')
        discriminante = float('nan')

        # Caso lineal si a es cero (o muy cercano a cero)
        if abs(a) < 1e-9:
            discriminante = 0 # Para el reporte
            if abs(b) < 1e-9:
                if abs(c) < 1e-9:
                    x_interpolado = x0
                else:
                    raise ValueError("El valor buscado (Y) no es alcanzable con los puntos seleccionados.")
            else:
                # Ecuación lineal: bu + c = 0 => u = -c / b
                u1 = -c / b
                x_sol1 = x0 + u1
                x_interpolado = x_sol1
        else:
            # Caso cuadrático
            discriminante = b * b - 4 * a * c
            
            if discriminante < 0:
                raise ValueError("No existe solución real (discriminante negativo)")
            
            sqrt_discriminante = math.sqrt(discriminante)
            
            # Calcular ambas soluciones posibles para u
            u1 = (-b + sqrt_discriminante) / (2 * a)
            u2 = (-b - sqrt_discriminante) / (2 * a)
            
            # x = x₀ + u
            x_sol1 = x0 + u1
            x_sol2 = x0 + u2
            
            # Seleccionar la solución que esté dentro o más cercana al intervalo [x₀, x₂]
            x_min_interv, x_max_interv = min(x0, x2), max(x0, x2)
            
            is_sol1_in = (x_min_interv <= x_sol1 <= x_max_interv)
            is_sol2_in = (x_min_interv <= x_sol2 <= x_max_interv)

            if is_sol1_in and is_sol2_in:
                # Si ambas están en el intervalo, seleccionar la más cercana al punto medio (x1)
                if abs(x_sol1 - x1) < abs(x_sol2 - x1):
                    x_interpolado = x_sol1
                else:
                    x_interpolado = x_sol2
            elif is_sol1_in:
                x_interpolado = x_sol1
            elif is_sol2_in:
                x_interpolado = x_sol2
            else:
                # Si ninguna está en el intervalo, tomar la más cercana a x1
                if abs(x_sol1 - x1) < abs(x_sol2 - x1):
                    x_interpolado = x_sol1
                else:
                    x_interpolado = x_sol2

        return {
            'indice': i,
            'x0': x0, 'x1': x1, 'x2': x2,
            'y0': y0, 'y1': y1, 'y2': y2,
            'y_buscado': y_buscado,
            'h': h,
            'delta_y0': delta_y0,
            'delta2_y0': delta2_y0,
            'diferencia_y': diferencia_y,
            'coef_a': a,
            'coef_b': b,
            'coef_c': c,
            'discriminante': discriminante,
            'x_sol1': x_sol1,
            'x_sol2': x_sol2,
            'x_resultado': x_interpolado
        }

    @staticmethod
    def generar_reporte(datos):
        """
        Genera un texto con el desarrollo paso a paso de la interpolación cuadrática.

        Args:
            datos (dict): Resultados devueltos por calcular_interpolacion().

        Returns:
            str: Reporte formateado con todos los cálculos.
        """
        def format_val(val):
            return f"{val:.8f}" if not math.isnan(val) else "N/A"

        resultado = f"\n{'='*70}\n"
        resultado += "INTERPOLACIÓN INVERSA CUADRÁTICA\n"
        resultado += f"{'='*70}\n\n"
        resultado += f"Puntos seleccionados para la interpolación (Índice {datos['indice']}):\n"
        resultado += f"  P0: (x0 = {format_val(datos['x0'])}, y0 = {format_val(datos['y0'])})\n"
        resultado += f"  P1: (x1 = {format_val(datos['x1'])}, y1 = {format_val(datos['y1'])})\n"
        resultado += f"  P2: (x2 = {format_val(datos['x2'])}, y2 = {format_val(datos['y2'])})\n\n"
        resultado += f"Valor buscado: y = {format_val(datos['y_buscado'])}\n\n"
        resultado += f"Cálculos intermedios:\n"
        resultado += f"  h = x₁ - x₀ = {format_val(datos['h'])}\n"
        resultado += f"  Δy₀ = y₁ - y₀ = {format_val(datos['delta_y0'])}\n"
        resultado += f"  Δ²y₀ = y₂ - 2y₁ + y₀ = {format_val(datos['delta2_y0'])}\n"
        resultado += f"  y - y₀ = {format_val(datos['diferencia_y'])}\n\n"
        resultado += f"Ecuación cuadrática (au² + bu + c = 0, donde u = x - x₀):\n"
        resultado += f"  a = Δ²y₀ / (2h²) = {format_val(datos['coef_a'])}\n"
        resultado += f"  b = (Δy₀/h) - (Δ²y₀/2h) = {format_val(datos['coef_b'])}\n"
        resultado += f"  c = -(y - y₀) = {format_val(datos['coef_c'])}\n"
        
        resultado += f"  Discriminante (D = b² - 4ac) = {format_val(datos['discriminante'])}\n\n"
        
        resultado += f"Soluciones (u = (-b ± √D) / 2a):\n"
        resultado += f"  u₁: {format_val(datos['x_sol1'] - datos['x0'])} => x₁ = x₀ + u₁ = {format_val(datos['x_sol1'])}\n"
        resultado += f"  u₂: {format_val(datos['x_sol2'] - datos['x0'])} => x₂ = x₀ + u₂ = {format_val(datos['x_sol2'])}\n\n"
        
        resultado += f"{'='*70}\nRESULTADO FINAL SELECCIONADO: x = {format_val(datos['x_resultado'])}\n{'='*70}\n"
        return resultado

# ===========================
# INTERFAZ GRÁFICA
# ===========================

class InterpolacionInversa:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpolación Inversa Cuadrática")
        self.root.geometry("850x750") # Tamaño inicial ajustado
        self.root.configure(bg='#f0f0f0')
        
        # Configuración de Responsividad de la ventana principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Listas para almacenar los datos
        self.x_vals = []
        self.y_vals = []
        
        # Variables para los labels de valores intermedios
        self.labels_valores = {}
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Usamos un Frame principal para contener todo y que sea el que se expande
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky='nsew')
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Hacer que la fila de la tabla se expanda más
        main_frame.grid_rowconfigure(2, weight=1) 

        # Título
        titulo = tk.Label(main_frame, text="Interpolación Inversa Cuadrática", 
                          font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#1E88E5')
        titulo.grid(row=0, column=0, pady=(0, 15), sticky='ew')
        
        # Frame 1: Ingreso de Datos (Row 1)
        frame_entrada = tk.LabelFrame(main_frame, text="Ingreso de Datos (Pares x, y)", 
                                      font=('Arial', 11, 'bold'), bg='#f0f0f0', padx=10, pady=5)
        frame_entrada.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        
        # Configuración de pesos para el frame de entrada
        frame_entrada.grid_columnconfigure(1, weight=2) # Columna del input X
        frame_entrada.grid_columnconfigure(3, weight=2) # Columna del input Y
        frame_entrada.grid_columnconfigure(0, weight=1)
        frame_entrada.grid_columnconfigure(2, weight=1)
        frame_entrada.grid_columnconfigure(4, weight=1)
        frame_entrada.grid_columnconfigure(5, weight=1)
        frame_entrada.grid_columnconfigure(6, weight=1)
        
        # Campos para ingresar x e y
        tk.Label(frame_entrada, text="Valor X:", font=('Arial', 10), 
                 bg='#f0f0f0').grid(row=0, column=0, padx=(0, 5), pady=5, sticky='w')
        self.entry_x = tk.Entry(frame_entrada, font=('Arial', 10), width=15)
        self.entry_x.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Label(frame_entrada, text="Valor Y:", font=('Arial', 10), 
                 bg='#f0f0f0').grid(row=0, column=2, padx=(10, 5), pady=5, sticky='w')
        self.entry_y_dato = tk.Entry(frame_entrada, font=('Arial', 10), width=15)
        self.entry_y_dato.grid(row=0, column=3, padx=5, pady=5, sticky='ew')
        
        # Botones de acción de datos
        btn_agregar = tk.Button(frame_entrada, text="Agregar Punto", 
                                command=self.agregar_punto,
                                font=('Arial', 9, 'bold'), bg='#4CAF50', fg='white')
        btn_agregar.grid(row=0, column=4, padx=(10, 5), pady=5, sticky='ew')
        
        btn_cargar_ejemplo = tk.Button(frame_entrada, text="Cargar Ejemplo", 
                                        command=self.cargar_ejemplo,
                                        font=('Arial', 9), bg='#9C27B0', fg='white')
        btn_cargar_ejemplo.grid(row=0, column=5, padx=5, pady=5, sticky='ew')
        
        btn_limpiar_datos = tk.Button(frame_entrada, text="Limpiar Datos", 
                                       command=self.limpiar_datos,
                                       font=('Arial', 9), bg='#F44336', fg='white')
        btn_limpiar_datos.grid(row=0, column=6, padx=(5, 0), pady=5, sticky='ew')
        
        # Frame 2: Datos Ingresados y Búsqueda (Row 2, expandible)
        frame_datos_busqueda = ttk.Frame(main_frame)
        frame_datos_busqueda.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        frame_datos_busqueda.grid_columnconfigure(0, weight=1) # Tabla (Izquierda)
        frame_datos_busqueda.grid_columnconfigure(1, weight=1) # Búsqueda/Resultados (Derecha)
        frame_datos_busqueda.grid_rowconfigure(0, weight=1)
        
        # Sub-Frame Izquierdo: Tabla de Datos
        frame_tabla = tk.LabelFrame(frame_datos_busqueda, text="Datos Ingresados", 
                                    font=('Arial', 11, 'bold'), bg='#f0f0f0', padx=10, pady=5)
        frame_tabla.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        frame_tabla.grid_columnconfigure(0, weight=1)
        frame_tabla.grid_rowconfigure(0, weight=1) # Hacer que la tabla se expanda
        
        # Treeview para mostrar los datos
        columns = ('index', 'x', 'y')
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show='headings', height=6)
        
        self.tree.heading('index', text='#')
        self.tree.heading('x', text='X')
        self.tree.heading('y', text='Y')
        
        self.tree.column('index', width=50, stretch=tk.NO, anchor='center')
        self.tree.column('x', minwidth=100, anchor='center', stretch=tk.YES)
        self.tree.column('y', minwidth=100, anchor='center', stretch=tk.YES)
        
        self.tree.grid(row=0, column=0, sticky='nsew', padx=(0, 5), pady=5)
        
        # Scrollbar para la tabla
        scrollbar_tabla = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tree.yview)
        scrollbar_tabla.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar_tabla.set)
        
        # Botón para eliminar punto seleccionado (debajo de la tabla)
        btn_eliminar = tk.Button(frame_tabla, text="Eliminar Seleccionado", 
                                 command=self.eliminar_punto,
                                 font=('Arial', 9), bg='#FF5722', fg='white')
        btn_eliminar.grid(row=1, column=0, columnspan=2, pady=5, sticky='ew')
        
        # Sub-Frame Derecho: Búsqueda, Botones y Resultado Rápido
        frame_resultados_cont = ttk.Frame(frame_datos_busqueda)
        frame_resultados_cont.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        frame_resultados_cont.grid_columnconfigure(0, weight=1)

        # Frame para valor a buscar
        frame_buscar = tk.LabelFrame(frame_resultados_cont, text="Valor Y a Interpolar", 
                                     font=('Arial', 11, 'bold'), bg='#f0f0f0', padx=10, pady=5)
        frame_buscar.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        frame_buscar.grid_columnconfigure(1, weight=1)
        
        tk.Label(frame_buscar, text="Valor Y buscado:", 
                 font=('Arial', 10), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self.entry_y_buscar = tk.Entry(frame_buscar, font=('Arial', 10), width=15)
        self.entry_y_buscar.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

        # Frame para botones de cálculo (para mantenerlos agrupados)
        frame_botones = tk.Frame(frame_resultados_cont, bg='#f0f0f0')
        frame_botones.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        frame_botones.grid_columnconfigure(0, weight=1)
        frame_botones.grid_columnconfigure(1, weight=1)
        
        btn_calcular = tk.Button(frame_botones, text="Calcular Interpolación\nCuadrática Inversa", 
                                 command=self.calcular_cuadratica,
                                 font=('Arial', 10, 'bold'), bg='#2196F3', 
                                 fg='white', padx=10, pady=5)
        btn_calcular.grid(row=0, column=0, padx=(0, 5), sticky='ew')
        
        btn_limpiar_resultados = tk.Button(frame_botones, text="Limpiar Valores", 
                                            command=self.limpiar_resultados,
                                            font=('Arial', 10), bg='#607D8B', 
                                            fg='white', padx=10, pady=5)
        btn_limpiar_resultados.grid(row=0, column=1, padx=(5, 0), sticky='ew')
        
        # Frame 3: Valores Intermedios y Cálculos (Row 3, debajo de la tabla)
        frame_valores = tk.LabelFrame(main_frame, text="Valores Intermedios y Solución", 
                                      font=('Arial', 11, 'bold'), bg='#f0f0f0', padx=10, pady=5)
        frame_valores.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
        
        # Grid para los valores (más compacto)
        frame_grid_valores = tk.Frame(frame_valores, bg='#f0f0f0')
        frame_grid_valores.pack(pady=5, fill='x')
        
        # Configurar 6 columnas de pesos 1 para distribución uniforme
        for i in range(6):
            frame_grid_valores.grid_columnconfigure(i, weight=1)
        
        # --- Fila 0: Puntos y Diferencias de Y
        self.crear_label_valor(frame_grid_valores, "y₀:", 'y0', 0, 0, '#E3F2FD', ancho=1)
        self.crear_label_valor(frame_grid_valores, "y₁:", 'y1', 0, 2, '#FFF3E0', ancho=1)
        self.crear_label_valor(frame_grid_valores, "y₂:", 'y2', 0, 4, '#E8F5E9', ancho=1)
        
        # --- Fila 1: h y Diferencias
        self.crear_label_valor(frame_grid_valores, "h:", 'h', 1, 0, '#F3E5F5', ancho=1)
        self.crear_label_valor(frame_grid_valores, "Δy₀:", 'delta_y0', 1, 2, '#FCE4EC', ancho=1)
        self.crear_label_valor(frame_grid_valores, "Δ²y₀:", 'delta2_y0', 1, 4, '#E0F2F1', ancho=1)
        
        # --- Fila 2: Coeficientes a y b
        self.crear_label_valor(frame_grid_valores, "Coef. a:", 'coef_a', 2, 0, '#E1BEE7', ancho=1)
        self.crear_label_valor(frame_grid_valores, "Coef. b:", 'coef_b', 2, 2, '#F8BBD0', ancho=1)
        self.crear_label_valor(frame_grid_valores, "Coef. c:", 'coef_c', 2, 4, '#B2DFDB', ancho=1)
        
        # --- Fila 3: Discriminante y soluciones
        tk.Label(frame_grid_valores, text="Cálculo cuadrático:", 
                 font=('Arial', 10, 'bold', 'italic'), bg='#f0f0f0').grid(row=3, column=0, columnspan=6, pady=(10, 5))
                 
        self.crear_label_valor(frame_grid_valores, "Disc.:", 'discriminante', 4, 0, '#FFCCBC', ancho=1)
        self.crear_label_valor(frame_grid_valores, "x₁:", 'x_sol1', 4, 2, '#C5CAE9', ancho=1)
        self.crear_label_valor(frame_grid_valores, "x₂:", 'x_sol2', 4, 4, '#D1C4E9', ancho=1)
        
        # --- Fila 5: Resultado final
        tk.Label(frame_grid_valores, text="", bg='#f0f0f0').grid(row=5, column=0, pady=5)
        self.crear_label_valor(frame_grid_valores, "RESULTADO FINAL X:", 'x_resultado', 6, 1, '#C8E6C9', ancho=3, final=True)
        
    def crear_label_valor(self, parent, texto, clave, fila, columna, color, ancho=15, final=False):
        """Crea un par de labels para mostrar nombre y valor con responsividad."""
        
        # Label con el nombre
        font_name = ('Arial', 10, 'bold')
        if final:
            font_name = ('Arial', 11, 'bold', 'underline')
        
        # El sticky 'e' asegura que el texto se alinea a la derecha (junto al valor)
        tk.Label(parent, text=texto, font=font_name, 
                 bg='#f0f0f0').grid(row=fila, column=columna, padx=(5, 2), pady=3, sticky='e')
        
        # Label con el valor (inicialmente vacío)
        label_valor = tk.Label(parent, text="---", font=('Arial', 10), 
                              bg=color, relief='groove', width=ancho, anchor='center', padx=5, pady=2)
        
        # Si es el resultado final, hacerlo ocupar más espacio (columnspan=3)
        if final:
            # Ocupa 3 columnas (columna+1 hasta columna+3)
            label_valor.grid(row=fila, column=columna+1, padx=(2, 5), pady=3, sticky='ew', columnspan=4)
        else:
            # Ocupa 1 columna
            label_valor.grid(row=fila, column=columna+1, padx=(2, 5), pady=3, sticky='ew')
             
        self.labels_valores[clave] = label_valor
    
    def actualizar_labels_valores(self, datos):
        """Actualiza los labels con los valores calculados"""
        def format_val(val):
            return f"{val:.6f}" if not math.isnan(val) else "N/A"
        
        def format_coef(val):
            return f"{val:.8f}" if not math.isnan(val) else "N/A"

        self.labels_valores['y0'].config(text=format_val(datos['y0']))
        self.labels_valores['y1'].config(text=format_val(datos['y1']))
        self.labels_valores['y2'].config(text=format_val(datos['y2']))
        self.labels_valores['h'].config(text=format_val(datos['h']))
        self.labels_valores['delta_y0'].config(text=format_val(datos['delta_y0']))
        self.labels_valores['delta2_y0'].config(text=format_val(datos['delta2_y0']))
        self.labels_valores['coef_a'].config(text=format_coef(datos['coef_a']))
        self.labels_valores['coef_b'].config(text=format_coef(datos['coef_b']))
        self.labels_valores['coef_c'].config(text=format_coef(datos['coef_c']))
        self.labels_valores['discriminante'].config(text=format_coef(datos['discriminante']))
        
        # Manejo de NaN para las soluciones y resultado final
        x_sol1_str = format_coef(datos['x_sol1'])
        x_sol2_str = format_coef(datos['x_sol2'])
        x_res_str = format_coef(datos['x_resultado'])

        self.labels_valores['x_sol1'].config(text=x_sol1_str)
        self.labels_valores['x_sol2'].config(text=x_sol2_str)
        
        self.labels_valores['x_resultado'].config(
            text=x_res_str,
            font=('Arial', 11, 'bold'),
            fg='#1B5E20'
        )
    
    def limpiar_labels_valores(self):
        """Limpia los labels de valores intermedios"""
        for clave, label in self.labels_valores.items():
            is_final = clave == 'x_resultado'
            label.config(text="---", font=('Arial', 10), fg='black' if not is_final else '#1B5E20')
            
    def agregar_punto(self):
        try:
            x = float(self.entry_x.get())
            y = float(self.entry_y_dato.get())
            
            # Buscar si ya existe un punto con el mismo X
            if x in self.x_vals:
                 messagebox.showwarning("Advertencia", f"El valor X={x} ya existe. Se reemplazará el valor Y asociado.")
                 idx = self.x_vals.index(x)
                 self.y_vals[idx] = y
            else:
                self.x_vals.append(x)
                self.y_vals.append(y)
            
            # Ordenar por X para asegurar la contigüidad
            try:
                self.x_vals, self.y_vals = zip(*sorted(zip(self.x_vals, self.y_vals)))
                self.x_vals = list(self.x_vals)
                self.y_vals = list(self.y_vals)
            except:
                # Caso extremo con pocos datos, no debería fallar.
                pass 
            
            self.actualizar_tabla()
            
            self.entry_x.delete(0, tk.END)
            self.entry_y_dato.delete(0, tk.END)
            self.entry_x.focus()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def eliminar_punto(self):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            # El índice visual es 1-basado. El índice real es 0-basado.
            index_visual = int(item['values'][0]) - 1 
            
            # Eliminar del índice real
            del self.x_vals[index_visual]
            del self.y_vals[index_visual]
            
            self.actualizar_tabla()
        else:
            messagebox.showwarning("Advertencia", "Seleccione un punto para eliminar")
    
    def actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar datos (ya ordenados)
        for i, (x, y) in enumerate(zip(self.x_vals, self.y_vals)):
            self.tree.insert('', 'end', values=(i+1, f"{x:.6f}", f"{y:.6f}"))
    
    def cargar_ejemplo(self):
        """Carga un ejemplo de datos para interpolación cuadrática"""
        self.x_vals = [0, 5, 10, 15, 20]
        self.y_vals = [1.792, 1.519, 1.308, 1.140, 1.002]
        self.actualizar_tabla()
        self.entry_y_buscar.delete(0, tk.END)
        self.entry_y_buscar.insert(0, "1.400")
        self.limpiar_labels_valores()
        messagebox.showinfo("Ejemplo Cargado", 
                            "Se ha cargado un ejemplo de datos para interpolación cuadrática (y=1.400).")
    
    def limpiar_datos(self):
        self.x_vals.clear()
        self.y_vals.clear()
        self.actualizar_tabla()
        self.entry_x.delete(0, tk.END)
        self.entry_y_dato.delete(0, tk.END)
        self.entry_y_buscar.delete(0, tk.END)
        self.limpiar_labels_valores()
    
    def limpiar_resultados(self):
        self.limpiar_labels_valores()
    
    def validar_datos(self):
        """Valida que haya suficientes datos ingresados para interpolación cuadrática"""
        if len(self.x_vals) < 3:
            messagebox.showerror("Error", 
                                 "Se necesitan al menos 3 puntos para interpolación cuadrática")
            return False
        
        try:
            float(self.entry_y_buscar.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un valor numérico válido para Y buscado.")
            return False
            
        return True
    
    def calcular_cuadratica(self):
        """Calcula la interpolación cuadrática inversa"""
        self.limpiar_resultados()
        
        if not self.validar_datos():
            return
        
        try:
            y_buscado = float(self.entry_y_buscar.get())
            
            # Advertencia de Extrapolación
            y_min, y_max = min(self.y_vals), max(self.y_vals)
            if y_buscado < y_min or y_buscado > y_max:
                messagebox.showwarning("Advertencia", 
                    f"El valor buscado (Y={y_buscado:.6f}) está fuera del rango de datos disponibles.\n"
                    f"Rango Y: [{y_min:.6f}, {y_max:.6f}].\n"
                    f"La extrapolación puede no ser precisa.")
            
            # Usar la lógica del algoritmo de interpolación cuadrática
            datos = AlgoritmoInterpolacion.calcular_interpolacion(
                self.x_vals, self.y_vals, y_buscado
            )
            
            # Actualizar los labels con los valores calculados
            self.actualizar_labels_valores(datos)
            
            # Muestra reporte en una ventana aparte
            reporte = AlgoritmoInterpolacion.generar_reporte(datos)
            self.mostrar_reporte(reporte)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")

    def mostrar_reporte(self, reporte):
        """Muestra el reporte de cálculo en una nueva ventana con ScrolledText."""
        reporte_window = tk.Toplevel(self.root)
        reporte_window.title("Reporte de Cálculo Paso a Paso")
        reporte_window.geometry("650x450")
        reporte_window.grab_set() # Bloquea la ventana principal
        
        st = scrolledtext.ScrolledText(reporte_window, wrap=tk.WORD, font=('Courier New', 10))
        st.insert(tk.INSERT, reporte)
        st.config(state=tk.DISABLED) # Hacerlo de solo lectura
        st.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Botón para cerrar
        btn_cerrar = tk.Button(reporte_window, text="Cerrar", command=reporte_window.destroy,
                               font=('Arial', 10, 'bold'), bg='#607D8B', fg='white')
        btn_cerrar.pack(pady=(0, 10))

if __name__ == "__main__":
    root = tk.Tk()
    app = InterpolacionInversa(root)
    root.mainloop()