import heapq

def calcular_area_accesible(x, y, ancho_matriz, alto_matriz, obstaculos):
    def es_valido(x, y):
        return 1 <= x <= ancho_matriz and 1 <= y <= alto_matriz and (x, y) not in obstaculos
    
    def calcular_camino_hasta_punto(dest_x, dest_y):
        # Inicializa el conjunto abierto y el conjunto cerrado
        conjunto_abierto = [(0, x, y)]
        conjunto_cerrado = set()
        
        while conjunto_abierto:
            costo_actual, nodo_x, nodo_y = heapq.heappop(conjunto_abierto)
            
            if (nodo_x, nodo_y) == (dest_x, dest_y):
                return costo_actual
            
            conjunto_cerrado.add((nodo_x, nodo_y))
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    
                    vecino_x, vecino_y = nodo_x + dx, nodo_y + dy
                    if es_valido(vecino_x, vecino_y) and (vecino_x, vecino_y) not in conjunto_cerrado:
                        costo_vecino = costo_actual + 1 + ((dx != 0) and (dy != 0))
                        heapq.heappush(conjunto_abierto, (costo_vecino, vecino_x, vecino_y))
        
        return float('inf')
    
    arriba_izquierda = calcular_camino_hasta_punto(1, 1)
    arriba_derecha = calcular_camino_hasta_punto(ancho_matriz, 1)
    abajo_izquierda = calcular_camino_hasta_punto(1, alto_matriz)
    abajo_derecha = calcular_camino_hasta_punto(ancho_matriz, alto_matriz)
    
    return arriba_izquierda, arriba_derecha, abajo_izquierda, abajo_derecha

# Ejemplo de uso
x = 2
y = 2
ancho_matriz = 5
alto_matriz = 5
obstaculos = [(2, 2), (2, 3), (4, 4)]

resultado = calcular_area_accesible(x, y, ancho_matriz, alto_matriz, obstaculos)
print("Área accesible en cuadrante superior izquierdo:", resultado[0])
print("Área accesible en cuadrante superior derecho:", resultado[1])
print("Área accesible en cuadrante inferior izquierdo:", resultado[2])
print("Área accesible en cuadrante inferior derecho:", resultado[3])
