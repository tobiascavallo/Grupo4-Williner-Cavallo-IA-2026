from simpleai.search.csp import CspProblem, backtrack

def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    rows, cols = camp_size
    craters_set = set(craters)

    all_cells = [(r, c) for r in range(rows) for c in range(cols) if (r, c) not in craters_set]
    border_cells = [cell for cell in all_cells if cell[0] == 0 or cell[0] == rows-1 or cell[1] == 0 or cell[1] == cols-1]
    interior_cells = [cell for cell in all_cells if cell not in border_cells]

    def adj(r, c):
        return [(r+dr, c+dc) for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)] if 0 <= r+dr < rows and 0 <= c+dc < cols]

    variables = []
    domains = {}

    for i in range(habs):
        v = f"hab{i}"
        variables.append(v)
        domains[v] = interior_cells[:]

    for i in range(generators):
        v = f"gen{i}"
        variables.append(v)
        domains[v] = all_cells[:]

    for i in range(labs):
        v = f"lab{i}"
        variables.append(v)
        domains[v] = all_cells[:]

    for i in range(deposits):
        v = f"dep{i}"
        variables.append(v)
        domains[v] = all_cells[:]

    for i in range(airlocks):
        v = f"air{i}"
        variables.append(v)
        domains[v] = border_cells[:]

    constraints = []

    # No overlap: all pairs
    for i in range(len(variables)):
        for j in range(i+1, len(variables)):
            vi, vj = variables[i], variables[j]
            def no_overlap(vars, vals, vi=vi, vj=vj):
                return vals[0] != vals[1]
            constraints.append(((vi, vj), no_overlap))

    # Gen not adjacent to hab
    for i in range(generators):
        for j in range(habs):
            gv = f"gen{i}"
            hv = f"hab{j}"
            def gen_hab(vars, vals):
                gr, gc = vals[0]
                hr, hc = vals[1]
                return (hr, hc) not in [(gr+dr, gc+dc) for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]]
            constraints.append(((gv, hv), gen_hab))

    # Gen not adjacent to gen
    for i in range(generators):
        for j in range(i+1, generators):
            gi, gj = f"gen{i}", f"gen{j}"
            def gen_gen(vars, vals):
                r1, c1 = vals[0]
                r2, c2 = vals[1]
                return (r2, c2) not in [(r1+dr, c1+dc) for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]]
            constraints.append(((gi, gj), gen_gen))

    # Lab adjacent to at least one dep
    dep_vars = [f"dep{i}" for i in range(deposits)]
    for i in range(labs):
        lv = f"lab{i}"
        lab_dep_vars = tuple([lv] + dep_vars)
        def lab_dep(vars, vals):
            lr, lc = vals[0]
            neighbors = set((lr+dr, lc+dc) for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)])
            for dep_pos in vals[1:]:
                if dep_pos in neighbors:
                    return True
            return False
        constraints.append((lab_dep_vars, lab_dep))

    # Hab evacuation route: at least one adjacent free cell (not crater, not occupied by any module)
    for i in range(habs):
        hv = f"hab{i}"
        other_vars = [v for v in variables if v != hv]
        hab_all_vars = tuple([hv] + other_vars)
        def hab_evac(vars, vals):
            hr, hc = vals[0]
            occupied = set(vals[1:])
            neighbors = [(hr+dr, hc+dc) for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]
                         if 0 <= hr+dr < rows and 0 <= hc+dc < cols]
            for nb in neighbors:
                if nb not in craters_set and nb not in occupied:
                    return True
            return False
        constraints.append((hab_all_vars, hab_evac))

    problem = CspProblem(variables, domains, constraints)
    solution = backtrack(problem)

    if solution is None:
        return None

    result = []
    for v, pos in solution.items():
        tipo = ''.join([ch for ch in v if not ch.isdigit()])
        result.append((tipo, pos[0], pos[1]))
    return result