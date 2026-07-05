import heapq

def is_solvable(state):
    inversions = 0
    state_list = [tile for tile in state if tile != 0]
    for i in range(len(state_list)):
        for j in range(i + 1, len(state_list)):
            if state_list[i] > state_list[j]:
                inversions += 1
    return inversions % 2 == 0

def get_manhattan_distance(state, goal_state=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    distance = 0
    for i in range(9):
        if state[i] == 0:
            continue 
        goal_index = goal_state.index(state[i])
        curr_row, curr_col = i // 3, i % 3
        goal_row, goal_col = goal_index // 3, goal_index % 3
        distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance

def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    row, col = zero_index // 3, zero_index % 3
    moves = [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]

    for dr, dc, move_name in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            neighbors.append((tuple(new_state), move_name))
    return neighbors

def construct_path(came_from, current_state):
    path = []
    while current_state in came_from:
        parent_state, move = came_from[current_state]
        path.append((move, current_state))
        current_state = parent_state
    return path[::-1]

def print_grid(state):
    for i in range(0, 9, 3):
        print(f"{state[i]} {state[i+1]} {state[i+2]}")
    print("-" * 5)

def solve_greedy(start_state):
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    open_list = []
    came_from = {} 
    
    start_h = get_manhattan_distance(start_state)
    heapq.heappush(open_list, (start_h, start_state))
    closed_set = set()
    nodes_explored = 0

    while open_list:
        current_h, current_state = heapq.heappop(open_list)
        nodes_explored += 1

        if current_state == goal_state:
            return construct_path(came_from, current_state), nodes_explored

        closed_set.add(current_state)

        for neighbor_state, move_name in get_neighbors(current_state):
            if neighbor_state in closed_set:
                continue

            if neighbor_state not in came_from:
                came_from[neighbor_state] = (current_state, move_name)
                h_score = get_manhattan_distance(neighbor_state)
                heapq.heappush(open_list, (h_score, neighbor_state))

    return None, nodes_explored

if __name__ == "__main__":
    start_puzzle = (1, 2, 3, 4, 0, 5, 7, 8, 6)
    
    print("=== INITIAL STATE ===")
    print_grid(start_puzzle)

    if not is_solvable(start_puzzle):
        print("This puzzle configuration is unsolvable.")
    else:
        print("Executing Greedy Best-First Search...\n")
        path, explored = solve_greedy(start_puzzle)
        
        print("=== INTERMEDIATE RESULTS (STEPS) ===")
        for step, (move, state) in enumerate(path, 1):
            print(f"Step {step}: Moved Empty Space '{move}'")
            print_grid(state)
            
        print("=== FINAL OUTPUT ===")
        print(f"Goal Reached Successfully!")
        print(f"Total Nodes Explored by Algorithm: {explored}")
        print(f"Total Moves to Solve: {len(path)}")