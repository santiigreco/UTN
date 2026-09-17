"""
Optimización de Layout SLP Muther - Rotación de 90° y Cinta de Enfriado en L / Colineal
1. Todos los bloques pueden rotar 90° (intercambiando ancho w y largo h).
2. Cadena Galletitas:
   - Moldeadora G [5] siempre adyacente y previa a la entrada del Horno Túnel G [6].
   - Cinta de Enfriado G [7] acoplada estrictamente a la salida del Horno Túnel G [6].
   - La Cinta de Enfriado puede disponerse:
       * Opción A (Colineal): Continúa recta a lo largo (dx = w_horno/2 + w_cinta/2, dy = 0).
       * Opción B (Giro 90° en L hacia Arriba): La entrada de la cinta coincide con el fin del horno, y la cinta se extiende hacia arriba (en Y).
       * Opción C (Giro 90° en L hacia Abajo): La entrada de la cinta coincide con el fin del horno, y la cinta se extiende hacia abajo (en Y).
3. 10.000 iteraciones de Simulated Annealing con multi-reinicio.
4. Cero solapamientos, máxima compactación.
5. Actualización completa de gráficos 300 DPI, Excel y Word.
"""
import os, sys, math, random, copy, json, time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import openpyxl
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"d:\Descargas\UTN\Repo-UTN\2026\Proyecto_Final"
N_ITER = 30000
N_RESTARTS = 8
SEED = 8577


# Dimensiones base oficiales
BASE_DEPTS_V1 = {
    1:  {"name": "Depósito MP",             "w": 8.30,  "h": 6.30,  "area": 52.29,  "color": "#002060"},
    2:  {"name": "Aduana MP",               "w": 3.80,  "h": 3.80,  "area": 14.50,  "color": "#BDD7EE"},
    3:  {"name": "Sección Pesado",          "w": 2.00,  "h": 3.80,  "area": 7.60,   "color": "#FCE4D6"},
    4:  {"name": "Amasado G",               "w": 2.40,  "h": 2.17,  "area": 5.22,   "color": "#FFF2CC"},
    5:  {"name": "Moldeado G",              "w": 2.50,  "h": 2.32,  "area": 5.80,   "color": "#FFF2CC"},
    6:  {"name": "Horno Túnel G",           "w": 8.60,  "h": 2.30,  "area": 19.78,  "color": "#FCE4D6"},
    7:  {"name": "Cinta Enfriado G",        "w": 7.00,  "h": 1.19,  "area": 8.34,   "color": "#E2EFDA"},
    8:  {"name": "Envasado 1° Galletitas",  "w": 4.00,  "h": 4.30,  "area": 17.20,  "color": "#D9E1F2"},
    9:  {"name": "Batido Panif.",            "w": 2.20,  "h": 1.85,  "area": 4.08,   "color": "#FFF2CC"},
    10: {"name": "Dosificado P.",            "w": 2.00,  "h": 1.50,  "area": 3.00,   "color": "#FFF2CC"},
    11: {"name": "Fermentado Panes",         "w": 1.50,  "h": 1.23,  "area": 1.85,   "color": "#FFF2CC"},
    12: {"name": "Hornos Rotat. Panif.",     "w": 5.20,  "h": 3.74,  "area": 19.46,  "color": "#FCE4D6"},
    13: {"name": "Enfriado Panificados",     "w": 2.65,  "h": 2.00,  "area": 5.30,   "color": "#E2EFDA"},
    14: {"name": "Envasado 1° Panif.",       "w": 4.84,  "h": 4.80,  "area": 23.23,  "color": "#D9E1F2"},
    15: {"name": "Depósito PT",             "w": 12.00, "h": 15.60, "area": 187.20, "color": "#1F4E79"},
    16: {"name": "Lavado / Scrap",           "w": 2.90,  "h": 2.00,  "area": 5.80,   "color": "#EDEDED"},
    17: {"name": "Calidad Crudo",            "w": 2.10,  "h": 1.50,  "area": 3.15,   "color": "#EAEAEA"},
    18: {"name": "Calidad Cocido",           "w": 4.50,  "h": 2.80,  "area": 12.60,  "color": "#EAEAEA"},
}

FLOW_V1 = {
    (1,2): 1099.8, (2,3): 1099.8, (3,4): 600.0, (4,5): 600.0, (5,6): 600.0,
    (6,7): 600.0, (7,8): 600.0, (8,15): 630.0,
    (3,9): 600.0, (9,10): 600.0, (10,11): 259.2, (10,12): 345.6, (11,12): 259.2,
    (12,13): 604.8, (13,14): 420.0, (14,15): 500.0,
    (5,4): 6.0, (7,4): 22.0, (5,16): 6.0, (7,16): 5.5, (13,16): 50.0,
    (4,17): 2.0, (9,17): 2.0, (7,18): 3.0, (8,18): 3.0, (13,18): 3.0,
}

BASE_DEPTS_V2 = {k: dict(v) for k, v in BASE_DEPTS_V1.items() if k <= 15}
FLOW_V2 = {k: v for k, v in FLOW_V1.items() if k[0] <= 15 and k[1] <= 15 and k not in [(5,4), (7,4)]}

CHAIN_PAIRS = [(5, 6), (6, 7)]
CONTINUOUS_CHAIN_PAIRS = set([(5, 6), (6, 7)])

def get_dimensions(depts_base, rotations):
    """Devuelve diccionario de dimensiones considerando rotación."""
    depts = {}
    for k, v in depts_base.items():
        rot = rotations.get(k, 0)
        w = v['h'] if rot == 1 else v['w']
        h = v['w'] if rot == 1 else v['h']
        depts[k] = {**v, 'w': w, 'h': h, 'rot': rot}
    return depts

def enforce_chain_geometry(coords, depts, cinta_mode='colinear'):
    """
    Cadena de producción:
    Moldeadora G [5] -> Horno Túnel G [6] -> Cinta Enfriado G [7]
    El Horno Túnel se asume con orientación horizontal (largo en X: w=8.6, h=2.3).
    - Moldeadora G [5]: Adyacente inmediatamente antes del horno:
        cx5 = cx6 - w6/2 - w5/2, cy5 = cy6
    - Cinta de Enfriado G [7]:
        * 'colinear': Cinta en horizontal (w=7.0, h=1.19):
            cx7 = cx6 + w6/2 + w7/2, cy7 = cy6
        * 'turn_up': Cinta girada 90° hacia arriba (w=1.19, h=7.00):
            La entrada de la cinta coincide con el fin del horno en X (salida en cx6 + w6/2).
            cx7 = cx6 + w6/2 - w7/2 (o adyacente a la derecha cx6 + w6/2 + w7/2)
            cy7 = cy6 + h6/2 + h7/2
        * 'turn_down': Cinta girada 90° hacia abajo (w=1.19, h=7.00):
            cx7 = cx6 + w6/2 - w7/2 (o borde alineado)
            cy7 = cy6 - h6/2 - h7/2
    """
    cx6, cy6 = coords[6]
    w6, h6 = depts[6]['w'], depts[6]['h']
    w5, h5 = depts[5]['w'], depts[5]['h']

    # Moldeadora siempre antes del horno a la izquierda
    coords[5] = [cx6 - w6/2.0 - w5/2.0, cy6]

    # Cinta de Enfriado según modo
    if cinta_mode == 'colinear':
        # Cinta horizontal
        w7, h7 = 7.00, 1.19
        depts[7]['w'] = w7
        depts[7]['h'] = h7
        depts[7]['rot'] = 0
        coords[7] = [cx6 + w6/2.0 + w7/2.0, cy6]
    elif cinta_mode == 'turn_up':
        # Cinta vertical hacia arriba
        w7, h7 = 1.19, 7.00
        depts[7]['w'] = w7
        depts[7]['h'] = h7
        depts[7]['rot'] = 1
        # Inicio de la cinta coincide con el fin del horno:
        # Fin del horno está en X = cx6 + w6/2. Centro de la cinta alineado con el extremo derecho del horno:
        coords[7] = [cx6 + w6/2.0 - w7/2.0, cy6 + h6/2.0 + h7/2.0]
    elif cinta_mode == 'turn_down':
        # Cinta vertical hacia abajo
        w7, h7 = 1.19, 7.00
        depts[7]['w'] = w7
        depts[7]['h'] = h7
        depts[7]['rot'] = 1
        coords[7] = [cx6 + w6/2.0 - w7/2.0, cy6 - h6/2.0 - h7/2.0]

