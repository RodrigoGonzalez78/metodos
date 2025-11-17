import numpy as np

def ingresar_matriz():
    """Solicita al usuario ingresar una matriz cuadrada"""
    n = int(input("Ingrese el tamaño de la matriz (n x n): "))
    A = np.zeros((n, n))
    print("Ingrese los elementos de la matriz fila por fila:")
    for i in range(n):
        fila = input(f"Fila {i+1} separada por espacios: ").strip().split()
        A[i] = [float(x) for x in fila]
    return A.astype(float) # Asegurar que sea float


def metodo_faddeev_leverrier(A):
    """
    Aplica el método de Faddeev-Leverrier para encontrar:
    - Coeficientes del polinomio característico
    - Autovalores (raíces del polinomio)
    - Matriz inversa (si existe)
    
    Args:
        A: Matriz cuadrada numpy array
        
    Returns:
        dict: Diccionario con coeficientes, autovalores y matriz inversa
    """
    n = A.shape[0]
    I = np.eye(n)
    B_prev = A.copy()
    b = []
    B_matrices = [A.copy()]  # Guardar todas las matrices B
    
    print("\n" + "=" * 70)
    print("MÉTODO DE FADDEEV–LEVERRIER")
    print("=" * 70)

    # Primer coeficiente
    b1 = np.trace(B_prev)
    b.append(b1)
    print(f"\n{'─' * 70}")
    print("Iteración 1:")
    print(f"{'─' * 70}")
    print(f"B₁ = A")
    print(B_prev)
    print(f"\nb₁ = tr(B₁) = {b1:.6f}")

    # Iteraciones para k = 2, ..., n
    for k in range(2, n + 1):
        # Esta es la formulación B_k = A(B_{k-1} - b_{k-1}I)
        Bk = np.dot(A, B_prev - b[-1] * I)
        bk = np.trace(Bk) / k
        b.append(bk)
        B_matrices.append(Bk.copy())
        
        print(f"\n{'─' * 70}")
        print(f"Iteración {k}:")
        print(f"{'─' * 70}")
        print(f"B₍{k}₎ = A × (B₍{k-1}₎ - b₍{k-1}₎×I)")
        print(Bk)
        print(f"\nb₍{k}₎ = tr(B₍{k}₎) / {k} = {bk:.6f}")
        B_prev = Bk

    # Construir coeficientes del polinomio característico
    # p(λ) = λⁿ - b₁λⁿ⁻¹ - b₂λⁿ⁻² - ... - bₙ
    # Los coeficientes c_k son -b_k
    coef_poly = [1]  # coeficiente de λⁿ
    for i in range(n):
        coef_poly.append(-b[i])
    
    print("\n" + "=" * 70)
    print("POLINOMIO CARACTERÍSTICO")
    print("=" * 70)
    print("\nCoeficientes [λⁿ, λⁿ⁻¹, ..., λ¹, λ⁰]:")
    print(coef_poly)
    
    # Mostrar polinomio en formato legible
    print("\nPolinomio característico p(λ) = det(λI - A):") 
    terms = []
    for i, c in enumerate(coef_poly):
        power = n - i
        if c == 0:
            continue
        # Formateo para que se vea bien
        term = ""
        if i > 0:
            term += f"{'+' if c > 0 else '-'} {abs(c):.6f}"
        else:
             if c == 1:
                term = ""
             elif c == -1:
                term = "-"
             else:
                term = f"{c:.6f}"

        if power == 0:
            terms.append(term)
        elif power == 1:
            terms.append(f"{term}λ")
        else:
            if abs(c) == 1 and i > 0:
                term = f"{'+' if c > 0 else '-'}"
            elif abs(c) == 1 and i == 0:
                term = ""
                
            terms.append(f"{term}λ^{power}")
    
    poly_str = " ".join(terms).strip()
    if poly_str.startswith("+"):
        poly_str = poly_str[1:].strip()
    print(f"p(λ) = {poly_str}")

    # Calcular autovalores (raíces del polinomio)
    print("\n" + "=" * 70)
    print("AUTOVALORES")
    print("=" * 70)
    autovalores = np.roots(coef_poly)
    autovalores_ordenados = np.sort(autovalores)[::-1] # Ordenar de mayor a menor
    autovalores = autovalores_ordenados

    print("\nAutovalores (raíces del polinomio característico):")
    for i, eigenval in enumerate(autovalores):
        if np.isreal(eigenval):
            print(f"  λ₍{i+1}₎ = {eigenval.real:.8f}")
        else:
            print(f"  λ₍{i+1}₎ = {eigenval.real:.8f} {eigenval.imag:+.8f}i")
    
    # Calcular matriz inversa usando Faddeev-Leverrier
    print("\n" + "=" * 70)
    print("MATRIZ INVERSA")
    print("=" * 70)
    
    # CORRECCIÓN: El polinomio es p(λ) = det(λI - A).
    # p(0) = det(-A) = (-1)ⁿ det(A) = cₙ (el término constante)
    # Por lo tanto, det(A) = (-1)ⁿ * cₙ
    
    # n ya está definida al inicio de la función
    det_A = ((-1)**n) * coef_poly[-1]
    
    print(f"\nDeterminante de A: det(A) = (-1)ⁿ × cₙ = {det_A:.6f}")
    
    if abs(det_A) < 1e-10:
        print("⚠️  La matriz es singular (det(A) ≈ 0), no tiene inversa.")
        A_inv = None
    else:
        # La fórmula de la inversa usa B_{n-1} y b_{n-1}
        # adj(A) = B_{n-1} - b_{n-1} * I
        # A⁻¹ = (1 / det(A)) * adj(A)
        
        # b[-1] es b_n, b[-2] es b_{n-1}
        b_n_minus_1 = b[-2]
        # B_matrices[-1] es B_n, B_matrices[-2] es B_{n-1}
        B_n_minus_1 = B_matrices[-2]
        
        matriz_adjunta = B_n_minus_1 - b_n_minus_1 * I
        A_inv = (1 / det_A) * matriz_adjunta
        
        print("\nMatriz inversa A⁻¹ = (1/det(A)) × (B₍n-1₎ - b₍n-1₎×I):")
        print(A_inv)
        
        # Verificar A × A⁻¹ = I
        producto = np.dot(A, A_inv)
        print("\nVerificación A × A⁻¹ (debería ser I):")
        print(np.round(producto, 6)) # Redondear para legibilidad
        error = np.linalg.norm(producto - I)
        print(f"Error ||A×A⁻¹ - I||: {error:.2e}")

    return {
        'coeficientes': coef_poly,
        'autovalores': autovalores,
        'determinante': det_A,
        'inversa': A_inv,
        'B_matrices': B_matrices,
        'b_coeficientes': b
    }


