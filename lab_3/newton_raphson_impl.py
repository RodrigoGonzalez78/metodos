import sympy as sp
import metodos as mt
import tanteo as tn

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
    intervalos = tn.metodo_tanteo(f, x_min, x_max, paso)
    
    if not intervalos:
        print("\n⚠ No se encontraron intervalos con cambio de signo.")
        return
    
    print(f"\n✓ Se encontraron {len(intervalos)} intervalos con posibles raíces:")
    for i, (a, b) in enumerate(intervalos, 1):
        print(f"  Intervalo {i}: [{a:.2f}, {b:.2f}]")
    
    # Mostrar gráfica
    mostrar_grafico = input("\n¿Desea mostrar la gráfica? (s/n, Enter=sí): ").strip().lower()
    if mostrar_grafico in ['', 's', 'si', 'sí', 'y', 'yes']:
        tn.graficar_funcion_con_intervalos(f, intervalos, x_min, x_max)
        print("📊 Gráfico mostrado. El programa continuará automáticamente...")
    
    # Aplicar Newton-Raphson a cada intervalo
    print(f"\n=== APLICANDO NEWTON-RAPHSON ===")
    
    for i, (a, b) in enumerate(intervalos, 1):
        print(f"\n--- Intervalo {i}: [{a:.2f}, {b:.2f}] ---")
        
        # Seleccionar x0 usando condición de Fourier
        x0, fa, fb = mt.seleccionar_x0_fourier(f, a, b)
        
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
            
            raiz, iteraciones, historial = mt.metodo_newton_raphson(
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