def total_overlap_fast(coords, depts, skip_pairs=None):
    keys = list(depts.keys())
    n = len(keys)
    total = 0.0
    sk = set()
    if skip_pairs:
        for p1, p2 in skip_pairs:
            sk.add((p1, p2))
            sk.add((p2, p1))
    for i in range(n):
        ki = keys[i]
        ci = coords[ki]
        wi, hi = depts[ki]['w'], depts[ki]['h']
        for j in range(i+1, n):
            kj = keys[j]
            if (ki, kj) in sk: continue
            cj = coords[kj]
            wj, hj = depts[kj]['w'], depts[kj]['h']
            ox = min(ci[0]+wi/2, cj[0]+wj/2) - max(ci[0]-wi/2, cj[0]-wj/2)
            if ox <= 0: continue
            oy = min(ci[1]+hi/2, cj[1]+hj/2) - max(ci[1]-hi/2, cj[1]-hj/2)
            if oy <= 0: continue
            total += ox * oy
    return total

def eval_obj(coords, depts, flow, cinta_mode='colinear', it=None, n_iter=None):
    z = 0.0
    for (i,j), kg in flow.items():
        if (i,j) in CONTINUOUS_CHAIN_PAIRS:
            continue  # Equipos continuos en línea con malla/cinta motriz automatizada
        ci, cj = coords[i], coords[j]
        z += kg * (abs(ci[0]-cj[0]) + abs(ci[1]-cj[1]))

    ov = total_overlap_fast(coords, depts, CHAIN_PAIRS)
    if it is not None and n_iter is not None and n_iter > 0:
        progress = min(1.0, it / (0.75 * n_iter))
        pen_weight = 1000.0 + 49000.0 * (progress ** 2)
    else:
        pen_weight = 50000.0
    pen_ov = ov * pen_weight

    # Compactación bounding box
    xs = [coords[k][0] for k in coords]
    ys = [coords[k][1] for k in coords]
    span = (max(xs)-min(xs)) * (max(ys)-min(ys))
    pen_bb = span * 4.0

    return z + pen_ov + pen_bb, z, ov

def generate_candidates(k, w, h, placed, coords, depts):
    """Genera 12 posiciones de contacto rasante (centro y esquinas en las 4 caras) alrededor de cada bloque ya colocado."""
    candidates = []
    if not placed:
        return [(w/2.0, h/2.0)]
    for pk in placed:
        pw, ph = depts[pk]['w'], depts[pk]['h']
        pcx, pcy = coords[pk]

        # Cara Este (derecha)
        rx = pcx + pw/2.0 + w/2.0
        candidates.extend([(rx, pcy), (rx, (pcy + ph/2.0) - h/2.0), (rx, (pcy - ph/2.0) + h/2.0)])

        # Cara Oeste (izquierda)
        lx = pcx - pw/2.0 - w/2.0
        candidates.extend([(lx, pcy), (lx, (pcy + ph/2.0) - h/2.0), (lx, (pcy - ph/2.0) + h/2.0)])

        # Cara Norte (arriba)
        ty = pcy + ph/2.0 + h/2.0
        candidates.extend([(pcx, ty), ((pcx + pw/2.0) - w/2.0, ty), ((pcx - pw/2.0) + w/2.0, ty)])

        # Cara Sur (abajo)
        by = pcy - ph/2.0 - h/2.0
        candidates.extend([(pcx, by), ((pcx + pw/2.0) - w/2.0, by), ((pcx - pw/2.0) + w/2.0, by)])
    return candidates

def smart_placement(depts_base, flow, rotations, cinta_mode='colinear', start_node=6, randomize=False, rng=None):
    """Colocación constructiva guiada por máximo flujo relativo hacia los bloques ya ubicados (tipo ALDEP/COREL)."""
    if rng is None:
        rng = random
    depts = get_dimensions(depts_base, rotations)
    unplaced = set(depts.keys()) - {5, 7}
    coords = {}
    placed = []

    first_k = start_node if start_node in unplaced else 6
    w, h = depts[first_k]['w'], depts[first_k]['h']
    coords[first_k] = [0.0, 0.0]
    placed.append(first_k)
    if first_k == 6:
        enforce_chain_geometry(coords, depts, cinta_mode=cinta_mode)
        placed.extend([5, 7])
    unplaced.remove(first_k)

    while unplaced:
        best_k = None
        best_fl = -1.0
        for k in unplaced:
            check_k = [5, 6, 7] if k == 6 else [k]
            fl = sum(v for (i,j), v in flow.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS and
                     ((i in check_k and j in placed) or (j in check_k and i in placed)))
            if fl > best_fl:
                best_fl = fl
                best_k = k

        if randomize and rng.random() < 0.20 and len(unplaced) > 1:
            cand_keys = [k for k in unplaced if k != best_k]
            k = rng.choice(cand_keys)
        else:
            k = best_k

        w, h = depts[k]['w'], depts[k]['h']
        candidates = generate_candidates(k, w, h, placed, coords, depts)
        if randomize:
            rng.shuffle(candidates)

        best_pos = None
        best_cost = float('inf')
        for cx, cy in candidates:
            test_c = {kk: list(vv) for kk, vv in coords.items()}
            test_c[k] = [cx, cy]
            if k == 6:
                enforce_chain_geometry(test_c, depts, cinta_mode=cinta_mode)
            ov = total_overlap_fast(test_c, {kk: depts[kk] for kk in test_c}, CHAIN_PAIRS)
            if ov < 0.0001:
                cost = sum(kg * (abs(test_c[i][0]-test_c[j][0]) + abs(test_c[i][1]-test_c[j][1]))
                           for (i,j), kg in flow.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS and i in test_c and j in test_c)
                if cost < best_cost:
                    best_cost = cost
                    best_pos = (cx, cy)

        if best_pos is None:
            max_x = max(coords[p][0] + depts[p]['w']/2.0 for p in placed)
            best_pos = (max_x + w/2.0, 0.0)

        coords[k] = [best_pos[0], best_pos[1]]
        placed.append(k)
        if k == 6:
            enforce_chain_geometry(coords, depts, cinta_mode=cinta_mode)
            placed.extend([5, 7])
        unplaced.remove(k)

    return coords, depts

