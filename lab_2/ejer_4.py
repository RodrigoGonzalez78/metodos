# Medida 1: 1 metro con error de 1 milímetro
medida1 = 1          # en metros
error_abs1 = 0.001   # 1 mm = 0.001 m

# Medida 2: 300 kilómetros con error de 300 metros
medida2 = 300000     # 300 km = 300000 m
error_abs2 = 300     # 300 m

# Errores relativos
error_rel1 = error_abs1 / medida1
error_rel2 = error_abs2 / medida2

# Mostrar resultados
print("=== MEDIDA 1 ===")
print(f"Medida: 1 m")
print(f"Error absoluto: 1 mm = {error_abs1} m")
print(f"Error relativo: {error_rel1} = {error_rel1*100:.3f}%")

print("\n=== MEDIDA 2 ===")
print(f"Medida: 300 km = {medida2} m")
print(f"Error absoluto: 300 m")
print(f"Error relativo: {error_rel2} = {error_rel2*100:.3f}%")

# Comparación
print("\n=== COMPARACIÓN ===")
if error_rel1 > error_rel2:
    print(f"✓ El error relativo es MAYOR en la medida de 1 m")
    print(f"  ({error_rel1} > {error_rel2})")
else:
    print(f"✓ El error relativo es MAYOR en la medida de 300 km")
    print(f"  ({error_rel2} > {error_rel1})")
