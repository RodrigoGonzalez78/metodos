import math

def resolvente(a, b, c):
    
    delta = b**2 - 4*a*c
    
    if delta < 0:
        return None
    sqrt_delta = math.sqrt(delta)
    x1 = (-b + sqrt_delta) / (2*a)
    x2 = (-b - sqrt_delta) / (2*a)
    return x1, x2

# Casos
raices1 = resolvente(1, 108, 1)
raices2 = resolvente(1, 108, 108)

print("Raíces cuando c = 1:", raices1)
print("Raíces cuando c = 108:", raices2)
