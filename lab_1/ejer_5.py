from decimal import Decimal, getcontext
import math

def calcular_e_serie(N):
    """
    Calcula e usando la serie: e = 1 + 1/1! + 1/2! + 1/3! + ... + 1/N!
    """
    suma = 1.0  # Empezamos con el primer término (1)
    factorial = 1.0
    
    print("Aproximación de e usando la serie:")
    print(f"Término 0: e ≈ {suma:.10f}")
    
    for n in range(1, N + 1):
        factorial *= n  # Calculamos n! incrementalmente
        termino = 1.0 / factorial
        suma += termino
        
        print(f"Término {n}: e ≈ {suma:.10f} (1/{n}! = {termino:.10f})")
    
    return suma

def calcular_e_decimal(N, precision=50):
    """
    Calcula e usando Decimal para mayor precisión
    """
    getcontext().prec = precision
    
    suma = Decimal(1)
    factorial = Decimal(1)
    
    print(f"\nAproximación con Decimal (precisión {precision}):")
    print(f"Término 0: e ≈ {suma}")
    
    for n in range(1, N + 1):
        factorial *= Decimal(n)
        termino = Decimal(1) / factorial
        suma += termino
        
        print(f"Término {n}: e ≈ {suma}")
    
    return suma

def analizar_convergencia():
    """
    Muestra cuántos términos se necesitan para una buena aproximación
    """
    print("\n" + "="*50)
    print("ANÁLISIS DE CONVERGENCIA")
    print("="*50)
    
    valor_real = math.e
    suma = 1.0
    factorial = 1.0
    
    for n in range(1, 20):
        factorial *= n
        termino = 1.0 / factorial
        suma += termino
        error = abs(valor_real - suma)
        
        print(f"n={n:2d} | e ≈ {suma:.15f} | Error: {error:.2e}")
        
        if error < 1e-10:
            print(f"¡Convergencia alcanzada! Error < 1e-10 con n={n}")
            break

if __name__ == "__main__":
    print("CÁLCULO DEL NÚMERO e USANDO SERIE INFINITA")
    print("e = 1 + 1/1! + 1/2! + 1/3! + ...")
    print(f"Valor real de math.e: {math.e}\n")
    
    try:
        N = int(input("Ingrese el número de términos de la serie (recomendado: 15): "))
        
        # Calcular con float
        aprox_float = calcular_e_serie(N)
        
        # Calcular con Decimal
        aprox_decimal = calcular_e_decimal(N)
        
        # Resultados finales
        print("\n" + "="*60)
        print("RESULTADOS FINALES:")
        print("="*60)
        print(f"Valor real de math.e:      {math.e}")
        print(f"Aproximación con {N} términos (float):  {aprox_float:.15f}")
        print(f"Aproximación con {N} términos (Decimal): {aprox_decimal}")
        print(f"Diferencia con valor real:  {abs(math.e - aprox_float):.2e}")
        
        # Análisis de convergencia
        analizar_convergencia()
        
    except ValueError:
        print("Error: Por favor ingrese un número entero válido.")
    except Exception as e:
        print(f"Error inesperado: {e}")
