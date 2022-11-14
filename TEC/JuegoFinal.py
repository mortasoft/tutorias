import random
import datetime


class Jugador():
    def __init__(self,nombre) -> None:
        self.intentos_totales = random.randint(12,18)
        self.intentos = 0
        self.nombre = nombre
        self.matriz_jugador = []
        self.puntos_positivos = 0
        self.puntos_negativos = 0
        self.trono = 0
        self.pierde = 0
        self.estado = ''
        self.tipo_gane =''
    

    def inicializarTableroJugador(self, tamano_tablero):

        for fila in range(tamano_tablero):
            fila= []
            
            for columna in range(tamano_tablero):
                fila.append(' ')

            self.matriz_jugador.append(fila)


    def print_tablero(self):

        print("   ", end=" ")
        cont=0
          
        for i in range(len(self.matriz_jugador)):
            print(f"  {str(i).rjust(3)}  ", end=" ")
        print()

        for row in self.matriz_jugador:
            print(f"  {cont}", end=" ")
            for val in row:
                print(f"  {str(val).rjust(3)}  ", end=" ")
            print()   
            cont = cont+1


class Tablero():
    def __init__(self) -> None:
        self.matriz_tablero = []
        self.puntos_positivos = 0
        self.puntos_negativos = 0
        self.porcentaje_premios_5pt = 0.30
        self.porcentaje_premios_10pt = 0.15
        self.inicializarTablero()


    def inicializarTablero(self):
        self.tamano_tablero = random.randint(8,10)
        distribucion_celdas = self.calcular_distribucion_celdas(self.tamano_tablero)

        for fila in range(self.tamano_tablero):
            fila= []
            
            for columna in range(self.tamano_tablero):
                valor = self.obtener_celda_aleatoria(distribucion_celdas)
                fila.append(valor)

            self.matriz_tablero.append(fila)
    

    def calcular_distribucion_celdas(self,tamano_matriz):
        cantidad_espacios = tamano_matriz * tamano_matriz
        premios5pt = round(cantidad_espacios*self.porcentaje_premios_5pt)
        premios10pt = round(cantidad_espacios*self.porcentaje_premios_10pt) 
        cuevas5pt = round(cantidad_espacios*self.porcentaje_premios_5pt)
        cuevas10pt = round(cantidad_espacios*self.porcentaje_premios_10pt)
        pierde = 1
        gana = 1
        ceros = cantidad_espacios - premios5pt - premios10pt - cuevas5pt - cuevas10pt - pierde - gana

        self.puntos_positivos = (premios5pt * 5)  +  (premios10pt * 10) 
        self.puntos_negativos = (cuevas5pt * 5)  +  (cuevas10pt * 10)

        return { "premios5pt": [premios5pt,5], "premios10pt": [premios10pt,10], "cuevas5pt": [cuevas5pt,-5], "cuevas10pt": [cuevas10pt,-10], "pierde" : [pierde,"p"], "gana": [gana,"g"], "ceros":[ceros,0] } 


    def obtener_celda_aleatoria(self,distribucion):      
        tipo,cantidad = random.choice(list(distribucion.items()))
        if cantidad[0] > 0:
            distribucion[tipo][0] = distribucion[tipo][0] -1
            val =  distribucion[tipo][1]
            return val
        else:
            return self.obtener_celda_aleatoria(distribucion)
    

    def print_tablero(self):

        print("   ", end=" ")
        cont=0
          
        for i in range(len(self.matriz_tablero)):
            print(f"  {str(i).rjust(3)}  ", end=" ")
        print()

        for row in self.matriz_tablero:
            print(f"  {cont}", end=" ")
            for val in row:
                print(f"  {str(val).rjust(3)}  ", end=" ")
            print()   
            cont = cont+1