def calcular_autovectores(A, autovalores):
    """
    Calcula los autovectores asociados a cada autovalor
    resolviendo (A - λI)v = 0 usando SVD.
    
    Args:
        A: Matriz cuadrada
        autovalores: Array con los autovalores
        
    Returns:
        list: Lista de autovectores (uno por cada autovalor)
    """
    n = A.shape[0]
    I = np.eye(n)
    autovectores = []
    
    print("\n" + "=" * 70)
    print("AUTOVECTORES")
    print("=" * 70)
    
    for i, eigenval in enumerate(autovalores):
        print(f"\n{'─' * 70}")
        print(f"Autovector {i+1} para λ₍{i+1}₎ = {eigenval:.8f}")
        print(f"{'─' * 70}")
        
        # Calcular el autovector resolviendo el sistema
        # (A - λI)v = 0. Esto es encontrar el espacio nulo (kernel)
        # de la matriz (A - λI).
        
        # Asegurarse de que A y I sean complejos si el autovalor lo es
        A_complex = A.astype(complex)
        I_complex = I.astype(complex)
        
        # Crear la matriz M = (A - λI)
        matriz_reducida = A_complex - eigenval * I_complex
        
        print(f"\nMatriz (A - λI):")
        print(matriz_reducida)
        
        # Usar SVD (Descomposición de Valores Singulares) para encontrar 
        # el espacio nulo.
        try:
            u, s, vh = np.linalg.svd(matriz_reducida)
            
            # vh es V^H (conjugado transpuesto). La última fila es el
            # vector que buscamos (como v^H).
            # Lo conjugamos para obtener el autovector 'v'.
            autovector = vh[-1, :].conj()
            
            print(f"\nAutovector normalizado v₍{i+1}₎:")
            for j, componente in enumerate(autovector):
                if np.isreal(componente) and abs(componente.imag) < 1e-10:
                    print(f"  v[{j+1}] = {componente.real:.8f}")
                else:
                    print(f"  v[{j+1}] = {componente.real:.8f} {componente.imag:+.8f}i")
            
            # Verificar A×v = λ×v
            Av = np.dot(A_complex, autovector)
            lambda_v = eigenval * autovector
            error = np.linalg.norm(Av - lambda_v)
            
            print(f"\nVerificación A×v = λ×v:")
            print(f"Error ||A×v - λ×v||: {error:.2e}")
            
            if error < 1e-6:
                print("✅ Autovector verificado correctamente")
            else:
                print("⚠️  Advertencia: Error significativo en la verificación")
            
            autovectores.append(autovector)
            
        except Exception as e:
            print(f"⚠️  Error al calcular autovector con SVD: {e}")
            autovectores.append(None)
    
    return autovectores


