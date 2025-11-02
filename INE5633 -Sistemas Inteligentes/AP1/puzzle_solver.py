# solver.py
import heapq
import time

class PuzzleSolver:
    def __init__(self, start, goal, puzzle_8):
        self.start = puzzle_8(start)
        self.goal = goal
        self.nodes_visited = 0
        self.max_frontier_size = 0
        self.execution_time = 0
        self.frontier_snapshot = []
        self.explored_snapshot = []

    def uniform_cost_search(self):
        return self.a_star_search(lambda state: 0)

    def a_star_search(self, heuristic):
        start_time = time.time()
        counter = 0
        frontier = []
        g = {tuple(self.start.board): 0}
        f0 = g[tuple(self.start.board)] + heuristic(self.start)
        heapq.heappush(frontier, (f0, counter, 0, self.start))
        closed = set()

        self.max_frontier_size = len(frontier)

        while frontier:
            self.max_frontier_size = max(self.max_frontier_size, len(frontier))
            f_curr, _, g_curr, state = heapq.heappop(frontier)

            if g_curr != g.get(tuple(state.board), float('inf')):
                continue

            if state.board == self.goal:
                self.execution_time = time.time() - start_time
                self.nodes_visited = len(closed) + 1 
                self.frontier_snapshot = [item[3].board for item in frontier]
                self.explored_snapshot = list(closed) + [tuple(state.board)]
                return state

            closed.add(tuple(state.board))

            for neighbor in state.get_neighbors():
                neighbor_board_t = tuple(neighbor.board)
                tentative_g = g_curr + 1

                if neighbor_board_t in closed and tentative_g >= g.get(neighbor_board_t, float('inf')):
                    continue

                if tentative_g < g.get(neighbor_board_t, float('inf')):
                    g[neighbor_board_t] = tentative_g
                    f_neighbor = tentative_g + heuristic(neighbor)
                    counter += 1
                    heapq.heappush(frontier, (f_neighbor, counter, tentative_g, neighbor))

        self.execution_time = time.time() - start_time
        self.nodes_visited = len(closed)
        self.frontier_snapshot = [item[3].board for item in frontier]
        self.explored_snapshot = list(closed)
        return None
