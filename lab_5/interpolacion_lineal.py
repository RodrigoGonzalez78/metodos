import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# ===========================
# LÓGICA DEL ALGORITMO
# ===========================

class AlgoritmoInterpolacion:
    """Contiene la lógica del método de interpolación lineal inversa."""

    @staticmethod
    def encontrar_intervalo(y_vals, y_buscado):
        """
        Busca el intervalo donde se encuentra el valor y_buscado.

        Args:
            y_vals (list): Lista de valores de Y conocidos.
            y_buscado (float): Valor de Y para el cual se quiere interpolar X.

        Returns:
            int: Índice del intervalo encontrado.
        """
        for i in range(len(y_vals) - 1):
            if (y_vals[i] >= y_buscado >= y_vals[i+1]) or \
               (y_vals[i] <= y_buscado <= y_vals[i+1]):
                return i
        return 0

    @staticmethod
    def calcular_interpolacion(x_vals, y_vals, y_buscado):
        """
        Calcula el valor de X correspondiente a un Y dado
        mediante interpolación lineal inversa.

        Args:
            x_vals (list): Valores de X conocidos.
            y_vals (list): Valores de Y conocidos.
            y_buscado (float): Valor de Y que se desea interpolar.

        Returns:
            dict: Resultados y valores intermedios del cálculo.
        """
        i = AlgoritmoInterpolacion.encontrar_intervalo(y_vals, y_buscado)

        x0, x1 = x_vals[i], x_vals[i+1]
        y0, y1 = y_vals[i], y_vals[i+1]

        h = x1 - x0
        delta_y = y1 - y0
        diferencia_y = y_buscado - y0

        if delta_y == 0:
            raise ZeroDivisionError("Los puntos seleccionados tienen el mismo valor de Y")

        x_interpolado = x0 + diferencia_y * h / delta_y

        return {
            'indice': i,
            'x0': x0, 'x1': x1,
            'y0': y0, 'y1': y1,
            'y_buscado': y_buscado,
            'h': h, 'delta_y': delta_y,
            'diferencia_y': diferencia_y,
            'x_resultado': x_interpolado
        }

    @staticmethod
    def generar_reporte(datos):
        """
        Genera un texto con el desarrollo paso a paso de la interpolación.

        Args:
            datos (dict): Resultados devueltos por calcular_interpolacion().

        Returns:
            str: Reporte formateado con todos los cálculos.
        """
        resultado = f"\n{'='*70}\n"
        resultado += "INTERPOLACIÓN INVERSA LINEAL\n"
        resultado += f"{'='*70}\n\n"
        resultado += f"Puntos seleccionados:\n"
        resultado += f"  P0: (x0 = {datos['x0']:10.6f}, y0 = {datos['y0']:10.6f})\n"
        resultado += f"  P1: (x1 = {datos['x1']:10.6f}, y1 = {datos['y1']:10.6f})\n\n"
        resultado += f"Valor buscado: y = {datos['y_buscado']:.6f}\n\n"
        resultado += f"h = {datos['h']:.6f}, Δy = {datos['delta_y']:.6f}, y - y0 = {datos['diferencia_y']:.6f}\n\n"
        resultado += f"x = x0 + (y - y0) * h / (y1 - y0)\n"
        resultado += f"x = {datos['x_resultado']:.8f}\n"
        resultado += f"{'='*70}\nRESULTADO FINAL: x = {datos['x_resultado']:.8f}\n{'='*70}\n"
        return resultado

# ===========================
# INTERFAZ GRÁFICA
# ===========================

class InterpolacionInversa:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpolación Inversa Lineal")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        
        # Listas para almacenar los datos
        self.x_vals = []
        self.y_vals = []
        
        # Variables para los labels de valores intermedios
        self.labels_valores = {}
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.root, text="Interpolación Inversa Lineal", 
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
        frame_valores = tk.LabelFrame(self.root, text="Valores Intermedios", 
                                     font=('Arial', 11, 'bold'), bg='#f0f0f0')
        frame_valores.pack(padx=20, pady=10, fill='x')
        
        # Grid para los valores
        frame_grid_valores = tk.Frame(frame_valores, bg='#f0f0f0')
        frame_grid_valores.pack(pady=10)
        
        # Primera fila
        self.crear_label_valor(frame_grid_valores, "y₀:", 'y0', 0, 0, '#E3F2FD')
        self.crear_label_valor(frame_grid_valores, "y:", 'y', 0, 2, '#FFF3E0')
        self.crear_label_valor(frame_grid_valores, "y₁:", 'y1', 0, 4, '#E8F5E9')
        
        # Segunda fila
        self.crear_label_valor(frame_grid_valores, "h = x₁ - x₀:", 'h', 1, 0, '#F3E5F5')
        self.crear_label_valor(frame_grid_valores, "y - y₀:", 'y_y0', 1, 2, '#FCE4EC')
        self.crear_label_valor(frame_grid_valores, "y₁ - y₀:", 'y1_y0', 1, 4, '#E0F2F1')
        
        # Tercera fila - Resultado
        tk.Label(frame_grid_valores, text="", bg='#f0f0f0').grid(row=2, column=0, pady=5)
        self.crear_label_valor(frame_grid_valores, "x (resultado):", 'x_resultado', 3, 1, '#C8E6C9', ancho=20)
        
        # Frame para botones de cálculo
        frame_botones = tk.Frame(self.root, bg='#f0f0f0')
        frame_botones.pack(pady=10)
        
        btn_calcular = tk.Button(frame_botones, text="Calcular Interpolación\nLineal Inversa", 
                              command=self.calcular_lineal,
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
        self.labels_valores['y'].config(text=f"{datos['y_buscado']:.6f}")
        self.labels_valores['y1'].config(text=f"{datos['y1']:.6f}")
        self.labels_valores['h'].config(text=f"{datos['h']:.6f}")
        self.labels_valores['y_y0'].config(text=f"{datos['diferencia_y']:.6f}")
        self.labels_valores['y1_y0'].config(text=f"{datos['delta_y']:.6f}")
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
        """Carga el ejemplo del ejercicio de viscosidad"""
        self.x_vals = [0, 5, 10, 15]
        self.y_vals = [1.792, 1.519, 1.308, 1.140]
        self.actualizar_tabla()
        self.entry_y_buscar.delete(0, tk.END)
        self.entry_y_buscar.insert(0, "1.702")
        messagebox.showinfo("Ejemplo Cargado", 
                           "Se ha cargado el ejemplo de viscosidad vs temperatura")
    
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
        """Valida que haya suficientes datos ingresados"""
        if len(self.x_vals) < 2:
            messagebox.showerror("Error", 
                               "Se necesitan al menos 2 puntos para interpolación lineal")
            return False
        return True
    
    def calcular_lineal(self):
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
            
            # Usar la lógica del algoritmo separada
            datos = AlgoritmoInterpolacion.calcular_interpolacion(
                self.x_vals, self.y_vals, y_buscado
            )
            
            # Actualizar los labels con los valores calculados
            self.actualizar_labels_valores(datos)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un valor numérico válido para Y")
        except ZeroDivisionError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = InterpolacionInversa(root)
    root.mainloop()