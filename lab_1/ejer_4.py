import math

def calcular_raices(a, b, c):
    """Calcula las raíces de la ecuación cuadrática ax^2 + bx + c = 0"""
    discriminante = b**2 - 4*a*c
    
    if discriminante < 0:
        return None  # No tiene raíces reales
    elif discriminante == 0:
        x = -b / (2*a)
        return (x,)  # Una sola raíz
    else:
        x1 = (-b + math.sqrt(discriminante)) / (2*a)
        x2 = (-b - math.sqrt(discriminante)) / (2*a)
        return (x1, x2)

def main():
    print("Ecuación cuadrática: ax^2 + bx + c = 0")
    a = float(input("Ingrese el valor de a: "))
    b = float(input("Ingrese el valor de b: "))
    c = float(input("Ingrese el valor de c: "))

    raices = calcular_raices(a, b, c)

    if raices is None:
        print("La ecuación no tiene raíces reales.")
    elif len(raices) == 1:
        print(f"La ecuación tiene una raíz: x = {raices[0]}")
    else:
        print(f"La ecuación tiene dos raíces: x1 = {raices[0]}, x2 = {raices[1]}")

# Ejecutar
if __name__ == "__main__":
    main()

