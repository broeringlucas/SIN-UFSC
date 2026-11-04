"""CLI:  python -m matriculaufsc --scenario S0 --seed 7 --trace out/trace.jsonl"""

from __future__ import annotations

import argparse
import json
import sys

from .baselines import compare_policies, opened_snapshot, run_baseline
from .metrics import student_results, summarize
from .scenarios import build
from .sim import Simulation


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="matriculaufsc", description="MatriculaUFSC — protótipo SMA (DSM2)")
    ap.add_argument("--scenario", default="S0", choices=["S0", "S1"])
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--students", type=int, default=16, help="nº de alunos (apenas S1)")
    ap.add_argument("--policy", default="auction", choices=["auction", "first_come", "priority", "compare"])
    ap.add_argument("--pricing", default=None, choices=["first", "uniform"])
    ap.add_argument("--trace", default=None, help="caminho do trace JSONL")
    ap.add_argument("--no-event", action="store_true", help="S0 sem o evento de professor indisponível")
    args = ap.parse_args(argv)

    sc = build(args.scenario, args.seed, args.students, 0 if args.no_event else 44)
    print(f"# {sc.name}: {sc.description}  (semente={args.seed})")

    if args.policy == "compare":
        res = compare_policies(sc, args.seed, args.pricing)
        keys = ["turmas_abertas", "ocupacao_vagas", "U_medio", "pct_satisfatoria", "gini_U",
                "U_medio_baixa_prioridade", "U_medio_alta_prioridade"]
        print(f"{'métrica':28s}" + "".join(f"{p:>13s}" for p in res))
        for k in keys:
            print(f"{k:28s}" + "".join(f"{res[p][k]:>13}" for p in res))
        bad = [v for r in res.values() for v in r["invariantes_violadas"]]
        print("invariantes:", "OK" if not bad else bad)
        return 0 if not bad else 1

    sim = Simulation(sc, args.seed, pricing=args.pricing).run()
    reg = sim.registrar
    if args.policy != "auction":
        reg = run_baseline(sc, args.policy, args.seed, opened_snapshot(reg))
    if args.trace and args.policy == "auction":
        sim.trace.dump(args.trace)
        print(f"trace: {args.trace} ({len(sim.trace.records)} registros, sha256={sim.trace.digest()[:16]})")

    print("\nTurmas:")
    for sid in sorted(reg.sections):
        s = reg.sections[sid]
        print(f"  {sid:8s} {s.status:9s} prof={s.prof} sala={s.room} vagas={len(s.roster)}/{s.capacity} {sorted(s.roster)}")
    print("\nAlunos:")
    for sid, r in student_results(reg, sc).items():
        print(f"  {sid:6s} U={r['U']:.2f} (R={r['R']:.2f} S={r['S']:.2f} E={r['E']:.2f}) "
              f"{'satisfatória' if r['satisfatoria'] else 'insatisfatória'}  turmas={r['sections']} pontos={r['points_left']}")
    summary = summarize(reg, sc, sim.trace if args.policy == "auction" else None)
    print("\nResumo:", json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not summary["invariantes_violadas"] else 1


if __name__ == "__main__":
    sys.exit(main())
