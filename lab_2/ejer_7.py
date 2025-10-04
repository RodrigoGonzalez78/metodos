import math

print("=== CONVERGENCIA DE LA SERIE ∑(1/n²) ===\n")

N = 10000

# Valor teórico (límite cuando N→∞)
valor_teorico = (math.pi**2) / 6

# ==========================================
# 1. SUMA DIRECTA (1 → 10000)
# ==========================================
suma_directa = 0.0
for i in range(1, N+1):
    suma_directa += 1 / (i**2)

# También se puede usar:
# suma_directa = sum(1 / (i**2) for i in range(1, N+1))

error_directa = abs(suma_directa - valor_teorico)

# ==========================================
# 2. SUMA INVERSA (10000 → 1)
# ==========================================
suma_inversa = 0.0
for i in range(N, 0, -1):
    suma_inversa += 1 / (i**2)

# También se puede usar:
# suma_inversa = sum(1 / (i**2) for i in range(N, 0, -1))

error_inversa = abs(suma_inversa - valor_teorico)

# ==========================================
# MOSTRAR RESULTADOS
# ==========================================
print("--- RESULTADOS ---")
print(f"Suma DIRECTA (1→{N}):     {suma_directa:.15f}")
print(f"Suma INVERSA ({N}→1):     {suma_inversa:.15f}")
print(f"Valor teórico (π²/6):     {valor_teorico:.15f}")

print("\n--- ERRORES ---")
print(f"Error suma directa:  {error_directa:.15e}")
print(f"Error suma inversa:  {error_inversa:.15e}")

diferencia = abs(suma_directa - suma_inversa)
print(f"\nDiferencia entre ambas sumas: {diferencia:.15e}")

# ==========================================
# ANÁLISIS Y EXPLICACIÓN
# ==========================================
print("\n" + "="*60)
print("EXPLICACIÓN DE LOS RESULTADOS")
print("="*60)

if suma_inversa < suma_directa:
    mejor = "INVERSA"
    print(f"\n✓ La suma INVERSA es MÁS PRECISA")
else:
    mejor = "DIRECTA"
    print(f"\n✓ La suma DIRECTA es MÁS PRECISA")

print(f"\n¿POR QUÉ?")
print(f"───────────────────────────────────────────────────────────")
print(f"1. PÉRDIDA DE PRECISIÓN POR MAGNITUDES:")
print(f"   - Al sumar números de magnitudes MUY diferentes,")
print(f"     los números pequeños pueden 'perderse'")
print(f"   - Ejemplo: 1.644934 + 0.0000001 ≈ 1.644934 (pérdida)")

print(f"\n2. SUMA DIRECTA (1→{N}):")
print(f"   - Empieza con: 1/1² = 1.0 (grande)")
print(f"   - Termina con: 1/10000² = 0.00000001 (muy pequeño)")
print(f"   - Los términos pequeños se suman a un acumulador GRANDE")
print(f"   - Resultado: Mayor pérdida de precisión")

print(f"\n3. SUMA INVERSA ({N}→1):")
print(f"   - Empieza con: 1/10000² = 0.00000001 (muy pequeño)")
print(f"   - Acumula términos pequeños primero")
print(f"   - Suma términos grandes al final")
print(f"   - Resultado: Mejor precisión numérica")

print(f"\n4. CONCLUSIÓN:")
print(f"   ⚠ SIEMPRE sumar de MENOR a MAYOR para minimizar errores")
print(f"   ⚠ Este es un problema clásico de ESTABILIDAD NUMÉRICA")

# ==========================================
# DEMOSTRACIÓN VISUAL
# ==========================================
print("\n" + "="*60)
print("DEMOSTRACIÓN CON PRIMEROS TÉRMINOS")
print("="*60)

print("\nPrimeros 5 términos:")
for i in range(1, 6):
    termino = 1 / (i**2)
    print(f"  1/{i}² = {termino:.10f}")

print("\nÚltimos 5 términos:")
for i in range(N-4, N+1):
    termino = 1 / (i**2)
    print(f"  1/{i}² = {termino:.15e}")

print(f"\nNota: Los últimos términos son ~{(1/1**2)/(1/N**2):.0e}x más pequeños")