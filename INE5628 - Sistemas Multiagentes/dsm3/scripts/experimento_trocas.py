"""Experimento do DSM3: efeito das trocas de vagas (seat_swap) no cenário S1, com e sem trocas, 15 sementes.

Uso:  python scripts/experimento_trocas.py > docs/evidencias/experimento_trocas.txt
"""
from collections import Counter
from statistics import mean

from matriculaufsc.metrics import summarize
from matriculaufsc.scenarios import build
from matriculaufsc.sim import Simulation

SEEDS = range(1, 16)


def rodar(seed, swaps):
    sc = build("S1", seed, 16)
    sim = Simulation(sc, seed, config={"swaps": swaps}).run()
    r = summarize(sim.registrar, sc, sim.trace)
    trocas = sum(1 for x in sim.trace.of_kind("registrar") if x["op"] == "swap_enroll" and x["ok"])
    pedidos = sum(1 for x in sim.trace.of_kind("msg") if x["protocol"] == "seat_swap" and x["perf"] == "request")
    msgs = sum(r["mensagens"].values())
    return {"U": r["U_medio"], "sat": r["pct_satisfatoria"], "gini": r["gini_U"], "msgs": msgs, "trocas": trocas,
            "pedidos": pedidos, "inv": r["invariantes_violadas"]}


def main():
    com = {s: rodar(s, True) for s in SEEDS}
    sem = {s: rodar(s, False) for s in SEEDS}
    print("S1, 16 alunos, 15 sementes: leilão com trocas x leilão sem trocas\n")
    print(f"{'semente':>7} {'U sem':>7} {'U com':>7} {'sat% sem':>9} {'sat% com':>9} {'pedidos':>8} {'trocas':>7} {'msgs +':>7}")
    for s in SEEDS:
        a, b = sem[s], com[s]
        print(f"{s:>7} {a['U']:>7.3f} {b['U']:>7.3f} {a['sat']:>9.1f} {b['sat']:>9.1f} {b['pedidos']:>8} {b['trocas']:>7} {b['msgs'] - a['msgs']:>7}")
    print()
    for k, nome in (("U", "U médio"), ("sat", "% satisfatórias"), ("gini", "Gini de U"), ("msgs", "mensagens")):
        print(f"{nome:16s} sem trocas {mean(sem[s][k] for s in SEEDS):8.3f}   com trocas {mean(com[s][k] for s in SEEDS):8.3f}")
    melhor = sum(com[s]["U"] > sem[s]["U"] + 1e-9 for s in SEEDS)
    pior = sum(com[s]["U"] < sem[s]["U"] - 1e-9 for s in SEEDS)
    print(f"\nsementes com U médio maior: {melhor}; igual: {len(SEEDS) - melhor - pior}; menor: {pior}")
    print(f"trocas concluídas no total: {sum(com[s]['trocas'] for s in SEEDS)} em {sum(com[s]['pedidos'] for s in SEEDS)} pedidos")
    print("invariantes violadas:", [v for s in SEEDS for v in com[s]["inv"] + sem[s]["inv"]] or "nenhuma")


if __name__ == "__main__":
    main()
