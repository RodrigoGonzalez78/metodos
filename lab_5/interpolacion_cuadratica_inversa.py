import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

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
        # Buscar el intervalo que contiene y_buscado
        for i in range(len(y_vals) - 2):
            # Verificar si y_buscado está entre y[i] y y[i+2]
            y_min = min(y_vals[i], y_vals[i+1], y_vals[i+2])
            y_max = max(y_vals[i], y_vals[i+1], y_vals[i+2])
            
            if y_min <= y_buscado <= y_max:
                return i
        return 0

    @staticmethod
    def calcular_interpolacion(x_vals, y_vals, y_buscado):
        """
        Calcula el valor de X correspondiente a un Y dado
        mediante interpolación cuadrática inversa.
        
        La fórmula utilizada es:
        P(x) = y₀ + (Δy₀/h)*(x - x₀) + (Δ²y₀/2!h²)*(x - x₀)*(x - x₁)
        
        Donde:
        - y₀, y₁, y₂ son tres valores consecutivos de Y
        - x₀, x₁, x₂ son los valores correspondientes de X
        - h = x₁ - x₀ (espaciamiento entre puntos)
        - Δy₀ = y₁ - y₀ (primera diferencia dividida)
        - Δ²y₀ = (y₂ - 2*y₁ + y₀) (segunda diferencia dividida)

        Args:
            x_vals (list): Valores de X conocidos.
            y_vals (list): Valores de Y conocidos.
            y_buscado (float): Valor de Y que se desea interpolar.

        Returns:
            dict: Resultados y valores intermedios del cálculo.
        """
        # Encontrar el intervalo de 3 puntos que contiene y_buscado
        i = AlgoritmoInterpolacion.encontrar_intervalo(y_vals, y_buscado)

        # Extraer los tres puntos necesarios
        x0, x1, x2 = x_vals[i], x_vals[i+1], x_vals[i+2]
        y0, y1, y2 = y_vals[i], y_vals[i+1], y_vals[i+2]

        # Calcular el espaciamiento h
        h = x1 - x0
        
        # Calcular las diferencias divididas
        # Primera diferencia: Δy₀ = y₁ - y₀
        delta_y0 = y1 - y0
        
        # Segunda diferencia: Δ²y₀ = y₂ - 2*y₁ + y₀
        delta2_y0 = y2 - 2*y1 + y0
        
        # Diferencia entre el valor buscado y y₀
        diferencia_y = y_buscado - y0

        # Validar que h no sea cero (puntos no deben coincidir)
        if h == 0:
            raise ZeroDivisionError("Los puntos X seleccionados son idénticos")

        # Resolver la ecuación cuadrática inversa para encontrar x
        # La ecuación cuadrática es: P(x) = y₀ + (Δy₀/h)*(x - x₀) + (Δ²y₀/2h²)*(x - x₀)*(x - x₁)
        # Reorganizando: (Δ²y₀/2h²)*(x - x₀)*(x - x₁) + (Δy₀/h)*(x - x₀) + (y₀ - y) = 0
        
        # Coeficientes de la ecuación cuadrática ax² + bx + c = 0
        # donde u = x - x₀
        
        # Coeficiente de u²
        a = delta2_y0 / (2 * h * h)
        
        # Coeficiente de u (considerando que (x-x₀)*(x-x₁) = (x-x₀)*((x-x₀)-h) = u*(u-h))
        b = delta_y0 / h - (delta2_y0 * h) / (2 * h * h)
        
        # Término independiente
        c = -diferencia_y
        
        # Resolver usando la fórmula cuadrática: u = (-b ± √(b² - 4ac)) / 2a
        discriminante = b * b - 4 * a * c
        
        if discriminante < 0:
            raise ValueError("No existe solución real (discriminante negativo)")
        
        import math
        sqrt_discriminante = math.sqrt(discriminante)
        
        # Calcular ambas soluciones posibles
        u1 = (-b + sqrt_discriminante) / (2 * a) if a != 0 else -c / b
        u2 = (-b - sqrt_discriminante) / (2 * a) if a != 0 else -c / b
        
        # x = x₀ + u
        x_sol1 = x0 + u1
        x_sol2 = x0 + u2
        
        # Seleccionar la solución que esté dentro del intervalo [x₀, x₂]
        x_min, x_max = min(x0, x2), max(x0, x2)
        
        if x_min <= x_sol1 <= x_max:
            x_interpolado = x_sol1
        elif x_min <= x_sol2 <= x_max:
            x_interpolado = x_sol2
        else:
            # Si ninguna está en el intervalo, tomar la más cercana
            x_interpolado = x_sol1 if abs(x_sol1 - x0) < abs(x_sol2 - x0) else x_sol2

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
        resultado = f"\n{'='*70}\n"
        resultado += "INTERPOLACIÓN INVERSA CUADRÁTICA\n"
        resultado += f"{'='*70}\n\n"
        resultado += f"Puntos seleccionados:\n"
        resultado += f"  P0: (x0 = {datos['x0']:10.6f}, y0 = {datos['y0']:10.6f})\n"
        resultado += f"  P1: (x1 = {datos['x1']:10.6f}, y1 = {datos['y1']:10.6f})\n"
        resultado += f"  P2: (x2 = {datos['x2']:10.6f}, y2 = {datos['y2']:10.6f})\n\n"
        resultado += f"Valor buscado: y = {datos['y_buscado']:.6f}\n\n"
        resultado += f"Cálculos intermedios:\n"
        resultado += f"  h = x₁ - x₀ = {datos['h']:.6f}\n"
        resultado += f"  Δy₀ = y₁ - y₀ = {datos['delta_y0']:.6f}\n"
        resultado += f"  Δ²y₀ = y₂ - 2y₁ + y₀ = {datos['delta2_y0']:.6f}\n"
        resultado += f"  y - y₀ = {datos['diferencia_y']:.6f}\n\n"
        resultado += f"Ecuación cuadrática (au² + bu + c = 0):\n"
        resultado += f"  a = {datos['coef_a']:.8f}\n"
        resultado += f"  b = {datos['coef_b']:.8f}\n"
        resultado += f"  c = {datos['coef_c']:.8f}\n"
        resultado += f"  Discriminante = {datos['discriminante']:.8f}\n\n"
        resultado += f"Soluciones:\n"
        resultado += f"  x₁ = {datos['x_sol1']:.8f}\n"
        resultado += f"  x₂ = {datos['x_sol2']:.8f}\n\n"
        resultado += f"{'='*70}\nRESULTADO FINAL: x = {datos['x_resultado']:.8f}\n{'='*70}\n"
        return resultado

