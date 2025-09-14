import math
import time

def pi_leibniz(N):
    """
    Calcula pi usando la serie de Leibniz con N términos.
    """
    suma = 0.0
    for k in range(N):
        suma += ((-1)**k) / (2*k + 1)
    return 4 * suma

def buscar_terminos(decimales):
    """
    Encuentra cuántos términos de la serie son necesarios
    para que la aproximación de pi tenga 'decimales' correctos,
    contando desde el primer decimal después de la coma.
    """
    # Obtener los primeros 'decimales' dígitos de pi después del punto decimal
    pi_str = f"{math.pi:.{decimales + 5}f}"  # Más precisión para comparar
    objetivo_str = pi_str[:decimales + 2]  # "3." + decimales dígitos
    
    N = 1
    while True:
        aprox = pi_leibniz(N)
        aprox_str = f"{aprox:.{decimales + 5}f}"
        aprox_truncada = aprox_str[:decimales + 2]  # "3." + decimales dígitos
        
        # Mostrar progreso cada cierto número de iteraciones para no saturar
        if N == 1 or N % max(1, N // 100) == 0 or N < 100:
            print(f"N={N:6}, Aproximación: {aprox:.{min(decimales+2, 10)}f}")
        
        # Verificar si los primeros 'decimales' después del punto son correctos
        if aprox_truncada == objetivo_str:
            print(f"N={N:6}, Aproximación: {aprox:.{decimales+2}f} ✓")
            return N, aprox
        
        N += 1
        
        # Protección contra loops infinitos (en caso de que algo salga mal)
        if N > 10**8:
            print("Se alcanzó el límite máximo de iteraciones")
            break

def verificar_decimales(aprox, decimales):
    """
    Función auxiliar para verificar cuántos decimales son correctos
    """
    pi_str = str(math.pi)
    aprox_str = str(aprox)
    
    decimales_correctos = 0
    # Saltar el "3."
    for i in range(2, min(len(pi_str), len(aprox_str))):
        if pi_str[i] == aprox_str[i]:
            decimales_correctos += 1
        else:
            break
    
    return decimales_correctos

if __name__ == "__main__":
    print("Cálculo de π usando la Serie de Leibniz")
    print("π = 4 * (1 - 1/3 + 1/5 - 1/7 + 1/9 - ...)")
    print("-" * 50)
    
    n = int(input("Ingrese la cantidad de cifras decimales exactas de π que desea calcular: "))
    
    if n > 10:
        print(f"\nAdvertencia: Para {n} decimales se necesitarán muchas iteraciones.")
        print("Esto puede tomar mucho tiempo debido a la convergencia lenta de la serie de Leibniz.")
        continuar = input("¿Desea continuar? (s/n): ").lower()
        if continuar != 's':
            exit()
    
    print(f"\nBuscando {n} decimales exactos...")
    start = time.perf_counter()
    N, aprox = buscar_terminos(n)
    elapsed = time.perf_counter() - start
    
    # Verificación adicional
    decimales_reales = verificar_decimales(aprox, n)
    
    print("\n" + "="*60)
    print("RESULTADOS:")
    print("="*60)
    print(f"Decimales solicitados: {n}")
    print(f"Decimales obtenidos:   {decimales_reales}")
    print(f"Términos necesarios:   {N:,}")
    print(f"Aproximación de π:     {aprox:.{n+2}f}")
    print(f"Valor real math.pi:    {math.pi:.{n+2}f}")
    print(f"Tiempo transcurrido:   {elapsed:.4f} segundos")
    
    # Mostrar la diferencia
    diferencia = abs(aprox - math.pi)
    print(f"Error absoluto:        {diferencia:.2e}")
    print("="*60)

