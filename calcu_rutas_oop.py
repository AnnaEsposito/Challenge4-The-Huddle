class Mapa:
    def __init__(self, alto, ancho):
        self.alto = alto
        self.ancho = ancho
        self.mapa = self.crear_mapa()

    def crear_mapa(self):
        return [[0 for _ in range(self.ancho)] for _ in range(self.alto)]

    def agregar_obstaculo(self, x, y, tipo_obstaculo):
        if 0 <= x < self.alto and 0 <= y < self.ancho:
            self.mapa[x][y] = tipo_obstaculo

    def quitar_obstaculo(self, x, y):
        if 0 <= x < self.alto and 0 <= y < self.ancho:
            self.mapa[x][y] = 0

    def es_valido(self, nodo):
        x, y = nodo
        return 0 <= x < self.alto and 0 <= y < self.ancho and self.mapa[x][y] == 0

    def mostrar_mapa(self):
        for fila in self.mapa:
            print(" ".join(map(str, fila)))

class CalculadoraDeRutas:
    def __init__(self, mapa):
        self.mapa = mapa
        self.movimientos_posibles = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def estimacion_g(self, valor_g):
        return valor_g + 1  # Costo uniforme de moverse a un nodo adyacente

    def estimacion_h(self, nodo_actual, nodo_meta):
        return abs(nodo_actual[0] - nodo_meta[0]) + abs(nodo_actual[1] - nodo_meta[1])

    def estimacion_f(self, valor_g, valor_h):
        return valor_g + valor_h

    def algoritmo_A_estrella(self, inicio, meta):
        lista_nodos_abiertos = []
        lista_nodos_cerrados = set()
        diccionario_nodo_padre = {}

        valor_g_inicial = 0
        lista_nodos_abiertos.append((inicio, valor_g_inicial))
        diccionario_nodo_padre[inicio] = None

        while lista_nodos_abiertos:
            lista_nodos_abiertos.sort(key=lambda nodo: nodo[1])
            nodo_actual, valor_g = lista_nodos_abiertos.pop(0)

            if nodo_actual == meta:
                camino = []
                while nodo_actual is not None:
                    camino.append(nodo_actual)
                    nodo_actual = diccionario_nodo_padre[nodo_actual]
                return camino[::-1]  # Ruta desde inicio hasta meta

            lista_nodos_cerrados.add(nodo_actual)

            for mov in self.movimientos_posibles:
                nodo_adyacente = (nodo_actual[0] + mov[0], nodo_actual[1] + mov[1])

                if nodo_adyacente in lista_nodos_cerrados or not self.mapa.es_valido(nodo_adyacente):
                    continue

                valor_g_adyacente = self.estimacion_g(valor_g)
                valor_h = self.estimacion_h(nodo_adyacente, meta)
                f = self.estimacion_f(valor_g_adyacente, valor_h)

                if nodo_adyacente not in [nodo for nodo, _ in lista_nodos_abiertos]:
                    lista_nodos_abiertos.append((nodo_adyacente, f))
                    diccionario_nodo_padre[nodo_adyacente] = nodo_actual
                else:
                    for i, (coord, viejo_f) in enumerate(lista_nodos_abiertos):
                        if coord == nodo_adyacente and f < viejo_f:
                            lista_nodos_abiertos[i] = (nodo_adyacente, f)
                            lista_nodos_abiertos.sort(key=lambda nodo: nodo[1])
                            diccionario_nodo_padre[nodo_adyacente] = nodo_actual

        return None

    def marcar_camino(self, camino, inicio, meta):
        for (x, y) in camino:
            if (x, y) != inicio and (x, y) != meta:
                self.mapa.mapa[x][y] = 'c'

        self.mapa.mapa[inicio[0]][inicio[1]] = 'I'
        self.mapa.mapa[meta[0]][meta[1]] = 'M'


def main():
    alto = 10
    ancho = 10

    # Crear mapa
    mapa = Mapa(alto, ancho)

    # Solicitar obstáculos
    num_obstaculos = int(input("Ingrese el número de obstáculos: "))
    for _ in range(num_obstaculos):
        x = int(input("Ingrese la coordenada x del obstáculo: "))
        y = int(input("Ingrese la coordenada y del obstáculo: "))
        tipo_obstaculo = int(input("Ingrese el tipo de obstáculo (1 o 2): "))
        mapa.agregar_obstaculo(x, y, tipo_obstaculo)

    # Mostrar el mapa inicial
    print("Mapa inicial:")
    mapa.mostrar_mapa()

    # Solicitar puntos de inicio y meta
    inicio_x = int(input("Ingrese la coordenada x del punto de inicio: "))
    inicio_y = int(input("Ingrese la coordenada y del punto de inicio: "))
    inicio = (inicio_x, inicio_y)

    meta_x = int(input("Ingrese la coordenada x del punto de llegada: "))
    meta_y = int(input("Ingrese la coordenada y del punto de llegada: "))
    meta = (meta_x, meta_y)

    # Crear calculadora de rutas
    calculadora = CalculadoraDeRutas(mapa)

    # Ejecutar el algoritmo A*
    camino = calculadora.algoritmo_A_estrella(inicio, meta)

    if camino:
        # Marcar el camino en el mapa
        calculadora.marcar_camino(camino, inicio, meta)

        # Mostrar el mapa con la ruta resuelta
        print("Mapa con la ruta resuelta:")
        mapa.mostrar_mapa()
    else:
        print("No se encontró una ruta desde el inicio hasta la meta.")

if __name__ == "__main__":
    main()
