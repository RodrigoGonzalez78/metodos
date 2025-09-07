def error_relativo(medida, error):
    """
    Calcula el error relativo como fracción (no en %)
    medida : valor real de la medida
    error  : error absoluto cometido
    """
    return error / medida

# Datos
medida1 = 1        # 1 metro
error1 = 0.001     # 1 mm = 0.001 m

medida2 = 300_000  # 300 km = 300000 m
error2 = 300       # 300 m

# Cálculo errores relativos
er1 = error_relativo(medida1, error1)
er2 = error_relativo(medida2, error2)

print(f"Error relativo en 1 m: {er1*100:.3f}%")
print(f"Error relativo en 300 km: {er2*100:.3f}%")

# Comparación
if er1 > er2:
    print("El error relativo mayor ocurre en la medida de 1 m.")
elif er2 > er1:
    print("El error relativo mayor ocurre en la medida de 300 km.")
else:
    print("Ambos errores relativos son iguales.")
