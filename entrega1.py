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
import math


def planear_rover(rover_inicio=(0, 0), bateria_inicial=20, zonas_sombra=[(0, 1), (0, 2)], muestras_igneas=[(1, 1), (1, 2)], muestras_sedimentarias=[(2, 3)]):
                  
    #           (ubicacion_rover, bateria, taladro, carga, muestras_i, muestras_s)
   
    INICIAL_STATE = (rover_inicio, bateria_inicial, None, (), tuple(muestras_igneas), tuple(muestras_sedimentarias))
    const_sombras = zonas_sombra

    problema = ProblemAres1(INICIAL_STATE, const_sombras)
    resultado = astar(problema)

    if resultado is not None:

        acciones_finales = []
        
        for accion, estado in resultado.path():
            if accion is not None:

                acciones_finales.append(accion)
        
        return acciones_finales  
    else:
        return []


class ProblemAres1(SearchProblem):

    def __init__(self, INICIAL_STATE, const_sombras):
        super().__init__(INICIAL_STATE)
        self.const_sombras = const_sombras

    def cost(self, state, action, state2):
        if action[0] == "moverse":
         minutos = 1
        elif action[0] == "sobremarcha":
         minutos = 1
        elif action[0] == "equipar":
         minutos = 3
        elif action[0] == "recolectar":
         minutos = 2
        elif action[0] == "depositar":
         minutos = 1 * len(state[3])
        elif action[0] == "recargar":
         minutos = 4
        else:
         minutos = 0

        return minutos
    
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


        if bateria > 1:
         for new_row, new_col in simple_moves:                    #antes de agregar la accion de movimiento verificamos que la coordenada no sea negativo   
          available_actions.append(("moverse",(new_row,new_col)))
        

        if bateria > 4 :
         for new_row_s, new_col_s in sobremarchas:                #antes de agregar la accion de sobremarcha verificamos que la coordenada no sea negativo 
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
        

        if (row,col) not in self.const_sombras and bateria < 12:
            available_actions.append(("recargar", None))


        if bateria > 1:
         if len(carga) == 2:                                                       #aca validamos que tengamos ambas muestras en la bodega para depositar
            available_actions.append(("depositar", None))
         elif len(carga) == 1 and not (coordenadas_ignea or coordenadas_sedimentaria):                   #aca verificamos el caso en el que se la ultima muestra para poder depositar solo una
            available_actions.append(("depositar", None))
            

        return available_actions
    
    def result(self, state, action):
        rover_pos = state[0]
        rover_bat = state[1]
        rover_herr = state[2]
        rover_carga = list(state[3])
        coord_igneas = list(state[4])
        coord_sedim = list(state[5])

        if action[0] == "moverse":
            rover_pos = action[1]
            rover_bat -= 1 
        elif action[0] == "sobremarcha":
            rover_pos = action[1]
            rover_bat -= 4
        
        if action[0] == "equipar":
            rover_herr = action[1]
            rover_bat -= 1

        if action[0] == "recolectar":
            rover_bat -= 3
            rover_carga.append(action[1])

            if action[1] == "ignea":
                coord_igneas.remove(rover_pos)
            elif action[1] == "sedimentaria":
                coord_sedim.remove(rover_pos)

        
        if action[0] == "depositar":
            rover_carga = ()
            rover_bat -= 1
        
        if action[0] == "recargar":
            rover_bat += 10
            if rover_bat > 20:
                rover_bat = 20
        
        return (rover_pos,
                rover_bat, 
                rover_herr, 
                tuple(rover_carga), 
                tuple(coord_igneas), 
                tuple(coord_sedim))
    

    def is_goal(self, state):
        return len(state[4]) == 0 and len(state[5]) == 0 and len(state[3]) == 0
    

    def heuristic(self, state):
       pos = state[0]
       coord_faltantes = state[4] + state[5]
       costo_carga = len(state[3])
    
       afirmar_cambio_herramineta = len(state[4]) != 0 and len(state[5]) != 0

       if len(coord_faltantes) == 0 and costo_carga == 0:
          return 0
       
       pos_min = min((abs(pos[0] - f) + abs(pos[1] - c)) / 2 
                     if pos[0] == f or pos[1] == c 
                     else abs(pos[0] - f) + abs(pos[1] - c)
                     for f, c in coord_faltantes) if coord_faltantes else 0

       if afirmar_cambio_herramineta == True:
          return pos_min + (len(coord_faltantes) * 2) + costo_carga + len(coord_faltantes) + 3
       else:
          return pos_min + (len(coord_faltantes) * 2) + costo_carga + len(coord_faltantes) 
          
       
        

if __name__ == "__main__":
    
    acciones = planear_rover(rover_inicio=(0, 0), bateria_inicial=20, zonas_sombra=[], muestras_igneas=[(0, 1), (0, 2)], muestras_sedimentarias=[(1, 1)])
    
   
    print(acciones)



        


        




        

