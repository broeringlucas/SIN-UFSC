"""MatriculaUFSC - Figura 3: sequência nominal do protocolo seat_auction.

Gera 03_sequencia_seat_auction.png e .svg na mesma pasta do script.
Uso: python 03_sequencia_seat_auction.py
Para editar: altere LIFELINES e MESSAGES abaixo e rode novamente.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

for name in ("Carlito", "DejaVu Sans"):
    if any(f.name == name for f in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = name
        break

LIFELINES = ["Departamento", "Aluno A (BDI)", "Aluno B (BDI)", "Registrar"]

# (origem, destino, texto, estilo)   estilo: "msg" | "self"
MESSAGES = [
    (0, 1, "cfp(T, k=1, reply_by)", "msg"),
    (0, 2, "cfp(T, k=1, reply_by)", "msg"),
    (1, 0, "propose(lance=40)", "msg"),
    (2, 0, "propose(lance=55)", "msg"),
    (0, 0, "fecha a janela; ordena os lances", "self"),
    (0, 3, "request(validar aluno B em T)", "msg"),
    (3, 0, "inform(ok: pré-req., horário, carga)", "msg"),
    (0, 2, "accept-proposal", "msg"),
    (0, 1, "reject-proposal", "msg"),
    (3, 2, "inform(matriculado)", "msg"),
]

BLUE, GRAY = "#1f4e79", "#44546a"


def main() -> None:
    n = len(LIFELINES)
    step = 0.25
    top = 0.45
    height = top + step * (len(MESSAGES) + 1) + 0.25
    fig = plt.figure(figsize=(6.0, height))
    ax = fig.add_axes([0, 0, 1, 1])  # 1 unidade de dados = 1 polegada
    xs = [i * 1.5 for i in range(n)]
    ax.set_xlim(-0.7, 6.0 - 0.7)
    ax.set_ylim(-(height - top - 0.05), top + 0.05)
    ax.axis("off")

    for x, name in zip(xs, LIFELINES):
        ax.text(x, top - 0.08, name, ha="center", va="center", fontsize=9, color=BLUE,
                bbox=dict(boxstyle="round,pad=0.3", fc="#eaf1f8", ec=BLUE, lw=1))
        ax.plot([x, x], [top - 0.28, -(len(MESSAGES)) * step - 0.17], ls=(0, (3, 3)), color="#9aa5b1", lw=0.8)

    shift = 0.0  # espaço extra depois de uma auto-mensagem
    for i, (a, b, text, kind) in enumerate(MESSAGES, start=1):
        y = -i * step + 0.08 - shift
        if kind == "self":
            x = xs[a]
            ax.annotate("", xy=(x, y - 0.14), xytext=(x, y + 0.02),
                        arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1,
                                        connectionstyle="arc3,rad=-1.6", shrinkA=0, shrinkB=0))
            ax.text(x + 0.3, y - 0.06, f"{i}. {text}", ha="left", va="center", fontsize=8.5, color=GRAY, style="italic")
            shift += 0.12
            continue
        x0, x1 = xs[a], xs[b]
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.1, shrinkA=0, shrinkB=0))
        ax.text((x0 + x1) / 2, y + 0.05, f"{i}. {text}", ha="center", va="bottom", fontsize=8.5, color="#222")

    out = Path(__file__).resolve().parent
    fig.savefig(out / "03_sequencia_seat_auction.png", dpi=200, bbox_inches="tight")
    fig.savefig(out / "03_sequencia_seat_auction.svg", bbox_inches="tight")


if __name__ == "__main__":
    main()
