def evaluar_medidas(medidas):
    resultados = []
    for nombre, real, medido in medidas:
        error_abs = abs(medido - real)
        error_rel = error_abs / real
        resultados.append((nombre, real, medido, error_abs, error_rel))
    return resultados

# (nombre, valor real, valor medido)
medidas = [
    ("Folio", 29.6, 30.0),
    ("Pupitre", 65.0, 65.4)
]

resultados = evaluar_medidas(medidas)

for nombre, real, medido, e_abs, e_rel in resultados:
    print(f"{nombre}:")
    print(f"  Valor real     = {real} cm")
    print(f"  Valor medido   = {medido} cm")
    print(f"  Error absoluto = {e_abs:.2f} cm")
    print(f"  Error relativo = {e_rel*100:.2f} %")
    print()

# Comparación de precisión
mas_precisa = min(resultados, key=lambda x: x[4])  # menor error relativo
print(f"La medida más precisa es la del {mas_precisa[0]} "
      f"porque tiene menor error relativo ({mas_precisa[4]*100:.2f}%).")