def main():
    print("=" * 70)
    print("MÉTODO DE FADDEEV–LEVERRIER")
    print("Calcula: Polinomio característico, Autovalores,")
    print("         Autovectores y Matriz Inversa")
    print("=" * 70)
    
    # Ingresar matriz
    A = ingresar_matriz()
    
    print("\n📊 Matriz ingresada A:")
    print(A)
    
    # Aplicar método de Faddeev-Leverrier
    resultados = metodo_faddeev_leverrier(A)
    
    # Calcular autovectores
    autovectores = calcular_autovectores(A, resultados['autovalores'])
    resultados['autovectores'] = autovectores
    
    # Resumen final conciso
    print("\n" + "=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    
    print("\n📊 AUTOVALORES (Ordenados de mayor a menor):")
    for i, eigenval in enumerate(resultados['autovalores']):
        if np.isreal(eigenval):
            print(f"  λ₍{i+1}₎ = {eigenval.real:.8f}")
        else:
            print(f"  λ₍{i+1}₎ = {eigenval.real:.8f} {eigenval.imag:+.8f}i")
    
    print("\n📐 AUTOVECTORES NORMALIZADOS:")
    for i, autovector in enumerate(autovectores):
        if autovector is not None:
            # Asociar por índice (ambos están ordenados)
            print(f"\n  v₍{i+1}₎ asociado a λ₍{i+1}₎ = {resultados['autovalores'][i].real:.4f}:")
            
            # Limpiar componentes imaginarios muy pequeños para impresión
            cleaned_vec = autovector.copy()
            for j in range(len(cleaned_vec)):
                if abs(cleaned_vec[j].imag) < 1e-10:
                    cleaned_vec[j] = complex(cleaned_vec[j].real, 0)
                if abs(cleaned_vec[j].real) < 1e-10:
                    cleaned_vec[j] = complex(0, cleaned_vec[j].imag)
            
            if np.all(np.isreal(cleaned_vec)):
                vec_str = "  [" + ", ".join([f"{x.real:.6f}" for x in cleaned_vec]) + "]"
            else:
                vec_str = "  [" + ", ".join([f"{x.real:.6f}{x.imag:+.6f}i" if not np.isreal(x) else f"{x.real:.6f}" for x in cleaned_vec]) + "]"
            print(vec_str)
    
    print(f"\n📏 Determinante: {resultados['determinante']:.6f}")
    if resultados['inversa'] is not None:
        print(f"✓ Matriz invertible")
    else:
        print(f"✗ Matriz singular (no invertible)")


if __name__ == "__main__":
    main()