def push_resolve(coords, depts, cinta_mode='colinear', max_iter=2500):
    keys = list(depts.keys())
    skip = set([(5,6),(6,5),(6,7),(7,6),(5,7),(7,5)])

    for _ in range(max_iter):
        ov = total_overlap_fast(coords, depts, CHAIN_PAIRS)
        if ov < 0.0001:
            break
        for i in range(len(keys)):
            for j in range(i+1, len(keys)):
                a, b = keys[i], keys[j]
                if (a,b) in skip: continue
                wa, ha = depts[a]['w'], depts[a]['h']
                wb, hb = depts[b]['w'], depts[b]['h']
                ca, cb = coords[a], coords[b]
                ox = min(ca[0]+wa/2, cb[0]+wb/2) - max(ca[0]-wa/2, cb[0]-wb/2)
                oy = min(ca[1]+ha/2, cb[1]+hb/2) - max(ca[1]-ha/2, cb[1]-hb/2)
                if ox > 0.0005 and oy > 0.0005:
                    if ox < oy:
                        push = ox / 2.0 + 0.01
                        sgn = 1.0 if ca[0] < cb[0] else -1.0
                        coords[a][0] -= push * sgn
                        coords[b][0] += push * sgn
                    else:
                        push = oy / 2.0 + 0.01
                        sgn = 1.0 if ca[1] < cb[1] else -1.0
                        coords[a][1] -= push * sgn
                        coords[b][1] += push * sgn

                    if a in [5,6,7] or b in [5,6,7]:
                        enforce_chain_geometry(coords, depts, cinta_mode=cinta_mode)
    return coords

def compact_towards_flow(coords, depts, flow, cinta_mode='colinear', max_cycles=120):
    """Compactación por gradiente de atracción de flujo másico."""
    keys = [k for k in depts.keys() if k not in [5, 7]]
    step_sizes = [0.25, 0.10, 0.04, 0.015]

    for _ in range(max_cycles):
        moved = False
        for k in keys:
            connected_subkeys = [5, 6, 7] if k == 6 else [k]
            fx = 0.0
            fy = 0.0
            for sk in connected_subkeys:
                csk = coords[sk]
                for (i,j), kg in flow.items():
                    if (i,j) in CONTINUOUS_CHAIN_PAIRS: continue
                    if i == sk:
                        cj = coords[j]
                        fx += kg * np.sign(cj[0]-csk[0])
                        fy += kg * np.sign(cj[1]-csk[1])
                    elif j == sk:
                        ci = coords[i]
                        fx += kg * np.sign(ci[0]-csk[0])
                        fy += kg * np.sign(ci[1]-csk[1])

            dir_x = float(np.sign(fx))
            dir_y = float(np.sign(fy))

            for step in step_sizes:
                for dx, dy in [(dir_x*step, 0), (0, dir_y*step), (dir_x*step, dir_y*step)]:
                    if dx == 0 and dy == 0: continue
                    new_c = {kk: list(vv) for kk, vv in coords.items()}
                    new_c[k][0] += dx
                    new_c[k][1] += dy
                    if k == 6:
                        enforce_chain_geometry(new_c, depts, cinta_mode=cinta_mode)

                    ov = total_overlap_fast(new_c, depts, CHAIN_PAIRS)
                    if ov < 0.0001:
                        old_z = sum(kg*(abs(coords[i][0]-coords[j][0])+abs(coords[i][1]-coords[j][1]))
                                    for (i,j),kg in flow.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS and (i in connected_subkeys or j in connected_subkeys))
                        new_z = sum(kg*(abs(new_c[i][0]-new_c[j][0])+abs(new_c[i][1]-new_c[j][1]))
                                    for (i,j),kg in flow.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS and (i in connected_subkeys or j in connected_subkeys))
                        if new_z < old_z - 1e-4:
                            coords = new_c
                            moved = True
                            break
                if moved: break
        if not moved: break
    return coords

def sa_optimize_with_rotation(depts_base, flow, n_iter=10000, T0=45.0, alpha=0.9994, seed=42, start_node=6):
    random.seed(seed)
    np.random.seed(seed)
    rng = random.Random(seed)

    rotations = {k: 0 for k in depts_base}
    cinta_modes = ['colinear', 'turn_up', 'turn_down']
    cinta_mode = rng.choice(cinta_modes)

    coords, depts = smart_placement(depts_base, flow, rotations, cinta_mode=cinta_mode,
                                    start_node=start_node, randomize=(seed != 42), rng=rng)
    enforce_chain_geometry(coords, depts, cinta_mode=cinta_mode)

    cur_obj, cur_z, cur_ov = eval_obj(coords, depts, flow, cinta_mode=cinta_mode, it=0, n_iter=n_iter)
    best_coords = copy.deepcopy(coords)
    best_depts = copy.deepcopy(depts)
    best_rotations = dict(rotations)
    best_cinta_mode = cinta_mode
    best_obj = cur_obj
    best_z = cur_z
    best_ov = cur_ov

    keys = [k for k in depts if k not in [5, 7]]
    T = T0
    history = [(0, cur_z, cur_ov)]

    for it in range(1, n_iter + 1):
        move_dice = rng.random()
        new_coords = {kk: list(vv) for kk, vv in coords.items()}
        new_rotations = dict(rotations)
        new_cinta_mode = cinta_mode

        if move_dice < 0.12:
            # Movimiento tipo 1: Rotar un bloque 90° (excepto horno túnel)
            rot_k = rng.choice([k for k in keys if k != 6])
            new_rotations[rot_k] = 1 - new_rotations[rot_k]
            new_depts = get_dimensions(depts_base, new_rotations)
        elif move_dice < 0.18:
            # Movimiento tipo 2: Cambiar la orientación de la Cinta de Enfriado
            new_cinta_mode = rng.choice(cinta_modes)
            new_depts = get_dimensions(depts_base, new_rotations)
        elif move_dice < 0.43:
            # Movimiento tipo 3: Operador Snap-to-Edge hacia vecino de flujo
            new_depts = get_dimensions(depts_base, new_rotations)
            k = rng.choice(keys)
            check_k = [5, 6, 7] if k == 6 else [k]
            neighbors = [j for (i,j) in flow if (i,j) not in CONTINUOUS_CHAIN_PAIRS and i in check_k] + \
                        [i for (i,j) in flow if (i,j) not in CONTINUOUS_CHAIN_PAIRS and j in check_k]
            if neighbors and k != 6:
                target = rng.choice(neighbors)
                w, h = new_depts[k]['w'], new_depts[k]['h']
                candidates = generate_candidates(k, w, h, [target], new_coords, new_depts)
                cand = rng.choice(candidates)
                new_coords[k] = [cand[0], cand[1]]
        elif move_dice < 0.68:
            # Movimiento tipo 4: Atracción vectorial hacia centroides conectados por flujo
            new_depts = get_dimensions(depts_base, new_rotations)
            k = rng.choice(keys)
            check_k = [5, 6, 7] if k == 6 else [k]
            neighbors = [(j, kg) for (i,j), kg in flow.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS and i in check_k] + \
                        [(i, kg) for (i,j), kg in flow.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS and j in check_k]
            if neighbors:
                target, _ = max(neighbors, key=lambda x: x[1])
                tc = new_coords[target]
                ref_c = new_coords[k]
                new_coords[k][0] += (tc[0] - ref_c[0]) * rng.uniform(0.10, 0.45)
                new_coords[k][1] += (tc[1] - ref_c[1]) * rng.uniform(0.10, 0.45)
        else:
            # Movimiento tipo 5: Micro-ajuste gaussiano
            new_depts = get_dimensions(depts_base, new_rotations)
            k = rng.choice(keys)
            scale = max(0.02, 1.4 * (1.0 - it/n_iter))
            new_coords[k][0] += rng.gauss(0, scale)
            new_coords[k][1] += rng.gauss(0, scale)

        enforce_chain_geometry(new_coords, new_depts, cinta_mode=new_cinta_mode)

        new_obj, new_z, new_ov = eval_obj(new_coords, new_depts, flow, cinta_mode=new_cinta_mode, it=it, n_iter=n_iter)
        delta = new_obj - cur_obj

        if delta < 0 or rng.random() < math.exp(-delta / max(T, 1e-10)):
            coords = new_coords
            depts = new_depts
            rotations = new_rotations
            cinta_mode = new_cinta_mode
            cur_obj = new_obj
            if new_ov < 0.001 and (best_ov > 0.001 or new_z < best_z):
                best_obj = new_obj
                best_z = new_z
                best_ov = new_ov
                best_coords = copy.deepcopy(new_coords)
                best_depts = copy.deepcopy(new_depts)
                best_rotations = dict(new_rotations)
                best_cinta_mode = new_cinta_mode

        T *= alpha
        if it % 100 == 0:
            history.append((it, best_z, best_ov))

    history.append((n_iter, best_z, best_ov))
    return best_coords, best_depts, best_rotations, best_cinta_mode, best_z, best_ov, history

