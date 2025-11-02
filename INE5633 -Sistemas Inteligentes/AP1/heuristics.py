def misplaced_tiles(state, goal):
    return sum(1 for i, tile in enumerate(state.board) if tile != 0 and tile != goal[i])

def manhattan_distance(state, goal):
    distance = 0
    for i, tile in enumerate(state.board):
        if tile != 0:
            goal_index = goal.index(tile)
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(goal_index, 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def non_admissible(state, goal):
    return 2 * manhattan_distance(state, goal)

def manhattan_distance_linear_conflict(state, goal):
    distance = 0
    conflicts = 0
    board = state.board

    distance = manhattan_distance(state, goal)
    
    for row in range(3):
        tiles_in_row = [board[row*3 + col] for col in range(3)]
        for i in range(3):
            for j in range(i+1, 3):
                t1 = tiles_in_row[i]
                t2 = tiles_in_row[j]
                if t1 != 0 and t2 != 0:
                    g1_row, g1_col = divmod(goal.index(t1), 3)
                    g2_row, g2_col = divmod(goal.index(t2), 3)
                    if g1_row == row == g2_row and g1_col > g2_col:
                        conflicts += 1

    for col in range(3):
        tiles_in_col = [board[row*3 + col] for row in range(3)]
        for i in range(3):
            for j in range(i+1, 3):
                t1 = tiles_in_col[i]
                t2 = tiles_in_col[j]
                if t1 != 0 and t2 != 0:
                    g1_row, g1_col = divmod(goal.index(t1), 3)
                    g2_row, g2_col = divmod(goal.index(t2), 3)
                    if g1_col == col == g2_col and g1_row > g2_row:
                        conflicts += 1

    return distance + 2 * conflicts

