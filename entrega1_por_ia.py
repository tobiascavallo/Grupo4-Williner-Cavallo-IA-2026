import math
from simpleai.search import SearchProblem, astar

class AresRoverProblem(SearchProblem):
    def _init_(self, rover_inicio, bateria_inicial, zonas_sombra, muestras_igneas, muestras_sedimentarias):
        self.zonas_sombra = set(zonas_sombra)
        
        # El estado será una tupla inmutable para que SimpleAI pueda usarlo en sets/diccionarios internamente.
        # Estructura del estado: 
        # (posicion, bateria, taladro_equipado, cantidad_carga, muestras_igneas_pendientes, muestras_sedimentarias_pendientes)
        estado_inicial = (
            rover_inicio,
            bateria_inicial,
            None, # Sin taladro equipado inicialmente
            0,    # Carga vacía (0 muestras)
            frozenset(muestras_igneas),
            frozenset(muestras_sedimentarias)
        )
        super()._init_(initial_state=estado_inicial)

    def actions(self, state):
        pos, bateria, taladro, carga, igneas, sedimentarias = state
        r, c = pos
        acciones_disponibles = []

        # 1. Moverse: Consume 1 batería (batería debe ser > 1 para que no llegue a 0)
        if bateria > 1:
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                acciones_disponibles.append(("moverse", (r + dr, c + dc)))

        # 2. Sobremarcha: Consume 4 batería (batería debe ser > 4)
        if bateria > 4:
            for dr, dc in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                acciones_disponibles.append(("sobremarcha", (r + dr, c + dc)))

        # 3. Equipar taladro: Consume 1 batería
        if bateria > 1:
            # Solo consideramos equiparlo si nos sirve para algo que falta recolectar y si no lo tenemos puesto
            if taladro != "termico" and igneas:
                acciones_disponibles.append(("equipar", "termico"))
            if taladro != "percusion" and sedimentarias:
                acciones_disponibles.append(("equipar", "percusion"))

        # 4. Perforar y recolectar: Consume 3 batería (batería debe ser > 3)
        if bateria > 3 and carga < 2:
            if pos in igneas and taladro == "termico":
                acciones_disponibles.append(("recolectar", "ignea"))
            if pos in sedimentarias and taladro == "percusion":
                acciones_disponibles.append(("recolectar", "sedimentaria"))

        # 5. Depositar cápsula: Consume 1 batería
        if bateria > 1 and carga > 0:
            # Condición: necesita 2 muestras, A MENOS que sea la última (es decir, que ya no queden en el mapa)
            if carga == 2 or (len(igneas) + len(sedimentarias) == 0):
                acciones_disponibles.append(("depositar", None))

        # 6. Desplegar paneles solares: Restaura 10 batería
        if pos not in self.zonas_sombra and bateria < 20:
            acciones_disponibles.append(("recargar", None))

        return acciones_disponibles

    def result(self, state, action):
        pos, bateria, taladro, carga, igneas, sedimentarias = state
        tipo_accion, param = action

        new_pos = pos
        new_bateria = bateria
        new_taladro = taladro
        new_carga = carga
        new_igneas = set(igneas)
        new_sedimentarias = set(sedimentarias)

        if tipo_accion == "moverse":
            new_pos = param
            new_bateria -= 1
        elif tipo_accion == "sobremarcha":
            new_pos = param
            new_bateria -= 4
        elif tipo_accion == "equipar":
            new_taladro = param
            new_bateria -= 1
        elif tipo_accion == "recolectar":
            if param == "ignea":
                new_igneas.remove(pos)
            else:
                new_sedimentarias.remove(pos)
            new_carga += 1
            new_bateria -= 3
        elif tipo_accion == "depositar":
            new_carga = 0
            new_bateria -= 1
        elif tipo_accion == "recargar":
            new_bateria = min(20, new_bateria + 10)

        return (new_pos, new_bateria, new_taladro, new_carga, frozenset(new_igneas), frozenset(new_sedimentarias))

    def cost(self, state, action, state2):
        tipo_accion, _ = action
        if tipo_accion == "moverse": 
            return 1
        if tipo_accion == "sobremarcha": 
            return 1
        if tipo_accion == "equipar": 
            return 3
        if tipo_accion == "recolectar": 
            return 2
        if tipo_accion == "depositar": 
            return state[3]  # Toma 1 minuto por muestra entregada (carga del estado anterior)
        if tipo_accion == "recargar": 
            return 4
        return 0

    def is_goal(self, state):
        _, _, _, carga, igneas, sedimentarias = state
        # El objetivo es que no queden muestras en el mapa ni en la bahía de carga del rover
        return len(igneas) == 0 and len(sedimentarias) == 0 and carga == 0

    def heuristic(self, state):
        pos, _, _, carga, igneas, sedimentarias = state
        pendientes = list(igneas) + list(sedimentarias)
        h = 0
        
        if pendientes:
            # 1. Tiempo mínimo para recolectar y depositar todo lo pendiente (2 mins recolección + 1 min depósito x muestra)
            h += 3 * len(pendientes)
            
            # 2. Distancia Manhattan a la muestra más cercana
            # Dividido por 2 porque 'sobremarcha' permite avanzar 2 celdas en 1 minuto (admisible)
            min_dist = min(abs(pos[0] - s[0]) + abs(pos[1] - s[1]) for s in pendientes)
            h += math.ceil(min_dist / 2)
            
        # 3. Tiempo ineludible para depositar la carga que ya tenemos encima
        if carga > 0:
            h += carga
            
        return h


def planear_rover(rover_inicio=(0, 0), bateria_inicial=20, zonas_sombra=None, muestras_igneas=None, muestras_sedimentarias=None):
    # Por seguridad con mutables en Python, iniciamos las listas vacías si no se proveen
    if zonas_sombra is None: zonas_sombra = []
    if muestras_igneas is None: muestras_igneas = []
    if muestras_sedimentarias is None: muestras_sedimentarias = []

    problema = AresRoverProblem(
        rover_inicio=rover_inicio,
        bateria_inicial=bateria_inicial,
        zonas_sombra=zonas_sombra,
        muestras_igneas=muestras_igneas,
        muestras_sedimentarias=muestras_sedimentarias
    )

    # astar con graph_search=True es mandatorio para evitar loops infinitos (como recargar-moverse constantemente)
    resultado = astar(problema, graph_search=True)
    
    if resultado is None:
        return [] # No se encontró solución

    # resultado.path() devuelve una lista de tuplas (acción, estado).
    # Descartamos el primer elemento (None, estado_inicial) y extraemos sólo la acción.
    acciones = [accion for accion, estado in resultado.path() if accion is not None]
    
    return acciones

# ==== Ejemplo de uso ====
if _name_ == '_main_':
    acciones = planear_rover(
        rover_inicio=(0, 0),
        bateria_inicial=20,
        zonas_sombra=[(0, 1), (0, 2)],
        muestras_igneas=[(1, 1), (1, 2)],
        muestras_sedimentarias=[(2, 3)],
    )
    
    print("Secuencia óptima de acciones:")
    for a in acciones:
        print(f"  {a}")