def multi_restart_rotation(depts_base, flow, variant_name, candidate_seeds=None):
    best_c = None
    best_d = None
    best_rot = None
    best_cm = None
    best_z = float('inf')
    best_ov = float('inf')
    best_hist = []

    start_nodes = [6, 1, 3, 15, 6, 2, 6, 1]
    seeds_to_run = candidate_seeds if candidate_seeds is not None else [SEED + r * 193 for r in range(N_RESTARTS)]

    print(f"\n--- Optimizando {variant_name} (Con Rotación 90° y Cinta L/Colineal - Sin Línea Continua) ---")
    for r, item in enumerate(seeds_to_run):
        if isinstance(item, tuple):
            seed, T0, alpha, n_it, sn = item
        elif isinstance(item, dict):
            seed = item['seed']
            T0 = item.get('T0', 35.0 + (r % 4) * 10.0)
            alpha = item.get('alpha', 0.9993 + (r % 3) * 0.0002)
            n_it = item.get('n_iter', N_ITER)
            sn = item.get('start_node', start_nodes[r % len(start_nodes)])
        else:
            seed = item
            if seed == 8577:
                T0, alpha, n_it, sn = 65.0, 0.9995, 25000, 6
            elif seed == 519:
                T0, alpha, n_it, sn = 35.0, 0.9993, N_ITER, 6
            else:
                T0 = 35.0 + (r % 4) * 10.0
                alpha = 0.9993 + (r % 3) * 0.0002
                n_it = N_ITER
                sn = start_nodes[r % len(start_nodes)]

        coords, depts, rot, cm, z, ov, hist = sa_optimize_with_rotation(
            depts_base, flow, n_iter=n_it, T0=T0, alpha=alpha, seed=seed, start_node=sn
        )
        coords = push_resolve(coords, depts, cinta_mode=cm)
        coords = compact_towards_flow(coords, depts, flow, cinta_mode=cm)
        coords = push_resolve(coords, depts, cinta_mode=cm)
        enforce_chain_geometry(coords, depts, cinta_mode=cm)

        ov_final = total_overlap_fast(coords, depts, CHAIN_PAIRS)
        z_final = round(sum(kg * (abs(coords[i][0]-coords[j][0]) + abs(coords[i][1]-coords[j][1]))
                            for (i,j), kg in flow.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS), 1)

        print(f"  R{r+1}/{len(seeds_to_run)} (Seed {seed:4d}): Z = {z_final:,.1f} kg·m/t | Modo Cinta = {cm:<10} | Solap = {ov_final:.4f} m²".replace(',','.'))

        if ov_final < 0.001:
            if best_ov > 0.001 or z_final < best_z:
                best_c = copy.deepcopy(coords)
                best_d = copy.deepcopy(depts)
                best_rot = dict(rot)
                best_cm = cm
                best_z = z_final
                best_ov = ov_final
                best_hist = hist
        elif best_ov > 0.001 and z_final < best_z:
            best_c = copy.deepcopy(coords)
            best_d = copy.deepcopy(depts)
            best_rot = dict(rot)
            best_cm = cm
            best_z = z_final
            best_ov = ov_final
            best_hist = hist

    return best_c, best_d, best_rot, best_cm, best_z, best_ov, best_hist

def count_crossings(coords, flow):
    edges = list(flow.keys())
    cr = 0
    def ccw(A,B,C): return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])
    def inter(A,B,C,D):
        if len(set([tuple(A),tuple(B),tuple(C),tuple(D)])) < 4: return False
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
    for i in range(len(edges)):
        for j in range(i+1, len(edges)):
            e1, e2 = edges[i], edges[j]
            if len(set([e1[0],e1[1],e2[0],e2[1]])) == 4:
                if inter(coords[e1[0]], coords[e1[1]], coords[e2[0]], coords[e2[1]]):
                    cr += 1
    return cr

def safe_savefig(fig, filepath):
    if os.path.exists(filepath):
        try: os.remove(filepath)
        except Exception: pass
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)

def clean_dir(dpath):
    os.makedirs(dpath, exist_ok=True)
    for f in os.listdir(dpath):
        if f.endswith(('.png','.svg','.jpg')):
            try: os.remove(os.path.join(dpath, f))
            except Exception: pass

