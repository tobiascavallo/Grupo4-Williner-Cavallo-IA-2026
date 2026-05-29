from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
)
def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    variables = ['hab', 'gen', 'lab', 'dep', 'air']

    domains = {
    'hab': [(x, y) for x in range(camp_size[0]) for y in range(camp_size[1])],    
    'gen': [(x, y) for x in range(camp_size[0]) for y in range(camp_size[1])],
    'lab': [(x, y) for x in range(camp_size[0]) for y in range(camp_size[1])],
    'dep': [(x, y) for x in range(camp_size[0]) for y in range(camp_size[1])],
    'air': [(x, y) for x in range(camp_size[0]) for y in range(camp_size[1])],
    }

    constraints = []

    def different(variables, values):

        return values[0] != values[1]

    for var1, var2 in combinations(variables, 2):
        constraints.append(
            ((var1, var2), different)
        )


    def no_crater(variables, values):

        return values[0] not in craters 
    
    for var in variables:
        constraints.append(((var,), no_crater))


    def esclusas_in_border(variables, values):
        xesc, yesc = values[0]
        abajo, derecha = camp_size

        return xesc == 0 or yesc == 0 or xesc == abajo-1 or yesc == derecha-1
    
    constraints.append((('air',),esclusas_in_border))


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
    constraints.append((('hab',), evacuacion))

    def hab_al_interior(variables, values):
        xesc, yesc = values[0]

        if xesc == 0 or yesc == 0 or xesc == camp_size[0] or yesc == camp_size[1] :
            return False
        return True
    constraints.append((('hab',), hab_al_interior))

    def adyacencia_generador(variables, values):
        xhab,yhab = values[0]
        gen = values[1]

        vecinos = [
            (xhab - 1, yhab),
            (xhab + 1, yhab),
            (xhab, yhab - 1),
            (xhab, yhab + 1)
        ]
        return gen not in vecinos
    
    for var1, var2 in combinations(variables, 2):
        if ('hab' in var1 and 'gen' in var2) or ('gen' in var1 and 'hab' in var2):
            constraints.append(((var1,var2), adyacencia_generador))

    def cadena_suministro(variable, values) :
        xlab, ylab = values[0]
        dep = values[1]

        vecinos = [
            (xlab - 1, ylab),
            (xlab + 1, ylab),
            (xlab, ylab - 1),
            (xlab, ylab + 1)
        ]

        return dep in vecinos
    for var1, var2 in combinations(variables, 2):
        if ( 'lab' in var1 and 'dep' in var2) or ('dep' in var1 and 'lab' in var2):
            constraints.append(((var1,var2), cadena_suministro))




        