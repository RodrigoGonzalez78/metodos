import math

def serie_ex(x, n):
    """
    Devuelve los n primeros términos de la serie de e^x.
    """
    terminos = []
    for k in range(n):
        term = x**k / math.factorial(k)
        terminos.append(term)
    return terminos

# Ejemplo de uso
x = 2
n = 10
terminos = serie_ex(x, n)
print(f"Primeros {n} términos de e^{x}:")
for i, t in enumerate(terminos):
    print(f"Término {i}: {t}")
    
# Suma aproximada de e^x
aprox = sum(terminos)
print(f"\nAproximación de e^{x} sumando los {n} términos: {aprox}")
