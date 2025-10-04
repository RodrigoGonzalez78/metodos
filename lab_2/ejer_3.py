import math

def resolver_cuadratica(a, b, c):
    D = b**2 - 4*a*c
    if D < 0:
        return None
    x1 = (-b + math.sqrt(D)) / (2*a)
    x2 = (-b - math.sqrt(D)) / (2*a)
    return x1, x2

casos = [1, 108]
for c in casos:
    x1, x2 = resolver_cuadratica(1, 108, c)
    print(f"Para c = {c}: x1 = {x1:.6f}, x2 = {x2:.6f}")