# ===========================
# INTERFAZ GRÁFICA
# ===========================

class InterpolacionInversa:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpolación Inversa Cuadrática")
        self.root.geometry("950x700")
        self.root.configure(bg='#f0f0f0')
        
        # Listas para almacenar los datos
        self.x_vals = []
        self.y_vals = []
        
        # Variables para los labels de valores intermedios
        self.labels_valores = {}
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.root, text="Interpolación Inversa Cuadrática", 
                         font=('Arial', 16, 'bold'), bg='#f0f0f0')
        titulo.pack(pady=10)
        
        # Frame para entrada de datos
        frame_entrada = tk.LabelFrame(self.root, text="Ingreso de Datos (Pares x, y)", 
                                     font=('Arial', 11, 'bold'), bg='#f0f0f0')
        frame_entrada.pack(padx=20, pady=10, fill='x')
        
        # Campos para ingresar x e y
        frame_inputs = tk.Frame(frame_entrada, bg='#f0f0f0')
        frame_inputs.pack(pady=10)
        
        tk.Label(frame_inputs, text="Valor X:", font=('Arial', 10), 
                bg='#f0f0f0').grid(row=0, column=0, padx=5, pady=5)
        self.entry_x = tk.Entry(frame_inputs, font=('Arial', 10), width=15)
        self.entry_x.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_inputs, text="Valor Y:", font=('Arial', 10), 
                bg='#f0f0f0').grid(row=0, column=2, padx=5, pady=5)
        self.entry_y_dato = tk.Entry(frame_inputs, font=('Arial', 10), width=15)
        self.entry_y_dato.grid(row=0, column=3, padx=5, pady=5)
        
        btn_agregar = tk.Button(frame_inputs, text="Agregar Punto", 
                               command=self.agregar_punto,
                               font=('Arial', 9, 'bold'), bg='#4CAF50', fg='white')
        btn_agregar.grid(row=0, column=4, padx=10, pady=5)
        
        btn_cargar_ejemplo = tk.Button(frame_inputs, text="Cargar Ejemplo", 
                                       command=self.cargar_ejemplo,
                                       font=('Arial', 9), bg='#9C27B0', fg='white')
        btn_cargar_ejemplo.grid(row=0, column=5, padx=5, pady=5)
        
        btn_limpiar_datos = tk.Button(frame_inputs, text="Limpiar Datos", 
                                      command=self.limpiar_datos,
                                      font=('Arial', 9), bg='#F44336', fg='white')
        btn_limpiar_datos.grid(row=0, column=6, padx=5, pady=5)
        
        # Frame para mostrar datos ingresados
        frame_tabla = tk.LabelFrame(self.root, text="Datos Ingresados", 
                                   font=('Arial', 11, 'bold'), bg='#f0f0f0')
        frame_tabla.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Crear Treeview para mostrar los datos
        columns = ('index', 'x', 'y')
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show='headings', height=6)
        
        self.tree.heading('index', text='#')
        self.tree.heading('x', text='X')
        self.tree.heading('y', text='Y')
        
        self.tree.column('index', width=50, anchor='center')
        self.tree.column('x', width=150, anchor='center')
        self.tree.column('y', width=150, anchor='center')
        
        self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar para la tabla
        scrollbar_tabla = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tree.yview)
        scrollbar_tabla.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar_tabla.set)
        
        # Botón para eliminar punto seleccionado
        btn_eliminar = tk.Button(frame_tabla, text="Eliminar Seleccionado", 
                                command=self.eliminar_punto,
                                font=('Arial', 9), bg='#FF5722', fg='white')
        btn_eliminar.pack(pady=5)
        
        # Frame para valor a buscar
        frame_buscar = tk.LabelFrame(self.root, text="Valor Y a Interpolar (Buscar X)", 
                                    font=('Arial', 11, 'bold'), bg='#f0f0f0')
        frame_buscar.pack(padx=20, pady=10, fill='x')
        
        frame_buscar_input = tk.Frame(frame_buscar, bg='#f0f0f0')
        frame_buscar_input.pack(pady=10)
        
        tk.Label(frame_buscar_input, text="Valor Y buscado:", 
                font=('Arial', 10), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=5)
        
        self.entry_y_buscar = tk.Entry(frame_buscar_input, font=('Arial', 10), width=15)
        self.entry_y_buscar.grid(row=0, column=1, padx=10, pady=5)
        
        # Frame para mostrar valores intermedios calculados
        frame_valores = tk.LabelFrame(self.root, text="Valores Intermedios y Cálculos", 
                                     font=('Arial', 11, 'bold'), bg='#f0f0f0')
        frame_valores.pack(padx=20, pady=10, fill='x')
        
        # Grid para los valores
        frame_grid_valores = tk.Frame(frame_valores, bg='#f0f0f0')
        frame_grid_valores.pack(pady=10)
        
        # Primera fila - Puntos Y
        self.crear_label_valor(frame_grid_valores, "y₀:", 'y0', 0, 0, '#E3F2FD')
        self.crear_label_valor(frame_grid_valores, "y₁:", 'y1', 0, 2, '#FFF3E0')
        self.crear_label_valor(frame_grid_valores, "y₂:", 'y2', 0, 4, '#E8F5E9')
        
        # Segunda fila - Espaciamiento y diferencias
        self.crear_label_valor(frame_grid_valores, "h = x₁ - x₀:", 'h', 1, 0, '#F3E5F5')
        self.crear_label_valor(frame_grid_valores, "Δy₀ = y₁ - y₀:", 'delta_y0', 1, 2, '#FCE4EC')
        self.crear_label_valor(frame_grid_valores, "Δ²y₀:", 'delta2_y0', 1, 4, '#E0F2F1')
        
        # Tercera fila - Diferencia Y
        self.crear_label_valor(frame_grid_valores, "y - y₀:", 'diferencia_y', 2, 1, '#FFF9C4', ancho=15)
        
        # Cuarta fila - Coeficientes de ecuación cuadrática
        tk.Label(frame_grid_valores, text="Ecuación cuadrática:", 
                font=('Arial', 10, 'bold', 'italic'), bg='#f0f0f0').grid(row=3, column=0, columnspan=6, pady=10)
        
        self.crear_label_valor(frame_grid_valores, "a:", 'coef_a', 4, 0, '#E1BEE7')
        self.crear_label_valor(frame_grid_valores, "b:", 'coef_b', 4, 2, '#F8BBD0')
        self.crear_label_valor(frame_grid_valores, "c:", 'coef_c', 4, 4, '#B2DFDB')
        
        # Quinta fila - Discriminante y soluciones
        self.crear_label_valor(frame_grid_valores, "Discriminante:", 'discriminante', 5, 1, '#FFCCBC', ancho=15)
        
        self.crear_label_valor(frame_grid_valores, "x₁:", 'x_sol1', 6, 0, '#C5CAE9')
        self.crear_label_valor(frame_grid_valores, "x₂:", 'x_sol2', 6, 2, '#D1C4E9')
        
        # Sexta fila - Resultado final
        tk.Label(frame_grid_valores, text="", bg='#f0f0f0').grid(row=7, column=0, pady=5)
        self.crear_label_valor(frame_grid_valores, "x (resultado final):", 'x_resultado', 8, 1, '#C8E6C9', ancho=20)
        
        # Frame para botones de cálculo
        frame_botones = tk.Frame(self.root, bg='#f0f0f0')
        frame_botones.pack(pady=10)
        
        btn_calcular = tk.Button(frame_botones, text="Calcular Interpolación\nCuadrática Inversa", 
                              command=self.calcular_cuadratica,
                              font=('Arial', 11, 'bold'), bg='#2196F3', 
                              fg='white', width=25, height=2)
        btn_calcular.grid(row=0, column=0, padx=10)
        
        btn_limpiar_resultados = tk.Button(frame_botones, text="Limpiar Valores", 
                                          command=self.limpiar_resultados,
                                          font=('Arial', 9), bg='#607D8B', 
                                          fg='white', width=20)
        btn_limpiar_resultados.grid(row=0, column=1, padx=10)
    
    def crear_label_valor(self, parent, texto, clave, fila, columna, color, ancho=15):
        """Crea un par de labels para mostrar nombre y valor"""
        # Label con el nombre
        tk.Label(parent, text=texto, font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').grid(row=fila, column=columna, padx=5, pady=5, sticky='e')
        
        # Label con el valor (inicialmente vacío)
        label_valor = tk.Label(parent, text="---", font=('Arial', 10), 
                              bg=color, relief='sunken', width=ancho, anchor='center')
        label_valor.grid(row=fila, column=columna+1, padx=5, pady=5)
        
        self.labels_valores[clave] = label_valor
    
    def actualizar_labels_valores(self, datos):
        """Actualiza los labels con los valores calculados"""
        self.labels_valores['y0'].config(text=f"{datos['y0']:.6f}")
        self.labels_valores['y1'].config(text=f"{datos['y1']:.6f}")
        self.labels_valores['y2'].config(text=f"{datos['y2']:.6f}")
        self.labels_valores['h'].config(text=f"{datos['h']:.6f}")
        self.labels_valores['delta_y0'].config(text=f"{datos['delta_y0']:.6f}")
        self.labels_valores['delta2_y0'].config(text=f"{datos['delta2_y0']:.6f}")
        self.labels_valores['diferencia_y'].config(text=f"{datos['diferencia_y']:.6f}")
        self.labels_valores['coef_a'].config(text=f"{datos['coef_a']:.8f}")
        self.labels_valores['coef_b'].config(text=f"{datos['coef_b']:.8f}")
        self.labels_valores['coef_c'].config(text=f"{datos['coef_c']:.8f}")
        self.labels_valores['discriminante'].config(text=f"{datos['discriminante']:.8f}")
        self.labels_valores['x_sol1'].config(text=f"{datos['x_sol1']:.8f}")
        self.labels_valores['x_sol2'].config(text=f"{datos['x_sol2']:.8f}")
        self.labels_valores['x_resultado'].config(
            text=f"{datos['x_resultado']:.8f}",
            font=('Arial', 11, 'bold'),
            fg='#1B5E20'
        )
    
    def limpiar_labels_valores(self):
        """Limpia los labels de valores intermedios"""
        for label in self.labels_valores.values():
            label.config(text="---")
    
    def agregar_punto(self):
        try:
            x = float(self.entry_x.get())
            y = float(self.entry_y_dato.get())
            
            self.x_vals.append(x)
            self.y_vals.append(y)
            
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
            index = int(item['values'][0]) - 1
            
            del self.x_vals[index]
            del self.y_vals[index]
            
            self.actualizar_tabla()
        else:
            messagebox.showwarning("Advertencia", "Seleccione un punto para eliminar")
    
    def actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar datos
        for i, (x, y) in enumerate(zip(self.x_vals, self.y_vals)):
            self.tree.insert('', 'end', values=(i+1, f"{x:.6f}", f"{y:.6f}"))
    
    def cargar_ejemplo(self):
        """Carga un ejemplo de datos para interpolación cuadrática"""
        self.x_vals = [0, 5, 10, 15, 20]
        self.y_vals = [1.792, 1.519, 1.308, 1.140, 1.002]
        self.actualizar_tabla()
        self.entry_y_buscar.delete(0, tk.END)
        self.entry_y_buscar.insert(0, "1.400")
        messagebox.showinfo("Ejemplo Cargado", 
                           "Se ha cargado un ejemplo de datos para interpolación cuadrática")
    
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
        return True
    
    def calcular_cuadratica(self):
        """Calcula la interpolación cuadrática inversa"""
        if not self.validar_datos():
            return
        
        try:
            y_buscado = float(self.entry_y_buscar.get())
            
            y_min, y_max = min(self.y_vals), max(self.y_vals)
            if y_buscado < y_min or y_buscado > y_max:
                messagebox.showwarning("Advertencia", 
                    f"El valor está fuera del rango de datos disponibles.\n"
                    f"Rango Y: [{y_min:.6f}, {y_max:.6f}]\n"
                    f"La extrapolación puede no ser precisa.")
            
            # Usar la lógica del algoritmo de interpolación cuadrática
            datos = AlgoritmoInterpolacion.calcular_interpolacion(
                self.x_vals, self.y_vals, y_buscado
            )
            
            # Actualizar los labels con los valores calculados
            self.actualizar_labels_valores(datos)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
        except ZeroDivisionError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = InterpolacionInversa(root)
    root.mainloop()