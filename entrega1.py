from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    limited_depth_first,
    uniform_cost,
    iterative_limited_depth_first,
    greedy,
    astar,
)
from simpleai.search.viewers import BaseViewer, WebViewer

TALADROS_POR_ROCA = {
    "ignea": "termico",
    "sedimentaria": "percusión"
}

def Planear_rover(rover_inicio=(0, 0), bateria_inicial=20, zonas_sombra=[(0, 1), (0, 2)], muestras_igneas=[(1, 1), (1, 2)], muestras_sedimentarias=[(2, 3)]):
                  
    #           (ubicacion_rover, bateria, taladro, carga, muestras_i, muestras_s)
   
    INICIAL_STATE = (rover_inicio, bateria_inicial, None, (), muestras_igneas, muestras_sedimentarias)
    const_sombras = zonas_sombra

    problema = ProblemAres1(INICIAL_STATE, const_sombras)
    resultado = astar(problema)


class ProblemAres1(SearchProblem):
    def cost(self, state, action, state2):
        if action == "moverse":
            minutos = 1
            UC = 1
            
        if action == "sobremarcha":
            minutos = 1
            UC = 4
        
        if action == "equipar":
            minutos = 3
            UC = 1

        if action == "recolectar":
            minutos = 2
            UC = 3
        
        if action == "depositar":
            minutos = 1
            UC = 1
        
        if action == "recargar":
            minutos = 4

        return minutos, UC 
    
    def actions(self, state):
        row, col = state[0]
        available_actions = []

        moves = [
            (row - 1, col),
            (row + 1, col),
            (row - 2, col),
            (row + 2, col),
            (row, col - 1),
            (row, col + 1),
            (row, col - 2),
            (row, col + 2)# QUEDE ACA DONDE ESTOY VIENDO COMO LIMITAR LOS MOVIMIENTO DENTRO DE LA GRILLA
        ]

        for new_row, new_col in moves:
            if 0 < new_row < len()

        

