import tanteos.tanteos as tnt
import 

if __name__ == "__main__":
    tnt.Metodo_tanteo(lambda x: x**3 - 6*x**2 + 11*x - 6, x_min=0, x_max=4, paso=0.1)
    tnt.graficar_funcion_con_intervalos(lambda x: x**3 - 6*x**2 + 11*x - 6, [(2.0, 3.0), (3.0, 4.0)], x_min=0, x_max=4)