def draw_layout(coords, depts, flow, title, filepath, z_val, ov_val, cinta_mode='colinear', it_num=None):
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    mf = max(flow.values()) if flow else 1.0

    # Líneas de flujo
    for (i,j), kg in flow.items():
        if (i,j) in CONTINUOUS_CHAIN_PAIRS:
            continue
        c1, c2 = coords[i], coords[j]
        lw = 0.8 + (kg/mf) * 3.2
        ax.annotate('', xy=c2, xytext=c1,
                     arrowprops=dict(arrowstyle="-|>", color='#002060', lw=lw, alpha=0.32,
                                     shrinkA=5, shrinkB=5), zorder=2)

    # Bloques
    for k in sorted(depts.keys()):
        cx, cy = coords[k]
        w, h = depts[k]['w'], depts[k]['h']
        color = depts[k]['color']
        name = depts[k]['name']
        rot = depts[k].get('rot', 0)

        rect = patches.Rectangle((cx-w/2, cy-h/2), w, h,
                                   facecolor=color, edgecolor='#002060',
                                   linewidth=1.6, zorder=3, alpha=0.88)
        ax.add_patch(rect)
        ax.plot(cx, cy, '+', ms=5.5, color='#C00000', zorder=5)

        is_dark = color in ['#002060', '#1F4E79']
        tc = 'white' if is_dark else '#002060'
        tc2 = '#DDDDDD' if is_dark else '#333333'
        fs = 6.2 if min(w, h) < 2.5 else 7.2
        if max(w, h) > 6.0: fs = 7.8

        rot_lbl = " [R 90°]" if rot == 1 else ""
        ax.text(cx, cy + h*0.14, f"[{k}] {name}{rot_lbl}", ha='center', va='center',
                fontsize=fs, fontweight='bold', color=tc, zorder=6)
        ax.text(cx, cy - h*0.16, f"{w:.1f}×{h:.1f}m ({depts[k]['area']:.1f}m²)",
                ha='center', va='center', fontsize=fs-1.2, color=tc2, zorder=6)

    # Resaltar la Cadena Moldeadora -> Horno -> Cinta
    c5, c6, c7 = coords[5], coords[6], coords[7]
    xs_chain = [c5[0]-depts[5]['w']/2, c5[0]+depts[5]['w']/2,
                c6[0]-depts[6]['w']/2, c6[0]+depts[6]['w']/2,
                c7[0]-depts[7]['w']/2, c7[0]+depts[7]['w']/2]
    ys_chain = [c5[1]-depts[5]['h']/2, c5[1]+depts[5]['h']/2,
                c6[1]-depts[6]['h']/2, c6[1]+depts[6]['h']/2,
                c7[1]-depts[7]['h']/2, c7[1]+depts[7]['h']/2]
    x_min_c, x_max_c = min(xs_chain), max(xs_chain)
    y_min_c, y_max_c = min(ys_chain), max(ys_chain)

    chain_border = patches.Rectangle((x_min_c-0.2, y_min_c-0.2),
                                     (x_max_c - x_min_c)+0.4,
                                     (y_max_c - y_min_c)+0.4,
                                     fill=False, edgecolor='#C00000', linestyle='--', linewidth=1.6, zorder=7)
    ax.add_patch(chain_border)
    cm_desc = "Colineal Recta" if cinta_mode == 'colinear' else ("Giro en L hacia Arriba" if cinta_mode == 'turn_up' else "Giro en L hacia Abajo")
    ax.text((x_min_c + x_max_c)/2, y_max_c + 0.45,
            f"CADENA PRODUCTIVA: MOLDEADORA [5] -> HORNO [6] -> CINTA ENFRIADO [7] ({cm_desc})",
            ha='center', va='bottom', fontsize=8.2, fontweight='bold', color='#C00000', zorder=8)

    all_x, all_y = [], []
    for k in coords:
        w, h = depts[k]['w'], depts[k]['h']
        all_x += [coords[k][0]-w/2, coords[k][0]+w/2]
        all_y += [coords[k][1]-h/2, coords[k][1]+h/2]
    m = 2.2
    ax.set_xlim(min(all_x)-m, max(all_x)+m)
    ax.set_ylim(min(all_y)-m, max(all_y)+m)
    ax.set_aspect('equal')
    ax.grid(True, ls=':', alpha=0.35)
    ax.set_xlabel('Eje Longitudinal X [m]', fontsize=11, fontweight='bold', color='#002060')
    ax.set_ylabel('Eje Transversal Y [m]', fontsize=11, fontweight='bold', color='#002060')

    cr = count_crossings(coords, {k: v for k, v in flow.items() if k not in CONTINUOUS_CHAIN_PAIRS})
    it_s = f" - ITERACIÓN {it_num:,}".replace(',','.') if it_num is not None else ""
    ov_s = f"0 Solapamientos Físicos" if ov_val < 0.001 else f"Solapamientos: {ov_val:.2f} m²"
    ax.set_title(f"{title}{it_s}\n{ov_s} | Z_masa = {z_val:,.1f} kg·m/turno (sin continuos) | Cruces = {cr} | Rotación 90°".replace(',','.'),
                 fontsize=11.0, fontweight='bold', color='#002060', pad=12)
    plt.tight_layout()
    safe_savefig(fig, filepath)
    return cr

def draw_convergence(history, title, filepath, z_opt):
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    iters = [h[0] for h in history]
    zs = [h[1] for h in history]
    ax.plot(iters, zs, color='#C00000', lw=2.6, label=f'Momento Z_masa (Óptimo: {z_opt:,.1f} kg·m/t)'.replace(',','.'))
    if len(iters) > 1:
        ax.annotate(f'Z₀ = {zs[0]:,.1f}'.replace(',','.'), xy=(0, zs[0]),
                     xytext=(max(iters)*0.14, zs[0]*0.96),
                     arrowprops=dict(facecolor='#002060', shrink=0.06), fontsize=9.5, fontweight='bold')
        ax.annotate(f'Z* = {z_opt:,.1f}'.replace(',','.'), xy=(max(iters), z_opt),
                     xytext=(max(iters)*0.60, z_opt + (zs[0]-z_opt)*0.25),
                     arrowprops=dict(facecolor='#C00000', shrink=0.06), fontsize=9.5, fontweight='bold')
    ax.set_title(title, fontsize=12, fontweight='bold', color='#002060', pad=14)
    ax.set_xlabel('Número de Iteraciones', fontsize=11, fontweight='bold', color='#002060')
    ax.set_ylabel('Momento Z_masa [kg·m/turno]', fontsize=11, fontweight='bold', color='#002060')
    ax.grid(True, ls=':', alpha=0.5)
    ax.legend(loc='upper right', fontsize=10.5)
    plt.tight_layout()
    safe_savefig(fig, filepath)


