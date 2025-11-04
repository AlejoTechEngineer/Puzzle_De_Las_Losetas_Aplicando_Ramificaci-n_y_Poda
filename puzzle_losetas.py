import heapq
from typing import List, Tuple, Optional
import copy

class Estado:
    """Representa un estado del puzzle"""
    def __init__(self, tablero: List[List[int]], movimientos: int = 0, padre=None):
        self.tablero = tablero
        self.movimientos = movimientos
        self.padre = padre
        self.pos_vacia = self.encontrar_vacia()
        self.heuristica = self.calcular_heuristica()
        self.costo_total = self.movimientos + self.heuristica
    
    def encontrar_vacia(self) -> Tuple[int, int]:
        """Encuentra la posición del espacio vacío (16)"""
        for i in range(4):
            for j in range(4):
                if self.tablero[i][j] == 16:
                    return (i, j)
        return (0, 0)
    
    def calcular_heuristica(self) -> int:
        """Calcula la distancia Manhattan (heurística)"""
        distancia = 0
        for i in range(4):
            for j in range(4):
                valor = self.tablero[i][j]
                if valor != 16:  # No contar el espacio vacío
                    fila_objetivo = (valor - 1) // 4
                    col_objetivo = (valor - 1) % 4
                    distancia += abs(i - fila_objetivo) + abs(j - col_objetivo)
        return distancia
    
    def es_objetivo(self) -> bool:
        """Verifica si es el estado objetivo (configuración natural)"""
        objetivo = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        return self.tablero == objetivo
    
    def obtener_vecinos(self) -> List['Estado']:
        """Genera todos los estados alcanzables con un movimiento válido"""
        vecinos = []
        i, j = self.pos_vacia
        
        # Movimientos posibles: arriba, abajo, izquierda, derecha
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for di, dj in movimientos:
            ni, nj = i + di, j + dj
            
            # Verificar si el movimiento es válido
            if 0 <= ni < 4 and 0 <= nj < 4:
                nuevo_tablero = copy.deepcopy(self.tablero)
                # Intercambiar la pieza con el espacio vacío
                nuevo_tablero[i][j], nuevo_tablero[ni][nj] = nuevo_tablero[ni][nj], nuevo_tablero[i][j]
                vecinos.append(Estado(nuevo_tablero, self.movimientos + 1, self))
        
        return vecinos
    
    def __lt__(self, otro):
        """Comparador para la cola de prioridad"""
        return self.costo_total < otro.costo_total
    
    def __eq__(self, otro):
        return self.tablero == otro.tablero
    
    def __hash__(self):
        return hash(str(self.tablero))


def contar_inversiones(tablero: List[List[int]]) -> int:
    """Cuenta las inversiones en el tablero"""
    lista = []
    for fila in tablero:
        for num in fila:
            if num != 16:  # Excluir el espacio vacío
                lista.append(num)
    
    inversiones = 0
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] > lista[j]:
                inversiones += 1
    
    return inversiones


def es_solucionable(tablero: List[List[int]]) -> bool:
    """
    Verifica si el puzzle es solucionable
    Un puzzle de 4x4 es solucionable si:
    - Si la fila del espacio vacío (contando desde abajo) es impar, 
      el número de inversiones debe ser par
    - Si la fila del espacio vacío es par, 
      el número de inversiones debe ser impar
    """
    inversiones = contar_inversiones(tablero)
    
    # Encontrar la fila del espacio vacío (contando desde abajo)
    fila_vacia = 0
    for i in range(4):
        for j in range(4):
            if tablero[i][j] == 16:
                fila_vacia = 4 - i  # Contar desde abajo
                break
    
    # Verificar condición de solubilidad
    if fila_vacia % 2 == 0:  # Fila par desde abajo
        return inversiones % 2 == 1
    else:  # Fila impar desde abajo
        return inversiones % 2 == 0


def imprimir_tablero(tablero: List[List[int]]):
    """Imprime el tablero de forma visual"""
    print("┌────┬────┬────┬────┐")
    for i, fila in enumerate(tablero):
        print("│", end="")
        for num in fila:
            if num == 16:
                print("    │", end="")
            else:
                print(f" {num:2} │", end="")
        print()
        if i < 3:
            print("├────┼────┼────┼────┤")
    print("└────┴────┴────┴────┘")


