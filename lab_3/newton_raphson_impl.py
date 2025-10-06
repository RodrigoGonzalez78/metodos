import sympy as sp
import time
import numpy as np
import matplotlib.pyplot as plt

def metodo_newton_raphson(func, derivada, x0, tolerancia=1e-6, max_iter=100):
    """
    Método de Newton-Raphson
    
    Parámetros:
    - func: función a evaluar
    - derivada: derivada de la función
    - x0: estimación inicial
    - tolerancia: precisión deseada
    - max_iter: número máximo de iteraciones
    """
    tiempo_inicio = time.time()  # Iniciar medición de tiempo
    
    historial = []
    x = x0
    
    for i in range(max_iter):
        fx = func(x)
        fpx = derivada(x)
        
        if abs(fpx) < 1e-14:
            tiempo_total = time.time() - tiempo_inicio
            print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
            raise ValueError(f"Derivada muy pequeña en x = {x}. El método puede no converger.")
        
        x_nuevo = x - fx / fpx
        error = abs(x_nuevo - x)
        
        historial.append({
            'iteracion': i + 1,
            'x': x,
            'fx': fx,
            'fpx': fpx,
            'x_nuevo': x_nuevo,
            'error': error
        })
        

        if error < tolerancia or abs(fx) < tolerancia:
            tiempo_total = time.time() - tiempo_inicio  # Calcular tiempo total
            print(f"\nConvergencia alcanzada en {i+1} iteraciones")
            print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
            return x_nuevo, i + 1, historial
        
        x = x_nuevo
    
    tiempo_total = time.time() - tiempo_inicio  # Calcular tiempo total
    print(f"\nMáximo de iteraciones alcanzado")
    print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
    return x, max_iter, historial



def seleccionar_x0_fourier(func, a, b):
    """
    Selecciona x0 basado en la condición de Fourier (menor valor absoluto de f(x))
    
    Parámetros:
    - func: función a evaluar
    - a: extremo izquierdo del intervalo
    - b: extremo derecho del intervalo
    
    Retorna:
    - x0: punto inicial seleccionado
    - fa, fb: valores de la función en los extremos
    """
    try:
        fa = func(a)
        fb = func(b)
        
        print(f"  f({a:.2f}) = {fa:.6f}")
        print(f"  f({b:.2f}) = {fb:.6f}")
        
        # Verificar condición de Bolzano
        if fa * fb > 0:
            print(f"  ⚠ No se cumple la condición de Bolzano en [{a:.2f}, {b:.2f}]")
            return None, fa, fb
        
        # Seleccionar x0 según condición de Fourier
        if abs(fa) < abs(fb):
            x0 = a
            print(f"  ✓ Seleccionado x0 = {x0:.2f} (menor |f(x)|)")
        else:
            x0 = b
            print(f"  ✓ Seleccionado x0 = {x0:.2f} (menor |f(x)|)")
        
        return x0, fa, fb
        
    except Exception as e:
        print(f"  ⚠ Error al evaluar la función: {e}")
        return None, None, None


def metodo_tanteo(func, x_min=-10, x_max=10, paso=0.5):
    """
    Encuentra intervalos donde se encuentran las raíces de una función usando el método de tanteo.
    
    Parámetros:
    - func: función matemática a evaluar
    - x_min: límite inferior del rango de búsqueda
    - x_max: límite superior del rango de búsqueda 
    - paso: tamaño del paso para el tanteo
    
    Retorna:
    - Lista de tuplas con los intervalos [a, b] donde hay cambio de signo
    """
    intervalos = []
    x = x_min
    
    try:
        f_anterior = func(x)
    except:
        print(f"Error al evaluar la función en x = {x}")
        return intervalos
    
    print(f"{'x':>8} | {'f(x)':>12} | {'Cambio de signo':>15}")
    print("-" * 40)
    print(f"{x:8.2f} | {f_anterior:12.4f} |")
    
    x += paso
    
    while x <= x_max:
        try:
            f_actual = func(x)
            
            # Verificar cambio de signo (teorema de Bolzano)
            if f_anterior * f_actual < 0:
                intervalos.append((x - paso, x))
                print(f"{x:8.2f} | {f_actual:12.4f} | *** [{x-paso:.2f}, {x:.2f}]")
            else:
                print(f"{x:8.2f} | {f_actual:12.4f} |")
            
            f_anterior = f_actual
            x += paso
            
        except:
            print(f"Error al evaluar la función en x = {x}")
            x += paso
            continue
    
    return intervalos






