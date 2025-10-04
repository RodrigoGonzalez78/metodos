import numpy as np

print("=== EFECTO DEL ERROR DE REDONDEO ===\n")

N = 100000

# ==========================================
# 1. Suma de 1 con precisión simple (float32)
# ==========================================
suma1_simple = np.float32(0)
for _ in range(N):
    suma1_simple += np.float32(1)

valor_esperado1 = N * 1
error1 = abs(suma1_simple - valor_esperado1)

print("--- SUMA DE 1 (float32) ---")
print(f"Valor calculado: {suma1_simple}")
print(f"Valor esperado:  {valor_esperado1}")
print(f"Error absoluto:  {error1}")
print(f"Error relativo:  {error1/valor_esperado1:.10e}")

# ==========================================
# 2. Suma de 0.00001 con precisión simple (float32)
# ==========================================
suma2_simple = np.float32(0)
for _ in range(N):
    suma2_simple += np.float32(0.00001)

valor_esperado2 = N * 0.00001
error2 = abs(suma2_simple - valor_esperado2)

print("\n--- SUMA DE 0.00001 (float32) ---")
print(f"Valor calculado: {suma2_simple}")
print(f"Valor esperado:  {valor_esperado2}")
print(f"Error absoluto:  {error2:.10f}")
print(f"Error relativo:  {error2/valor_esperado2:.10e}")

# ==========================================
# 3. Suma de 0.00001 con doble precisión (float64)
# ==========================================
suma3_doble = 0.0  # float64 por defecto en Python
for _ in range(N):
    suma3_doble += 0.00001

error3 = abs(suma3_doble - valor_esperado2)

print("\n--- SUMA DE 0.00001 (float64) ---")
print(f"Valor calculado: {suma3_doble}")
print(f"Valor esperado:  {valor_esperado2}")
print(f"Error absoluto:  {error3:.10f}")
print(f"Error relativo:  {error3/valor_esperado2:.10e}")

# ==========================================
# ANÁLISIS COMPARATIVO
# ==========================================
print("\n" + "="*50)
print("ANÁLISIS DE RESULTADOS")
print("="*50)

print(f"\n1. Suma de 1 (float32):")
print(f"   ✓ Error prácticamente nulo: {error1}")
print(f"   Razón: 1 es representable exactamente en float32")

print(f"\n2. Suma de 0.00001 (float32):")
print(f"   ✗ Error significativo: {error2:.6f}")
print(f"   Razón: 0.00001 NO es representable exactamente en binario")
print(f"   El error se acumula en {N:,} sumas")

print(f"\n3. Suma de 0.00001 (float64):")
print(f"   ✓ Error mucho menor: {error3:.10f}")
print(f"   Razón: Mayor precisión reduce (pero no elimina) el error")

print(f"\n4. Comparación float32 vs float64:")
print(f"   Mejora: {error2/error3:.2f}x menos error con float64")

# ==========================================
# DEMOSTRACIÓN ADICIONAL: Forma óptima
# ==========================================
print("\n" + "="*50)
print("MÉTODO ÓPTIMO (sin acumulación de error)")
print("="*50)

# Calcular directamente sin bucle
suma_optima = N * 0.00001
print(f"Valor calculado: {suma_optima}")
print(f"Error: prácticamente cero (una sola operación)")