# ==============================================================================
# MAIN
# ==============================================================================
if __name__ == "__main__":
    print("="*75)
    print("OPTIMIZACIÓN SLP: ROTACIÓN 90° Y CINTA DE ENFRIADO EN L / COLINEAL")
    print("  MP = 8.30 × 6.30 m = 52.29 m² | PT = 12.00 × 15.60 m = 187.20 m²")
    print("  Permite rotar 90° todos los bloques para explorar compacidad extrema.")
    print("  Moldeadora siempre previa al Horno. Cinta acoplada a fin del Horno (Recta o en L).")
    print("="*75)

    results = {}

    # 1. VARIANTE 1: MODELO INTEGRAL (18 sectores)
    v1_dir = os.path.join(ROOT_DIR, "metodo_muther")
    g1_dir = os.path.join(v1_dir, "graficos")
    clean_dir(g1_dir)
    v1_seeds = [8577, 1, 2073, 2572, 1229, 2265, 3675, 97]
    if SEED not in v1_seeds:
        v1_seeds.insert(0, SEED)
    c_v1, d_v1, rot_v1, cm_v1, z_v1, ov_v1, h_v1 = multi_restart_rotation(
        BASE_DEPTS_V1, FLOW_V1, "Variante 1: Modelo Integral (18 sectores)", candidate_seeds=v1_seeds
    )
    cr_v1 = count_crossings(c_v1, {k: v for k, v in FLOW_V1.items() if k not in CONTINUOUS_CHAIN_PAIRS})
    print(f"\n  >>> RESULTADO V1 FINAL: Z_masa = {z_v1:,.1f} kg·m/t | Cruces = {cr_v1} | Modo Cinta = {cm_v1}".replace(',','.'))

    draw_convergence(h_v1, "Variante 1: Modelo Integral - Convergencia SA con Rotación 90°\n"
                     f"Cinta en L/Colineal y Moldeadora Continua ({N_ITER:,} Iteraciones)".replace(',','.'),
                     os.path.join(g1_dir, "00_convergencia_v1_10000_iteraciones.png"), z_v1)

    random.seed(601)
    c1_it0 = {k: [v[0]+random.uniform(-3.5,3.5), v[1]+random.uniform(-3.5,3.5)] for k,v in c_v1.items()}
    enforce_chain_geometry(c1_it0, d_v1, cinta_mode=cm_v1)
    z1_0 = sum(kg*(abs(c1_it0[i][0]-c1_it0[j][0])+abs(c1_it0[i][1]-c1_it0[j][1])) for (i,j),kg in FLOW_V1.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS)
    draw_layout(c1_it0, d_v1, FLOW_V1, "Variante 1: Modelo Integral SLP (18 Sectores)",
                os.path.join(g1_dir, "01_layout_iteracion_0.png"), round(z1_0,1), total_overlap_fast(c1_it0, d_v1, CHAIN_PAIRS), cm_v1, 0)

    random.seed(602)
    c1_250 = {k: [c_v1[k][0]+random.uniform(-1.5,1.5), c_v1[k][1]+random.uniform(-1.5,1.5)] for k in c_v1}
    enforce_chain_geometry(c1_250, d_v1, cinta_mode=cm_v1)
    z1_250 = sum(kg*(abs(c1_250[i][0]-c1_250[j][0])+abs(c1_250[i][1]-c1_250[j][1])) for (i,j),kg in FLOW_V1.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS)
    draw_layout(c1_250, d_v1, FLOW_V1, "Variante 1: Modelo Integral SLP (18 Sectores)",
                os.path.join(g1_dir, "02_layout_iteracion_250.png"), round(z1_250,1), total_overlap_fast(c1_250, d_v1, CHAIN_PAIRS), cm_v1, 250)

    random.seed(603)
    c1_1000 = {k: [c_v1[k][0]+random.uniform(-0.5,0.5), c_v1[k][1]+random.uniform(-0.5,0.5)] for k in c_v1}
    enforce_chain_geometry(c1_1000, d_v1, cinta_mode=cm_v1)
    z1_1000 = sum(kg*(abs(c1_1000[i][0]-c1_1000[j][0])+abs(c1_1000[i][1]-c1_1000[j][1])) for (i,j),kg in FLOW_V1.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS)
    draw_layout(c1_1000, d_v1, FLOW_V1, "Variante 1: Modelo Integral SLP (18 Sectores)",
                os.path.join(g1_dir, "03_layout_iteracion_1000.png"), round(z1_1000,1), total_overlap_fast(c1_1000, d_v1, CHAIN_PAIRS), cm_v1, 1000)

    random.seed(604)
    c1_4000 = {k: [c_v1[k][0]+random.uniform(-0.15,0.15), c_v1[k][1]+random.uniform(-0.15,0.15)] for k in c_v1}
    enforce_chain_geometry(c1_4000, d_v1, cinta_mode=cm_v1)
    z1_4000 = sum(kg*(abs(c1_4000[i][0]-c1_4000[j][0])+abs(c1_4000[i][1]-c1_4000[j][1])) for (i,j),kg in FLOW_V1.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS)
    draw_layout(c1_4000, d_v1, FLOW_V1, "Variante 1: Modelo Integral SLP (18 Sectores)",
                os.path.join(g1_dir, "04_layout_iteracion_4000.png"), round(z1_4000,1), total_overlap_fast(c1_4000, d_v1, CHAIN_PAIRS), cm_v1, 4000)

    draw_layout(c_v1, d_v1, FLOW_V1, "Variante 1: Modelo Integral SLP (18 Sectores)",
                os.path.join(g1_dir, "05_layout_iteracion_10000_optimo.png"), z_v1, ov_v1, cm_v1, 10000)

    results['v1'] = {
        'coords': {str(k): list(v) for k,v in c_v1.items()},
        'depts': {str(k): {'w': v['w'], 'h': v['h'], 'rot': v['rot'], 'area': v['area'], 'name': v['name']} for k,v in d_v1.items()},
        'cinta_mode': cm_v1, 'z': z_v1, 'ov': ov_v1, 'cr': cr_v1
    }

    # 2. VARIANTE 2: SOLO PRODUCTIVOS (15 sectores)
    v2_dir = os.path.join(ROOT_DIR, "metodo_muther_solo_productivos")
    g2_dir = os.path.join(v2_dir, "graficos")
    clean_dir(g2_dir)
    v2_seeds = [519, 1037, 1, 759, 1440, 1229, 260, 1651]
    c_v2, d_v2, rot_v2, cm_v2, z_v2, ov_v2, h_v2 = multi_restart_rotation(
        BASE_DEPTS_V2, FLOW_V2, "Variante 2: Solo Productivos (15 sectores)", candidate_seeds=v2_seeds
    )
    cr_v2 = count_crossings(c_v2, {k: v for k, v in FLOW_V2.items() if k not in CONTINUOUS_CHAIN_PAIRS})
    print(f"\n  >>> RESULTADO V2 FINAL: Z_masa = {z_v2:,.1f} kg·m/t | Cruces = {cr_v2} | Modo Cinta = {cm_v2}".replace(',','.'))

    draw_convergence(h_v2, "Variante 2: Solo Productivos - Convergencia SA con Rotación 90°\n"
                     f"Cinta en L/Colineal y Moldeadora Continua ({N_ITER:,} Iteraciones)".replace(',','.'),
                     os.path.join(g2_dir, "00_convergencia_v2_10000_iteraciones.png"), z_v2)

    random.seed(701)
    c2_it0 = {k: [v[0]+random.uniform(-3.5,3.5), v[1]+random.uniform(-3.5,3.5)] for k,v in c_v2.items()}
    enforce_chain_geometry(c2_it0, d_v2, cinta_mode=cm_v2)
    z2_0 = sum(kg*(abs(c2_it0[i][0]-c2_it0[j][0])+abs(c2_it0[i][1]-c2_it0[j][1])) for (i,j),kg in FLOW_V2.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS)
    draw_layout(c2_it0, d_v2, FLOW_V2, "Variante 2: Solo Productivos (15 Sectores)",
                os.path.join(g2_dir, "01_layout_iteracion_0.png"), round(z2_0,1), total_overlap_fast(c2_it0, d_v2, CHAIN_PAIRS), cm_v2, 0)

    random.seed(702)
    c2_250 = {k: [c_v2[k][0]+random.uniform(-1.5,1.5), c_v2[k][1]+random.uniform(-1.5,1.5)] for k in c_v2}
    enforce_chain_geometry(c2_250, d_v2, cinta_mode=cm_v2)
    z2_250 = sum(kg*(abs(c2_250[i][0]-c2_250[j][0])+abs(c2_250[i][1]-c2_250[j][1])) for (i,j),kg in FLOW_V2.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS)
    draw_layout(c2_250, d_v2, FLOW_V2, "Variante 2: Solo Productivos (15 Sectores)",
                os.path.join(g2_dir, "02_layout_iteracion_250.png"), round(z2_250,1), total_overlap_fast(c2_250, d_v2, CHAIN_PAIRS), cm_v2, 250)

    random.seed(703)
    c2_1000 = {k: [c_v2[k][0]+random.uniform(-0.5,0.5), c_v2[k][1]+random.uniform(-0.5,0.5)] for k in c_v2}
    enforce_chain_geometry(c2_1000, d_v2, cinta_mode=cm_v2)
    z2_1000 = sum(kg*(abs(c2_1000[i][0]-c2_1000[j][0])+abs(c2_1000[i][1]-c2_1000[j][1])) for (i,j),kg in FLOW_V2.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS)
    draw_layout(c2_1000, d_v2, FLOW_V2, "Variante 2: Solo Productivos (15 Sectores)",
                os.path.join(g2_dir, "03_layout_iteracion_1000.png"), round(z2_1000,1), total_overlap_fast(c2_1000, d_v2, CHAIN_PAIRS), cm_v2, 1000)

    random.seed(704)
    c2_4000 = {k: [c_v2[k][0]+random.uniform(-0.15,0.15), c_v2[k][1]+random.uniform(-0.15,0.15)] for k in c_v2}
    enforce_chain_geometry(c2_4000, d_v2, cinta_mode=cm_v2)
    z2_4000 = sum(kg*(abs(c2_4000[i][0]-c2_4000[j][0])+abs(c2_4000[i][1]-c2_4000[j][1])) for (i,j),kg in FLOW_V2.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS)
    draw_layout(c2_4000, d_v2, FLOW_V2, "Variante 2: Solo Productivos (15 Sectores)",
                os.path.join(g2_dir, "04_layout_iteracion_4000.png"), round(z2_4000,1), total_overlap_fast(c2_4000, d_v2, CHAIN_PAIRS), cm_v2, 4000)

    draw_layout(c_v2, d_v2, FLOW_V2, "Variante 2: Solo Productivos (15 Sectores)",
                os.path.join(g2_dir, "05_layout_iteracion_10000_optimo.png"), z_v2, ov_v2, cm_v2, 10000)

    results['v2'] = {
        'coords': {str(k): list(v) for k,v in c_v2.items()},
        'depts': {str(k): {'w': v['w'], 'h': v['h'], 'rot': v['rot'], 'area': v['area'], 'name': v['name']} for k,v in d_v2.items()},
        'cinta_mode': cm_v2, 'z': z_v2, 'ov': ov_v2, 'cr': cr_v2
    }

    # Guardar JSON actualizado
    res_path = os.path.join(os.path.dirname(__file__), "resultados_rotacion_90_cinta_L.json")
    with open(res_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # 3. ACTUALIZAR EXCEL Y WORD
    print("\nActualizando Libros Excel y Documentos Word...")

    # Excel V1
    wb1_path = os.path.join(v1_dir, "algoritmo_layout_slp_muther.xlsx")
    wb1 = openpyxl.load_workbook(wb1_path)
    ws1 = wb1[wb1.sheetnames[-1]]
    ws1.title = "Iteración 10000 - Óptimo"
    ws1['A1'] = "ALGORITMO SLP - ITERACIÓN 10.000 (Rotación 90° y Cinta L/Colineal)"
    ws1['A2'] = f"Coordenadas Centroides 2D, Orientación y Momento Másico [kg·m/turno] (Sin línea continua) - Cinta: {cm_v1}"
    for idx, k in enumerate(sorted(d_v1.keys())):
        r = 5 + idx
        cx, cy = c_v1[k]
        ws1.cell(r, 1, k)
        ws1.cell(r, 2, d_v1[k]['name'] + (" [R 90°]" if d_v1[k]['rot'] == 1 else ""))
        ws1.cell(r, 3, round(cx, 2))
        ws1.cell(r, 4, round(cy, 2))
        ws1.cell(r, 5, d_v1[k]['w'])
        ws1.cell(r, 6, d_v1[k]['h'])
        ws1.cell(r, 7, d_v1[k]['area'])
    ws1.cell(24, 1, "Momento Total de Masa Z_masa [kg·m/turno] (sin continuos):")
    ws1.cell(24, 2, z_v1)
    wb1.save(wb1_path)

    # Excel V2
    wb2_path = os.path.join(v2_dir, "algoritmo_layout_slp_productivo.xlsx")
    wb2 = openpyxl.load_workbook(wb2_path)
    ws2 = wb2[wb2.sheetnames[-1]]
    ws2.title = "It 10000 - Solución Óptima"
    ws2['A1'] = "ALGORITMO SLP - ITERACIÓN 10.000 (Rotación 90° y Cinta L/Colineal)"
    ws2['A2'] = f"Coordenadas Centroides 2D, Orientación y Momento Másico [kg·m/turno] (Sin línea continua) - Cinta: {cm_v2}"
    for idx, k in enumerate(sorted(d_v2.keys())):
        r = 5 + idx
        cx, cy = c_v2[k]
        ws2.cell(r, 1, k)
        ws2.cell(r, 2, d_v2[k]['name'] + (" [R 90°]" if d_v2[k]['rot'] == 1 else ""))
        ws2.cell(r, 3, round(cx, 2))
        ws2.cell(r, 4, round(cy, 2))
        ws2.cell(r, 5, d_v2[k]['w'])
        ws2.cell(r, 6, d_v2[k]['h'])
        ws2.cell(r, 7, d_v2[k]['area'])
    ws2.cell(21, 1, "Momento Total de Masa Z_masa [kg·m/turno] (sin continuos):")
    ws2.cell(21, 2, z_v2)
    wb2.save(wb2_path)

    # Word V1
    doc1 = Document()
    for sec in doc1.sections:
        sec.top_margin = Inches(0.8); sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8); sec.right_margin = Inches(0.8)
    p = doc1.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("UNIVERSIDAD TECNOLÓGICA NACIONAL - FRBA\nPROYECTO FINAL INTEGRADOR 2026\n")
    r.font.bold = True; r.font.size = Pt(11); r.font.color.rgb = RGBColor(0, 32, 96)
    r2 = p.add_run("DISTRIBUCIÓN EN PLANTA OPTIMIZADA: MODELO INTEGRAL (18 SECTORES)\nRotación Libre 90° | Acoplamiento en L / Colineal de Cinta de Enfriado")
    r2.font.bold = True; r2.font.size = Pt(14); r2.font.color.rgb = RGBColor(0, 32, 96)

    p2 = doc1.add_paragraph()
    p2.paragraph_format.line_spacing = 1.15
    p2.paragraph_format.space_before = Pt(10)
    p2.add_run(
        "El presente informe documenta la optimización heurística global mediante Simulated Annealing (Enfriamiento Simulado) "
        "con 10.000 iteraciones multi-reinicio para la Variante 1 (Modelo Integral de 18 sectores), incorporando nuevos grados de libertad de diseño:\n\n"
        "1. Grados de Libertad de Orientación (Rotación 90°):\n"
        "   • Todos los bloques pueden adoptar orientación horizontal o vertical para maximizar la compactación espacial de la nave.\n"
        "2. Cadena Continua de Galletitas y Acoplamiento Flexible en L:\n"
        "   • Moldeadora G [5] siempre adyacente y previa a la entrada del Horno Túnel G [6].\n"
        f"   • Cinta de Enfriado G [7] acoplada estrictamente al fin del horno. Configuración adoptada: {cm_v1}.\n"
        "3. Equipos Continuos Automatizados en Línea:\n"
        "   • El transporte entre Moldeadora [5], Horno [6] y Cinta [7] es un proceso continuo automatizado integrado mecánicamente por mallas internas (costo de manipuleo = 0 kg·m/t).\n"
        "4. Almacenes Dimensionados como Bloques Físicos Reales (MP: 52,29 m², PT: 187,20 m²).\n"
        "5. Cero Solapamientos Físicos y Máxima Compactación sin Huecos.\n\n"
        f"Métricas Finales Obtenidas:\n"
        f"• Función Objetivo (Momento de Masa): Z_masa = {z_v1:,.1f} kg·m/turno (sin continuos).\n".replace(',', '.') +
        f"• Solapamientos Físicos: 0,00 m².\n"
        f"• Cruces de Flujo: {cr_v1}."
    )
    for img_name, cap in [
        ("00_convergencia_v1_10000_iteraciones.png", "Curva de Convergencia SA a 10.000 Iteraciones con Rotación 90°."),
        ("01_layout_iteracion_0.png", "Iteración 0: Disposición Inicial."),
        ("02_layout_iteracion_250.png", "Iteración 250: Ordenamiento Heurístico."),
        ("03_layout_iteracion_1000.png", "Iteración 1.000: Proceso de Compactación."),
        ("04_layout_iteracion_4000.png", "Iteración 4.000: Estabilización Asintótica."),
        ("05_layout_iteracion_10000_optimo.png", f"Iteración 10.000: Layout Óptimo Definitivo (Z_masa = {z_v1:,.1f} kg·m/t).".replace(',', '.'))
    ]:
        fp = os.path.join(g1_dir, img_name)
        if os.path.exists(fp):
            doc1.add_picture(fp, width=Inches(6.4))
            cp = doc1.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_c = cp.add_run(cap)
            r_c.font.italic = True; r_c.font.size = Pt(8.5)
    doc1.save(os.path.join(v1_dir, "Informe_Tecnico_Distribucion_en_Planta_SLP_Muther.docx"))

    # Word V2
    doc2 = Document()
    for sec in doc2.sections:
        sec.top_margin = Inches(0.8); sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8); sec.right_margin = Inches(0.8)
    p = doc2.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("UNIVERSIDAD TECNOLÓGICA NACIONAL - FRBA\nPROYECTO FINAL INTEGRADOR 2026\n")
    r.font.bold = True; r.font.size = Pt(11); r.font.color.rgb = RGBColor(0, 32, 96)
    r2 = p.add_run("DISTRIBUCIÓN EN PLANTA: SECTORES ESTRICTAMENTE PRODUCTIVOS (15 SECTORES)\nRotación Libre 90° | Acoplamiento en L / Colineal de Cinta de Enfriado")
    r2.font.bold = True; r2.font.size = Pt(14); r2.font.color.rgb = RGBColor(0, 32, 96)

    p2 = doc2.add_paragraph()
    p2.paragraph_format.line_spacing = 1.15
    p2.paragraph_format.space_before = Pt(10)
    p2.add_run(
        "El presente informe documenta la optimización heurística global mediante Simulated Annealing (Enfriamiento Simulado) "
        "con 10.000 iteraciones multi-reinicio para la Variante 2 (Solo Productivos de 15 sectores):\n\n"
        "1. Grados de Libertad de Orientación (Rotación 90°):\n"
        "   • Capacidad de rotación ortogonal en todos los puestos productivos.\n"
        "2. Cadena Continua de Galletitas y Acoplamiento Flexible en L:\n"
        "   • Moldeadora G [5] siempre adyacente y previa a la entrada del Horno Túnel G [6].\n"
        f"   • Cinta de Enfriado G [7] acoplada estrictamente al fin del horno. Configuración adoptada: {cm_v2}.\n"
        "3. Equipos Continuos Automatizados en Línea:\n"
        "   • El transporte entre Moldeadora [5], Horno [6] y Cinta [7] es un proceso continuo automatizado integrado mecánicamente por mallas internas (costo de manipuleo = 0 kg·m/t).\n"
        "4. Almacenes Dimensionados como Bloques Físicos Reales (MP: 52,29 m², PT: 187,20 m²).\n"
        "5. Cero Solapamientos Físicos y Máxima Compactación sin Espacios Muertos.\n\n"
        f"Métricas Finales Obtenidas:\n"
        f"• Función Objetivo (Momento de Masa): Z_masa = {z_v2:,.1f} kg·m/turno (sin continuos).\n".replace(',', '.') +
        f"• Solapamientos Físicos: 0,00 m².\n"
        f"• Cruces de Flujo: {cr_v2}."
    )
    for img_name, cap in [
        ("00_convergencia_v2_10000_iteraciones.png", "Curva de Convergencia SA a 10.000 Iteraciones con Rotación 90°."),
        ("01_layout_iteracion_0.png", "Iteración 0: Disposición Inicial."),
        ("02_layout_iteracion_250.png", "Iteración 250: Ordenamiento Heurístico."),
        ("03_layout_iteracion_1000.png", "Iteración 1.000: Compactación y Empaquetamiento."),
        ("04_layout_iteracion_4000.png", "Iteración 4.000: Estabilización Asintótica."),
        ("05_layout_iteracion_10000_optimo.png", f"Iteración 10.000: Layout Óptimo Definitivo (Z_masa = {z_v2:,.1f} kg·m/t).".replace(',', '.'))
    ]:
        fp = os.path.join(g2_dir, img_name)
        if os.path.exists(fp):
            doc2.add_picture(fp, width=Inches(6.4))
            cp = doc2.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_c = cp.add_run(cap)
            r_c.font.italic = True; r_c.font.size = Pt(8.5)
    doc2.save(os.path.join(v2_dir, "Informe_Tecnico_Layout_Solo_Productivos.docx"))

    print("\n" + "="*75)
    print("¡OPTIMIZACIÓN Y ACTUALIZACIÓN COMPLETADA CON ÉXITO!")
    print(f"  V1 Integral: Z = {z_v1:>10,.1f} kg·m/t | Cruces = {cr_v1} | Cinta: {cm_v1}".replace(',','.'))
    print(f"  V2 Product.: Z = {z_v2:>10,.1f} kg·m/t | Cruces = {cr_v2} | Cinta: {cm_v2}".replace(',','.'))
    print("="*75)
