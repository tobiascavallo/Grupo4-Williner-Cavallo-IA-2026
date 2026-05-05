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
   
    inital_state = (("r",(rover_inicio)), ("b",(bateria_inicial)), ("m_i",(muestras_igneas)), ("m_s",(muestras_sedimentarias)),("t",(None)),("a",0))#DUDA: el tipo de taladro con el que comienza a trabajar llega por parametro, no seteamos ninguno o cualquiera
    const_sombras = zonas_sombra


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
        

