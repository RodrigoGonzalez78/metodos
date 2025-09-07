from math import pi, e

# valores reales
true_value = pi / e

# redondeados a 6 decimales
pi6 = round(pi, 6)
print(pi6)
e6 = round(e, 6)
print(e6)
approx_value = pi6 / e6

print("Valor real:     ", true_value)
print("Valor aproximado:", approx_value)


true_str = f"{true_value:.12f}"
approx_str = f"{approx_value:.12f}"


sig = 0
for t, a in zip(true_str.replace(".", ""), approx_str.replace(".", "")):
    if t == a:
        sig += 1
    else:
        break

dec = 0
for t, a in zip(true_str.split(".")[1], approx_str.split(".")[1]):
    if t == a:
        dec += 1
    else:
        break

print("Dígitos significativos correctos:", sig)
print("Decimales correctos:", dec)
