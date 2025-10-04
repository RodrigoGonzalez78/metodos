import math

print("=== CÁLCULO DEL ÁREA DE LA PISCINA ===\n")

# Dimensiones reales
ancho_real = math.sqrt(2)
largo_real = math.sqrt(8)

# Dimensiones aproximadas (redondeadas)
ancho_aprox = 1.41
largo_aprox = 2.83

# Área aproximada (usando valores redondeados)
A_aprox = ancho_aprox * largo_aprox

# Área real (usando valores exactos)
A_real = ancho_real * largo_real

# También podemos simplificar: √2 × √8 = √16 = 4
A_simplificada = math.sqrt(2 * 8)  # = √16 = 4

# Errores
error_abs = abs(A_real - A_aprox)
error_rel = error_abs / A_real

print("--- Parte a) ¿Es 3.99 m² el valor real? ---")
print(f"Área aproximada: {A_aprox} m²")
print(f"Área real: {A_real} m²")
print(f"Error absoluto: {error_abs:.5f} m²")
print(f"Error relativo: {error_rel:.5%}")
print(f"\n✗ NO, 3.99 m² NO es el valor real.")
print(f"  Razón: Se usaron valores redondeados (1.41 y 2.83)")
print(f"  que introducen error de redondeo en el cálculo.")

print("\n--- Parte b) Forma más exacta de calcular ---")
print(f"✓ SÍ, existe una forma exacta:")
print(f"  A = √2 × √8 = √(2×8) = √16 = 4 m²")
print(f"  Valor exacto: {A_simplificada} m²")
print(f"\nConclusión: El área real es EXACTAMENTE 4 m², no 3.99 m²")