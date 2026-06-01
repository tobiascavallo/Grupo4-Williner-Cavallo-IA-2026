from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
)
def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):

    variables = []
    variables += [f"hab_{i}" for i in range(habs)]
    variables += [f"gen_{i}" for i in range(generators)]
    variables += [f"lab_{i}" for i in range(labs)]
    variables += [f"dep_{i}" for i in range(deposits)]
    variables += [f"air_{i}" for i in range(airlocks)]
    
    domains = {}
    rows, cols = camp_size
    craters_set = set(craters)

    camp = [(x, y) for x in range(camp_size[0]) for y in range(camp_size[1])]
    
    for var in variables:
        domains[var] = camp
    
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
    
    air_vars = [v for v in variables if v.startswith('air')]
    for air in air_vars:
        constraints.append(((air,), esclusas_in_border))


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
    
    hab_vars = [v for v in variables if v.startswith('hab')]
    for hab in hab_vars:
        vars_involucradas = [hab] + [v for v in variables if v != hab]
        constraints.append((tuple(vars_involucradas), evacuacion))

    def hab_al_interior(variables, values):
        xesc, yesc = values[0]

        if xesc == 0 or yesc == 0 or xesc == camp_size[0] - 1 or yesc == camp_size[1] - 1:
            return False
        return True
        
    
    for hab in hab_vars:
        constraints.append(((hab,), hab_al_interior))

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
    
    gen_vars = [v for v in variables if v.startswith('gen')]
    
    for h in hab_vars:
        for g in gen_vars:
            constraints.append(((h, g), adyacencia_generador))
            
    for g1, g2 in combinations(gen_vars, 2):
        constraints.append(((g1, g2), adyacencia_generador))

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
   
    lab_vars = [v for v in variables if v.startswith('lab')]
    dep_vars = [v for v in variables if v.startswith('dep')]
    
    for lab in lab_vars:
        vars_involucradas = [lab] + dep_vars
        constraints.append((tuple(vars_involucradas), cadena_suministro))


    problem = CspProblem(variables, domains, constraints)
    resultado = backtrack(problem)
    
    if resultado is not None:
        resultado_final = []
        for nombre, coord in resultado.items():
            tipo = nombre.split('_')[0] 
            fila, columna = coord
            resultado_final.append((tipo, fila, columna))
        return resultado_final
        
    return None
        