def main():
    print("Bienvenido(a) al juego el trono de Jokander. \n")
    print("Existe un reino, Jokander, con un trono que todos quieren obtener. Tú debes explorar el territorio para obtener puntos y ganar el reino. El reino, dividido en territorios desde el aire, se observa como un tablero de 8x8, 9x9 o 10x10 terrenos, a los cuales debes viajar ingresando las coordenadas de territorio deseado. \n")
    print("Las reglas consisten en lo siguiente: \n")
    print("1. Las coordenadas van desde la posición (1,1) hasta (8,8), (9,9) o (10,10), dependiendo de las dimensiones del tablero.")
    print("2. Tiene de 12 a 18 intentos de juego, de los cuales se escogen de manera aleatoria.")
    print("3. Si repite una coordenada, automáticamente pierde un intento.")
    print("4. Se gana cuando se obtiene el 50% del total de numeros positivos del juego o cuando se encuentra el gran premio.")
    print("5. Se pierde cuando se el 50% del total de numeros negativos del juego o cuando se encuentra con la gran decepción. \n")
    nombre=str(input("Introduzca su nombre: "))
    jugador1 = Jugador(nombre)
    print("Tienes", jugador1.intentos_totales,"intentos.  ¡Que comience el juego!")
    tablero1 = Tablero()
    print("Tamaño de la matriz: ", tablero1.tamano_tablero )
    jugador1.inicializarTableroJugador(tablero1.tamano_tablero)
    tablero1.print_tablero()
    jugar(jugador1, tablero1) 
    


def jugar(jugador,tablero):
    while(verificarGane(jugador,tablero)):
        jugador.print_tablero()
        print("Intentos restantes: ",jugador.intentos_totales - jugador.intentos)
        try:
            posicion=str(input("Digite una posicion (Ejemplo: 1,1 ) ")).split(",")
            fila = int(posicion[0])
            columna = int(posicion[1])
            if(validarCoordenadas(fila,columna,len(tablero.matriz_tablero))):
                resultado = tablero.matriz_tablero[fila][columna]
                if resultado == 'g':
                    jugador.trono = resultado
                elif resultado == 'p':
                    jugador.pierde = resultado
                elif jugador.matriz_jugador[fila][columna] != " ":
                    print("El jugador ya habia seleccionado esa casilla")
                elif resultado == 0:
                    print("No gano puntos.")
                elif resultado > 1:
                    jugador.puntos_positivos = jugador.puntos_positivos + resultado
                    print("Gano ",resultado," puntos!")
                elif resultado < 1:
                    jugador.puntos_negativos = jugador.puntos_negativos + resultado
                    print("Perdio ",resultado," puntos!")
                jugador.matriz_jugador[fila][columna] = resultado
                jugador.intentos = jugador.intentos + 1
            else:
                print("Debe digitar una coordenada valida")
        except Exception as e:
            print("Debe digitar una coordenada valida")
            jugador.intentos = jugador.intentos + 1
    print("Juego finalizado")
    volverJugar=str(input("Quiere volver a jugar? S/N - "))
    if volverJugar.lower() == 's':
        main()
    else:
        f = open("Juegos.dat", "a")
        salida = f"{jugador.nombre},{datetime.datetime.now()},{jugador.puntos_positivos},{jugador.puntos_negativos},{jugador.estado},{jugador.tipo_gane}"
        f.write(salida)
        f.close()



def validarCoordenadas(fila,columna,tamano):
    if str(fila).isnumeric() and str(columna).isnumeric() and fila >= 0 and fila < tamano and columna >= 0 and columna < tamano:
        return True
    else:
        return False


def verificarGane(jugador,tablero):

    if jugador.trono == 'g':
        print("Gano por adivinar la posicion del trono")
        jugador.estado = "Gano"
        jugador.tipo_gane = "Emergente"
        return False
    
    if jugador.pierde == 'p':
        print("Perdio!!!!")
        jugador.estado = "Perdio"
        jugador.tipo_gane = "Emergente"
        return False

    if jugador.intentos == jugador.intentos_totales:
        print("Se acabaron los turnos")
        jugador.estado = "Perdio"
        jugador.tipo_gane = "Turnos terminados"
        return False

    if jugador.puntos_positivos >= tablero.puntos_positivos*0.5:
        print("Gano por acumular mas del 50% de los puntos")
        jugador.estado = "Gano"
        jugador.tipo_gane = "Por puntos"
        return False
    
    if jugador.puntos_negativos >= tablero.puntos_negativos*0.5:
        print("Perdio por acumular mas del 50% de los puntos negativos")
        jugador.estado = "Perdio"
        jugador.tipo_gane = "Por puntos"
        return False


    # Sigue jugando    
    return True

main() 
