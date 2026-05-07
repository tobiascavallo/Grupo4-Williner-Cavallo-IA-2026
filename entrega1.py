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


def Planear_rover(rover_inicio=(0, 0), bateria_inicial=20, zonas_sombra=[(0, 1), (0, 2)], muestras_igneas=[(1, 1), (1, 2)], muestras_sedimentarias=[(2, 3)]):
                  
    #           (ubicacion_rover, bateria, taladro, carga, muestras_i, muestras_s)
   
    INICIAL_STATE = (rover_inicio, bateria_inicial, None, (), muestras_igneas, muestras_sedimentarias)
    const_sombras = zonas_sombra

    problema = ProblemAres1(INICIAL_STATE, const_sombras)
    resultado = astar(problema)


class ProblemAres1(SearchProblem):

    def __init__(self, INICIAL_STATE, const_sombras):
        super().__init__(INICIAL_STATE)
        self.const_sombras = const_sombras

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
        herramienta = state[2]
        coordenadas_ignea = state[4]
        coordenadas_sedimentaria = state[5]
        carga = state[3]
        bateria = state[1]

        available_actions = []

        simple_moves = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]
#los separe porque no cuestan lo mismo
        sobremarchas = [
            (row - 2, col),
            (row + 2, col),
            (row, col - 2),
            (row, col + 2),
        ]


        for new_row, new_col in simple_moves and bateria > 1:                    #antes de agregar la accion de movimiento verificamos que la coordenada no sea negativo 
            if new_row >= 0 and new_col >= 0:
                available_actions.append(("moverse",(new_row,new_col)))
        

        for new_row_s, new_col_s in sobremarchas and bateria > 4:                #antes de agregar la accion de sobremarcha verificamos que la coordenada no sea negativo 
            if new_row_s >= 0 and new_col_s >= 0:
                available_actions.append(("sobremarcha",(new_row_s,new_col_s)))
        

        if (row,col) in coordenadas_ignea:                                       #primero verificamos que el rover este parado sobre una roca ignea
            if herramienta != "termico":    
                if bateria > 1:                                     #verificamos si tiene el taladro adecuado
                 available_actions.append(("equipar","termico"))                  #si no lo tiene lo equipamos
            elif bateria > 3 and len(carga) < 2:
                available_actions.append(("recolectar","ignea"))                  #si ya lo tenia equipado comenzamos la recoleccion


        if (row,col) in coordenadas_sedimentaria:                                 # este if es el mismo que el de arriba pero para muestras sedimentarias
            if herramienta != "percusion":
                if bateria > 1:
                 available_actions.append(("equipar","percusion"))
            elif bateria > 3 and len(carga) < 2:
                available_actions.append(("recolectar","sedimentaria"))
        

        if (row,col) not in self.const_sombras and bateria < 20:
            available_actions.append(("recargar", None))


        if len(carga) == 2 and bateria > 1:                                                       #aca validamos que tengamos ambas muestras en la bodega para depositar
            available_actions.append(("despositar", None))
        elif len(carga) == 1 and not (coordenadas_ignea or coordenadas_sedimentaria):                   #aca verificamos el caso en el que se la ultima muestra para poder depositar solo una
            available_actions.append(("depositar", None))
            

        return available_actions
    
    def result(self, state, action):
        rover_pos = list(state[0])
        rover_bat = list(state[1])
        rover_herr = list(state[2])
        rover_carga = list(state[3])
        coord_igneas = list(state[4])
        coord_sedim= list(state[5])

        if action == "moverse":
            rover_pos = action[1]
            rover_bat -= 1 
        elif action == "sobremarcha":
            rover_pos = action[1]
            rover_bat -= 4
        
        if action == "equipar":
            rover_herr = action[1]
            rover_bat -= 1

        if action == "recolectar":
            rover_carga = action[1]
            rover_bat -= 3
            if action[1] == "ignea": #terminar esto, estaba haciendo lo de eliminar la muestra q se recolecto del mapa

        
        if action == "depositar":
            rover_carga = ()
            rover_bat -= 1
        
        if action == "recargar":
            rover_bat += 10
        
        return (tuple(rover_pos,rover_bat,rover_herr,rover_carga,coord_igneas,coord_sedim))



        


        




        

