# Medición 1: Folio
real1 = 29.6
medido1 = 30.0

# Medición 2: Pupitre
real2 = 65.0
medido2 = 65.4

# Errores absolutos
error_abs1 = abs(real1 - medido1)
error_abs2 = abs(real2 - medido2)

# Errores relativos
error_rel1 = error_abs1 / real1
error_rel2 = error_abs2 / real2

# Mostrar resultados
print("=== MEDICIÓN DEL FOLIO ===")
print(f"Valor real: {real1} cm")
print(f"Valor medido: {medido1} cm")
print(f"Error absoluto: {error_abs1} cm")
print(f"Error relativo: {error_rel1:.5f} ({error_rel1*100:.3f}%)")

print("\n=== MEDICIÓN DEL PUPITRE ===")
print(f"Valor real: {real2} cm")
print(f"Valor medido: {medido2} cm")
print(f"Error absoluto: {error_abs2} cm")
print(f"Error relativo: {error_rel2:.5f} ({error_rel2*100:.3f}%)")

# Comparación de precisión
print("\n=== COMPARACIÓN ===")
if error_rel1 < error_rel2:
    print("✓ La medida del FOLIO es más precisa.")
    print(f"Razón: Tiene menor error relativo ({error_rel1:.5f} < {error_rel2:.5f})")
else:
    print("✓ La medida del PUPITRE es más precisa.")
    print(f"Razón: Tiene menor error relativo ({error_rel2:.5f} < {error_rel1:.5f})")