def graficar_funcion_con_intervalos(func, intervalos, x_min=-10, x_max=10):
    """
    Grafica la función y marca los intervalos donde se encuentran las raíces.
    """
    x = np.linspace(x_min, x_max, 1000)
    
    try:
        y = [func(xi) for xi in x]
    except:
        print("Error al generar la gráfica")
        return
    
    plt.figure(figsize=(12, 8))
    plt.plot(x, y, 'b-', linewidth=2, label='f(x)')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    plt.axvline(x=0, color='k', linestyle='--', alpha=0.5)
    
    
    for i, (a, b) in enumerate(intervalos):
        plt.axvspan(a, b, alpha=0.3, color='red', 
                   label=f'Intervalo {i+1}: [{a:.2f}, {b:.2f}]' if i == 0 else "")
        if i > 0:
            plt.axvspan(a, b, alpha=0.3, color='red')
    
    plt.grid(True, alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Función con intervalos que contienen raíces')
    plt.legend()
    plt.show(block=False)


def solicitar_parametros():
    """Solicita todos los parámetros necesarios al usuario"""
    print("=== CONFIGURACIÓN DEL MÉTODO DE TANTEO ===")
    
    # Solicitar función
    f_str = input("Ingrese la función f(x): ")
    
    # Convertir a funciones Python y simbólicas
    try:
        x = sp.Symbol("x")
        f_sympy = sp.sympify(f_str)
        
        # Calcular la derivada automáticamente
        print(f"Calculando la derivada de f(x) = {f_str}")
        f_deriv_sympy = sp.diff(f_sympy, x)
        print(f"f'(x) = {f_deriv_sympy}")
        
        f = sp.lambdify(x, f_sympy, "math")
        f_deriv = sp.lambdify(x, f_deriv_sympy, "math")
    except Exception as e:
        print(f"⚠ Error al procesar la función: {e}")
        return None, None, None, None, None, None, None
    
    # Solicitar parámetros del tanteo
    print("\n=== PARÁMETROS DEL TANTEO ===")
    try:
        x_min = float(input("Ingrese el límite inferior del intervalo de tanteo: "))
        x_max = float(input("Ingrese el límite superior del intervalo de tanteo: "))
        paso = float(input("Ingrese el tamaño del paso para el tanteo: "))
        
        if x_min >= x_max:
            print("⚠ El límite inferior debe ser menor que el superior")
            return None, None, None, None, None, None, None
        
        if paso <= 0:
            print("⚠ El paso debe ser positivo")
            return None, None, None, None, None, None, None
            
    except ValueError:
        print("⚠ Error en los parámetros del tanteo")
        return None, None, None, None, None, None, None
    
    # Solicitar parámetros de Newton-Raphson
    print("\n=== PARÁMETROS DE NEWTON-RAPHSON ===")
    tolerancia_input = input("Ingrese la tolerancia (presione Enter para usar 1e-6): ").strip()
    if tolerancia_input == "":
        tolerancia = 1e-6
    else:
        try:
            tolerancia = float(tolerancia_input)
        except ValueError:
            print("⚠ Valor inválido para tolerancia. Usando 1e-6 por defecto.")
            tolerancia = 1e-6
    
    max_iter_input = input("Ingrese el máximo de iteraciones (presione Enter para usar 100): ").strip()
    if max_iter_input == "":
        max_iter = 100
    else:
        try:
            max_iter = int(max_iter_input)
            if max_iter <= 0:
                print("⚠ El máximo de iteraciones debe ser positivo. Usando 100 por defecto.")
                max_iter = 100
        except ValueError:
            print("⚠ Valor inválido para máximo de iteraciones. Usando 100 por defecto.")
            max_iter = 100
    
    return f, f_deriv, x_min, x_max, paso, tolerancia, max_iter




def main():
    """Función principal que ejecuta todo el proceso"""
    
    # Solicitar parámetros
    f, f_deriv, x_min, x_max, paso, tolerancia, max_iter = solicitar_parametros()
    
    if f is None:
        print("⚠ Error en la configuración. Terminando programa.")
        return
    
    print(f"\n=== CONFIGURACIÓN FINAL ===")
    print(f"Intervalo de tanteo: [{x_min}, {x_max}]")
    print(f"Paso: {paso}")
    print(f"Tolerancia: {tolerancia}")
    print(f"Máx. iteraciones: {max_iter}")
    
    # Realizar tanteo
    print(f"\n=== MÉTODO DE TANTEO ===")
    intervalos = metodo_tanteo(f, x_min, x_max, paso)
    
    if not intervalos:
        print("\n⚠ No se encontraron intervalos con cambio de signo.")
        return
    
    print(f"\n✓ Se encontraron {len(intervalos)} intervalos con posibles raíces:")
    for i, (a, b) in enumerate(intervalos, 1):
        print(f"  Intervalo {i}: [{a:.2f}, {b:.2f}]")
    
    # Mostrar gráfica
    mostrar_grafico = input("\n¿Desea guardar la gráfica? (s/n, Enter=sí): ").strip().lower()
    if mostrar_grafico in ['', 's', 'si', 'sí', 'y', 'yes']:
        graficar_funcion_con_intervalos(f, intervalos, x_min, x_max)
        print("📊 Gráfico Guardado")
    
    # Aplicar Newton-Raphson a cada intervalo
    print(f"\n=== APLICANDO NEWTON-RAPHSON ===")
    
    for i, (a, b) in enumerate(intervalos, 1):
        print(f"\n--- Intervalo {i}: [{a:.2f}, {b:.2f}] ---")
        
        # Seleccionar x0 usando condición de Fourier
        x0, fa, fb = seleccionar_x0_fourier(f, a, b)
        
        if x0 is None:
            print("  Saltando este intervalo...")
            continue
        
        try:
            # Ejecutar Newton-Raphson
            print(f"\n  === MÉTODO NEWTON-RAPHSON ===")
            print(f"  Intervalo: [{a:.6f}, {b:.6f}]")
            print(f"  x₀ = {x0:.6f}")
            print(f"  Tolerancia = {tolerancia}")
            print(f"  Máx. iteraciones = {max_iter}")
            print()
            
            raiz, iteraciones, historial = metodo_newton_raphson(
                f, f_deriv, 
                x0=x0, 
                tolerancia=tolerancia, 
                max_iter=max_iter
            )
            
            # Mostrar tabla de iteraciones en el mismo estilo que regla falsa
            print(f"{'Iter':>4} | {'x':>12} | {'f(x)':>12} | {'f\'(x)':>12} | {'Error':>12}")
            print("-" * 65)
            
            for entrada in historial:
                iter_num = entrada.get('iteracion', 0)
                xi = entrada['x']
                fxi = entrada['fx'] 
                fpxi = entrada['fpx']
                error = entrada['error']
                print(f"{iter_num:4} | {xi:12.8f} | {fxi:12.8f} | {fpxi:12.8f} | {error:12.8f}")
            
            # Mensaje de convergencia
            if abs(f(raiz)) < tolerancia:
                print(f"\nConvergencia alcanzada en {iteraciones} iteraciones")
            else:
                print(f"\nMáximo de iteraciones alcanzado")
            
            # Resultados finales
            print(f"\n  📊 RESULTADOS FINALES:")
            print(f"     Raíz aproximada: x = {raiz:.8f}")
            print(f"     f(x) = {f(raiz):.8e}")
            print(f"     Iteraciones: {iteraciones}")
            print(f"     Error final: {historial[-1]['error']:.8e}")
                
        except Exception as e:
            print(f"  ⚠ Error durante Newton-Raphson: {e}")
            continue

if __name__ == "__main__":
    main()
    input("Presioná Enter para salir...")