def resolver_puzzle(tablero_inicial: List[List[int]]) -> Optional[List[Estado]]:
    """
    Resuelve el puzzle usando Ramificación y Poda (Branch and Bound con A*)
    """
    # Verificar si es solucionable
    if not es_solucionable(tablero_inicial):
        return None
    
    estado_inicial = Estado(tablero_inicial)
    
    # Si ya está resuelto
    if estado_inicial.es_objetivo():
        return [estado_inicial]
    
    # Cola de prioridad para Branch and Bound
    frontera = []
    heapq.heappush(frontera, estado_inicial)
    
    # Conjunto de estados visitados (PODA)
    visitados = set()
    visitados.add(hash(estado_inicial))
    
    nodos_explorados = 0
    
    while frontera:
        estado_actual = heapq.heappop(frontera)
        nodos_explorados += 1
        
        # Verificar si llegamos al objetivo
        if estado_actual.es_objetivo():
            # Reconstruir el camino
            camino = []
            temp = estado_actual
            while temp:
                camino.append(temp)
                temp = temp.padre
            camino.reverse()
            
            print(f"\n✓ Solución encontrada en {estado_actual.movimientos} movimientos")
            print(f"  Nodos explorados: {nodos_explorados}")
            return camino
        
        # Generar vecinos (ramificación)
        for vecino in estado_actual.obtener_vecinos():
            hash_vecino = hash(vecino)
            if hash_vecino not in visitados:
                visitados.add(hash_vecino)
                heapq.heappush(frontera, vecino)
    
    return None


def main():
    print("="*50)
    print("  PUZZLE DE LAS 15 LOSETAS")
    print("  Ramificación y Poda (Branch and Bound)")
    print("="*50)
    
    # Ejemplo 1: Configuración de la imagen (última presentación)
    print("\n📋 EJEMPLO 1: Configuración de la presentación")
    tablero1 = [
        [1, 2, 3, 4],
        [8, 14, 16, 12],
        [10, 11, 5, 13],
        [9, 6, 7, 15]
    ]
    
    print("\n🔹 Configuración inicial:")
    imprimir_tablero(tablero1)
    
    print("\n⏳ Verificando solubilidad...")
    inversiones = contar_inversiones(tablero1)
    print(f"   Inversiones: {inversiones}")
    
    if not es_solucionable(tablero1):
        print("\n❌ Esta configuración NO tiene solución")
        print("   El puzzle es IMPOSIBLE de resolver desde esta configuración.")
    else:
        print("\n✓ Esta configuración SÍ tiene solución")
        print("\n⏳ Buscando solución óptima...")
        
        solucion = resolver_puzzle(tablero1)
        
        if solucion:
            print(f"\n🎯 SOLUCIÓN ENCONTRADA ({len(solucion)-1} movimientos):\n")
            for i, estado in enumerate(solucion):
                print(f"Paso {i}:")
                imprimir_tablero(estado.tablero)
                print()
    
    # Ejemplo 2: Configuración sencilla
    print("\n" + "="*50)
    print("\n📋 EJEMPLO 2: Configuración sencilla (2 movimientos)")
    tablero2 = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 16, 15]
    ]
    
    print("\n🔹 Configuración inicial:")
    imprimir_tablero(tablero2)
    
    solucion2 = resolver_puzzle(tablero2)
    
    if solucion2:
        print(f"\n🎯 SOLUCIÓN ENCONTRADA ({len(solucion2)-1} movimientos):\n")
        for i, estado in enumerate(solucion2):
            print(f"Paso {i}:")
            imprimir_tablero(estado.tablero)
            print()
            
    # Ejemplo 3: Configuración IMPOSIBLE
    print("\n" + "="*50)
    print("\n📋 EJEMPLO 3: Configuración IMPOSIBLE")
    tablero3 = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 15, 14, 16]  # 14 y 15 intercambiados - configuración imposible
    ]

    print("\n🔹 Configuración inicial:")
    imprimir_tablero(tablero3)

    print("\n⏳ Verificando solubilidad...")
    inversiones3 = contar_inversiones(tablero3)
    print(f"   Inversiones: {inversiones3}")

    if not es_solucionable(tablero3):
        print("\n❌ Esta configuración NO tiene solución")
        print("   El puzzle es IMPOSIBLE de resolver desde esta configuración.")
        print("   Razón: Las inversiones y la posición del espacio vacío no cumplen")
        print("   con las condiciones matemáticas de solubilidad.")
    else:
        print("\n✓ Esta configuración SÍ tiene solución")
        solucion3 = resolver_puzzle(tablero3)
        if solucion3:
            print(f"\n🎯 SOLUCIÓN: {len(solucion3)-1} movimientos")

if __name__ == "__main__":
    main()