import json
from puzzle_8 import Puzzle8    
from puzzle_solver import PuzzleSolver
import heuristics as h

def print_board(board):
    for i in range(0, 9, 3):
        print(" ".join(str(x) if x != 0 else "_" for x in board[i:i+3]))

def main():
    cases = {
        "1": {
            "nome": "Fácil",
            "start": [1, 2, 3,
                      4, 0, 6,
                      7, 5, 8]
        },
        "2": {
            "nome": "Médio",
            "start": [1, 0, 3,
                      5, 2, 6,
                      4, 7, 8]
        },
        "3": {
            "nome": "Difícil",
            "start": [8, 6, 7,
                      2, 5, 4,
                      3, 0, 1]  
        }
    }

    goal = [1, 2, 3,
            4, 5, 6,
            7, 8, 0]

    print("Selecione o nível de dificuldade:")
    for k, v in cases.items():
        print(f"{k} - {v['nome']}")
        print()
        print_board(v["start"])
        print()
    choice = input("Opção: ").strip()

    if choice not in cases:
        print("Opção inválida!")
        return

    start = cases[choice]["start"]
    level_name = cases[choice]["nome"].lower()
    print(f"Executando caso {cases[choice]['nome']}...")

    solver = PuzzleSolver(start, goal, Puzzle8)

    algorithms = {
        "UCS": solver.uniform_cost_search,
        "A*_admissivel_simples": lambda: solver.a_star_search(lambda s: h.misplaced_tiles(s, goal)),
        "A*_admissivel_avancada": lambda: solver.a_star_search(lambda s: h.manhattan_distance(s, goal)),
        "A*_admissivel_avancada_2x": lambda: solver.a_star_search(lambda s: h.manhattan_distance_linear_conflict(s, goal)),
        "A*_nao_admissivel": lambda: solver.a_star_search(lambda s: h.non_admissible(s, goal)),
    }

    results = {}
    for name, algo in algorithms.items():
        print(f"Executando {name}...")
        solution_state = algo()
        if solution_state:
            path = solution_state.get_path()
            metrics = {
                "caminho": path,
                "tamanho_caminho": len(path),
                "nodos_visitados": solver.nodes_visited,
                "tempo_execucao_s": round(solver.execution_time,5),
                "maior_tamanho_fronteira": solver.max_frontier_size,
            }
            results[name] = metrics
            print(f"Solução {name}: {metrics['caminho']}")
        else:
            results[name] = {"erro": "Nenhuma solução encontrada"}

    with open(f"../resultados-{level_name}.json", "w") as f:
        json.dump(results, f, indent=2)
        
if __name__ == "__main__":
    main()
