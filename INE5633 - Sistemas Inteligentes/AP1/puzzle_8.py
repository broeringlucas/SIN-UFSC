class Puzzle8:
    def __init__(self, board, parent=None, move=None, depth=0, cost=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
        self.zero_index = board.index(0)

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(self.board))

    def get_path(self):
        path, state = [], self
        while state.parent is not None:
            path.append(state.move)
            state = state.parent
        return list(reversed(path))

    def get_neighbors(self):
        neighbors = []
        row, col = divmod(self.zero_index, 3)
        moves = {
            "up": (row - 1, col),
            "down": (row + 1, col),
            "left": (row, col - 1),
            "right": (row, col + 1)
        }
        for move, (r, c) in moves.items():
            if 0 <= r < 3 and 0 <= c < 3:
                new_index = r * 3 + c
                new_board = self.board[:]
                new_board[self.zero_index], new_board[new_index] = new_board[new_index], new_board[self.zero_index]
                neighbors.append(Puzzle8(new_board, self, move, self.depth + 1, self.cost + 1))
        return neighbors
