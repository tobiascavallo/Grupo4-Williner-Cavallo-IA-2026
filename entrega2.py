from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
)
def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    variables = ['hab', 'gen', 'lab', 'dep', 'air']

    domains = {
    'hab': [(x, y) for x in range(camp_size) for y in range(camp_size)],    
    'gen': [(x, y) for x in range(camp_size) for y in range(camp_size)],
    'lab': [(x, y) for x in range(camp_size) for y in range(camp_size)],
    'dep': [(x, y) for x in range(camp_size) for y in range(camp_size)],
    'air': [(x, y) for x in range(camp_size) for y in range(camp_size)],
    }

    constraints = []

    def different(variables, values):

        return values[0] != values[1]

    for var1, var2 in combinations(variables, 2):
        constraints.append(
            ((var1, var2), different)
        )


    def no_crater(variables, values):
        for n in values
           if n in craters return False

        return True

    constraints.append((tuple(variables), no_crater))

    def esclusas(variables, values):
        xesc, yesc = values[0]
        abajo, derecha = camp_size

        return xesc == 0 or yesc == 0 or xesc == abajo or yesc == derecha
        
    constraints.append(('air'),esclusas)


    def evacuacion(variables, values):
        xhab, yhab = values[0] 
        otras_posiciones = []
        for n in range(1, len(variables)):
            otras_posiciones.append(values[n])
        contador = 0
        
        vecinos = [
            (xhab - 1, yhab),
            (xhab + 1, yhab),
            (xhab, yhab - 1),
            (xhab, yhab + 1)
        ]

        for vx, vy in vecinos:
            no_es_crater = (vx, vy) not in craters
            no_hay_otro_modulo = (vx, vy) not in otras_posiciones
            
            if no_es_crater and no_hay_otro_modulo:
                contador += 1

        return contador >= 1