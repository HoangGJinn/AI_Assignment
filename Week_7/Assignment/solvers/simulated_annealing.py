# Simulated Annealing algorithm for N-Queens
import copy, math, random
from .common import N, is_valid_solution, heuristic_cost

def simulated_annealing_trace(x, T0=100, alpha=0.95, Tmin=1e-3, restarts=300):
    """
    Simulated Annealing cho N-Queens với multi-restart.
    """
    best_path, best_steps = [], []
    found = False
    best_attempt = -1

    for attempt in range(1, restarts + 1):   # đếm lượt restart
        board = [[0 for _ in range(N)] for _ in range(N)]
        cols = [random.randint(0, N-1) for _ in range(N)]
        for r, c in enumerate(cols):
            board[r][c] = 1

        path = [(r, c) for r, c in enumerate(cols)]
        step_costs = []
        T = T0

        while T > Tmin:
            row = random.randint(0, N-1)
            old_col = cols[row]
            new_col = random.randint(0, N-1)
            while new_col == old_col:
                new_col = random.randint(0, N-1)

            new_board = copy.deepcopy(board)
            new_board[row][old_col] = 0
            new_board[row][new_col] = 1

            h_old = heuristic_cost(board)
            h_new = heuristic_cost(new_board)
            delta = h_old - h_new

            if delta >= 0:
                prob, accept = 1.0, True
            else:
                prob = math.exp(delta / T)
                accept = random.random() < prob

            step_costs.append((delta, T, prob, accept, attempt))  # thêm attempt vào log

            if accept:
                board = new_board
                cols[row] = new_col
                path = [(r, c) for r, c in enumerate(cols)]

                if h_new == 0 and is_valid_solution(board, x):
                    print(f"Thành công ở restart {attempt}")
                    return path, step_costs, True, attempt

            T *= alpha

        if len(path) > len(best_path):   # lưu best nếu chưa có solution
            best_path, best_steps = path, step_costs
            best_attempt = attempt

    print(f"Không tìm thấy nghiệm. Best ở restart {best_attempt}")
    return best_path, best_steps, False, best_attempt
