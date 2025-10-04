import math

# Valores redondeados a 6 decimales
pi_aprox = round(math.pi, 6)  # 3.141593
e_aprox = round(math.e, 6)     # 2.718282

# Cociente con valores redondeados
r_aprox = pi_aprox / e_aprox

# Valor real con mayor precisión
r_real = math.pi / math.e

# Error absoluto
error_abs = abs(r_real - r_aprox)

# Error relativo
error_rel = error_abs / abs(r_real)

# Dígitos significativos correctos
digitos_significativos = -math.log10(error_rel)

# Dígitos decimales correctos
# Comparamos dígito por dígito
str_real = f"{r_real:.15f}"
str_aprox = f"{r_aprox:.15f}"

decimales_correctos = 0
punto_encontrado = False
for i in range(min(len(str_real), len(str_aprox))):
    if str_real[i] == '.':
        punto_encontrado = True
        continue
    if punto_encontrado:
        if str_real[i] == str_aprox[i]:
            decimales_correctos += 1
        else:
            break

# Mostrar resultados
print(f"π redondeado: {pi_aprox}")
print(f"e redondeado: {e_aprox}")
print(f"\nValor real (π/e): {r_real:.15f}")
print(f"Valor aproximado: {r_aprox:.15f}")
print(f"\nError absoluto: {error_abs:.2e}")
print(f"Error relativo: {error_rel:.2e}")
digitos_sig_entero = int(digitos_significativos)
print(f"\nDígitos significativos correctos: {digitos_sig_entero:.1f}")
print(f"Decimales correctos: {decimales_correctos}")