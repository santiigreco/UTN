"""
SEED HUNTER - Búsqueda Paralela Multi-Core de Semillas Óptimas para SLP Muther
Explora decenas de semillas en paralelo usando todos los núcleos del CPU
para encontrar configuraciones con Z_masa < 35.000 kg·m/t (sin transferencias continuas).
"""
import os, sys, time, json
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

# Importar funciones y constantes del algoritmo oficial
from ejecutar_algoritmo_slp import (
    BASE_DEPTS_V1, FLOW_V1,
    BASE_DEPTS_V2, FLOW_V2,
    CHAIN_PAIRS, CONTINUOUS_CHAIN_PAIRS,
    get_dimensions, enforce_chain_geometry,
    total_overlap_fast, push_resolve,
    compact_towards_flow, sa_optimize_with_rotation
)

def evaluate_single_seed(args):
    """Evalúa una semilla candidata para una variante dada."""
    seed_val, variant_name, n_iter, start_node, T0, alpha = args
    depts_base = BASE_DEPTS_V2 if variant_name == 'v2' else BASE_DEPTS_V1
    flow = FLOW_V2 if variant_name == 'v2' else FLOW_V1

    coords, depts, rot, cm, z, ov, _ = sa_optimize_with_rotation(
        depts_base, flow, n_iter=n_iter, T0=T0, alpha=alpha, seed=seed_val, start_node=start_node
    )
    coords = push_resolve(coords, depts, cinta_mode=cm)
    coords = compact_towards_flow(coords, depts, flow, cinta_mode=cm)
    coords = push_resolve(coords, depts, cinta_mode=cm)
    enforce_chain_geometry(coords, depts, cinta_mode=cm)

    ov_final = total_overlap_fast(coords, depts, CHAIN_PAIRS)
    z_final = round(sum(kg * (abs(coords[i][0]-coords[j][0]) + abs(coords[i][1]-coords[j][1]))
                        for (i,j), kg in flow.items() if (i,j) not in CONTINUOUS_CHAIN_PAIRS), 1)

    return {
        'seed': seed_val,
        'variant': variant_name,
        'z': z_final,
        'ov': ov_final,
        'cinta_mode': cm,
        'start_node': start_node
    }

def hunt_seeds(variant='v2', num_seeds=100, n_iter=25000):
    cpu_count = os.cpu_count() or 4
    print(f"\n{'='*75}")
    print(f"🎯 INICIANDO SEED HUNTER ({variant.upper()}) | CPUs detectados: {cpu_count}")
    print(f"   Evaluando {num_seeds} semillas con {n_iter:,} iteraciones cada una...")
    print(f"{'='*75}")

    start_nodes = [6, 1, 3, 200, 6, 2, 6, 1]
    tasks = []
    for idx in range(num_seeds):
        s = 1 + idx * 37 + (idx % 7) * 11
        sn = start_nodes[idx % len(start_nodes)]
        T0 = 35.0 + (idx % 4) * 10.0
        alpha = 0.9993 + (idx % 3) * 0.0002
        tasks.append((s, variant, n_iter, sn, T0, alpha))

    best_result = None
    results = []
    completed = 0
    t0 = time.time()

    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        futures = {executor.submit(evaluate_single_seed, t): t[0] for t in tasks}
        for future in as_completed(futures):
            res = future.result()
            completed += 1
            if res['ov'] < 0.001:
                results.append(res)
                is_record = False
                if best_result is None or res['z'] < best_result['z']:
                    best_result = res
                    is_record = True

                rec_tag = " ⭐ NUEVO RÉCORD!" if is_record else ""
                goal_tag = " 🏆 ¡OBJETIVO < 35.000 ALCANZADO!" if res['z'] < 35000 else ""
                print(f" [{completed:2d}/{num_seeds}] Seed {res['seed']:5d} | Z = {res['z']:,.1f} kg·m/t | Cinta: {res['cinta_mode']:<10}{rec_tag}{goal_tag}".replace(',','.'))

    results.sort(key=lambda x: x['z'])
    t_elapsed = time.time() - t0

    print(f"\n{'='*75}")
    print(f"🏁 CACERÍA FINALIZADA en {t_elapsed:.1f} segundos")
    print(f"TOP 5 MEJORES SEMILLAS ({variant.upper()}):")
    for i, r in enumerate(results[:5], 1):
        print(f"  {i}. SEED = {r['seed']:<5d} -> Z = {r['z']:,.1f} kg·m/t (Modo Cinta: {r['cinta_mode']})".replace(',','.'))
    print(f"{'='*75}")

    if best_result and best_result['z'] < 35000:
        print(f"\n🎉 ¡ÉXITO TOTAL! Puedes colocar SEED = {best_result['seed']} en ejecutar_algoritmo_slp.py")
    return results

if __name__ == "__main__":
    # 1. Cazar para V2 (Solo Productivos)
    top_v2 = hunt_seeds(variant='v2', num_seeds=0, n_iter=25000)

    # 2. Cazar para V1 (Modelo Integral)
    top_v1 = hunt_seeds(variant='v1', num_seeds=500, n_iter=25000)

    with open("mejores_seeds.json", "w", encoding="utf-8") as f:
        json.dump({'v2': top_v2[:10], 'v1': top_v1[:10]}, f, indent=4)
    print("\n💾 Resultados guardados exitosamente en 'mejores_seeds.json'")
