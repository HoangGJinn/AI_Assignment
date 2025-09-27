# solvers/nqueens.py
from collections import deque
from queue import Queue
from itertools import count
import heapq, copy, math, random, time

from twelve_queen_solutions import list_solutions

N = 8

def isValid(board, row, col):
    for i in range(row):
        if board[i][col] == 1:
            return False
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1
    i, j = row - 1, col + 1
    while i >= 0 and j < N:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1
    return True

def cost_estimate(i, j):
    if i == 0 or i == 7 or j == 0 or j == 7:
        return 22
    if i == 1 or i == 6 or j == 1 or j == 6:
        return 24
    if i == 2 or i == 5 or j == 2 or j == 5:
        return 26
    if i == 3 or i == 4 or j == 3 or j == 4:
        return 28
    return 0

def is_valid_solution(board, x):
    return board == list_solutions[x]

def bfs_trace(x):
    q = Queue()
    empty_board = [[0 for _ in range(N)] for _ in range(N)]
    q.put((empty_board, 0, []))
    while not q.empty():
        board, row, path = q.get()
        if row == N:
            if is_valid_solution(board, x):
                return path
        for col in range(N):
            if isValid(board, row, col):
                new_board = copy.deepcopy(board)
                new_board[row][col] = 1
                new_path = path + [(row, col)]
                q.put((new_board, row + 1, new_path))
    return []

def dfs_trace(x):
    q = deque()
    empty_board = [[0 for _ in range(N)] for _ in range(N)]
    q.append((empty_board, 0, []))
    while q:
        board, row, path = q.pop()
        if row == N:
            if is_valid_solution(board, x):
                return path
        for col in range(N):
            if isValid(board, row, col):
                new_board = copy.deepcopy(board)
                new_board[row][col] = 1
                new_path = path + [(row, col)]
                q.append((new_board, row + 1, new_path))
    return []

def ucs_trace(x):
    """
    UCS: mỗi trạng thái là (board, row, path, cost)
    """
    empty_board = [[0 for _ in range(N)] for _ in range(N)]
    # heap item: (cost, row, tie, board, path)
    pq = []
    tie = count()
    heapq.heappush(pq, (0, 0, next(tie), empty_board, []))
    
    while pq:
        cost, row, _, board, path = heapq.heappop(pq)
        if row == N:
            if is_valid_solution(board, x):
                return path, cost
            continue

        for col in range(N):
            if isValid(board, row, col):
                new_board = copy.deepcopy(board)
                new_board[row][col] = 1
                new_path = path + [(row, col)]
                new_cost = cost + cost_estimate(row, col)
                heapq.heappush(pq, (new_cost, row + 1, next(tie), new_board, new_path))
    return [], 0

#depth-limited search
def dls_trace(board, row, path, limit, x):
    if row == N:
        if is_valid_solution(board, x):
            return path
        else:
            return "failure"
    elif limit == 0:
        return "cutoff"
    else:
        cutoff_occcurred = False
        for col in range(N):
            if isValid(board, row, col):
                new_board = copy.deepcopy(board)
                new_board[row][col] = 1
                new_path = path + [(row, col)]
                result = dls_trace(new_board, row+1, new_path, limit-1, x)
                if result == "cutoff":
                    cutoff_occcurred = True
                elif result != "failure":
                    return result
        return "cutoff" if cutoff_occcurred else "failure"
    
#iterative deeping search base on dls
def ids_trace_dls(x):
    for lim in range(0,N+1):
        empty_board = [[0 for _ in range(8)] for _ in range(8)]
        result = dls_trace(empty_board, 0, [], lim, x)
        if result != "cutoff" and result != "failure":
            return result, lim

def dfs_with_limit(x, limit):
    q = deque()
    empty_board = [[0 for _ in range(N)] for _ in range(N)]
    q.append((empty_board, 0, [], limit))
    cutoff_occurred = False

    while q:
        board, row, path, lim = q.pop()

        if row == N:
            if is_valid_solution(board, x):
                return path
            else:
                continue
        elif lim == 0:
            cutoff_occurred = True
            continue

        for col in range(N):
            if isValid(board, row, col):
                new_board = copy.deepcopy(board)
                new_board[row][col] = 1
                new_path = path + [(row, col)]
                q.append((new_board, row + 1, new_path, lim-1))
                
    if cutoff_occurred:
        return "cutoff"
    else:
        return "failure"
    
def ids_trace_dfs_with_limit(x):
    for lim in range(0, N+1):
        result = dfs_with_limit(x, lim)
        if result != "cutoff" and result != "failure":
            return result, lim

def heuristic_cost(board):
    conflict = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1:
                # cột xuống
                for r in range(i+1, N):
                    if board[r][j] == 1:
                        conflict += 1
                # chéo xuống phải
                rr, cc = i+1, j+1
                while rr < N and cc < N:
                    if board[rr][cc] == 1:
                        conflict += 1
                    rr += 1; cc += 1
                # chéo xuống trái
                rr, cc = i+1, j-1
                while rr < N and cc >= 0:
                    if board[rr][cc] == 1:
                        conflict += 1
                    rr += 1; cc -= 1
    return conflict

#f_cost for a* algorithm
def f_cost(i, j, board):
    return cost_estimate(i, j) + heuristic_cost(board)
    
def greedy_trace(x):
    pq = []
    tie = count()
    empty_board = [[0 for _ in range(N)] for _ in range(N)]
    # (heuristic, row, board, path)
    h0 = heuristic_cost(empty_board)
    heapq.heappush(pq, (h0, 0, next(tie), empty_board, []))

    while pq:
        h, row, _, board, path = heapq.heappop(pq)
        if row == N:
            if is_valid_solution(board, x):
                return path
            else:
                continue
        for col in range(N):
            new_board = copy.deepcopy(board)
            new_board[row][col] = 1
            newpath = path + [(row, col)]
            
            hc = heuristic_cost(new_board)
            heapq.heappush(pq, (hc, row+1, next(tie), new_board, newpath))
    return []


def a_star_trace(x):
    pq = []
    tie = count()
    empty_board = [[0 for _ in range(N)] for _ in range(N)]
    # (f, row, board, path, costs)
    g0 = 0
    h0 = heuristic_cost(empty_board)
    f0 = g0 + h0
    heapq.heappush(pq, (f0, 0, next(tie), empty_board, [], []))

    while pq:
        f, row, _, board, path, costs = heapq.heappop(pq)
        if row == N:
            if is_valid_solution(board, x):
                return path, costs
            else:
                continue
        for col in range(N):
            if isValid(board, row, col):
                new_board = copy.deepcopy(board)
                new_board[row][col] = 1
                newpath = path + [(row, col)]
                
                step_cost = cost_estimate(row, col)
                fc = f_cost(row, col, new_board) + step_cost
                newcosts = costs + [fc]

                heapq.heappush(
                    pq,
                    (fc, row+1, next(tie), new_board, newpath, newcosts)
                )
    return [], []

def hill_climbing_trace(x):
    tie = count()
    empty_board = [[0 for _ in range(N)] for _ in range(N)]
    # (h, row, count, board, path, costs)
    h0 = heuristic_cost(empty_board)
    pq = [(h0, 0, next(tie), empty_board, [], [])]

    prev_h_cost = 20
    while pq:
        h, row, _, board, path, costs = heapq.heappop(pq)
        pq.clear()  # reset để chỉ giữ trạng thái tốt nhất

        if row == N:
            if is_valid_solution(board, x):
                return path, costs
            else:
                continue

        improved = False
        for col in range(N):
            if isValid(board, row, col):
                new_board = copy.deepcopy(board)
                new_board[row][col] = 1

                newpath = path + [(row, col)]
                h_new = heuristic_cost(new_board)
                newcosts = costs + [h_new]

                heapq.heappush(pq, (h_new, row+1, next(tie), new_board, newpath, newcosts))
                if h_new < prev_h_cost:
                    improved = True

        if not improved:
            return path, costs

        prev_h_cost = h  # cập nhật theo trạng thái hiện tại

    return [], []

#Thuật toán luyện kim
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

# ================= GENETIC ALGORITHM (with evolution log) =================

def _cols_to_board(cols):
    board = [[0]*N for _ in range(N)]
    for r, c in enumerate(cols):
        board[r][c] = 1
    return board

def _target_cols(x):
    b = list_solutions[x]
    return [row.index(1) for row in b]

def _matches_to_target(cols, target_cols):
    return sum(1 for a, b in zip(cols, target_cols) if a == b)

def _fitness(cols, target_cols):
    board = _cols_to_board(cols)
    conflicts = heuristic_cost(board)         # 0 là tốt nhất
    max_conflicts = 28                        # C(8,2)
    match_bonus = 2 * _matches_to_target(cols, target_cols)
    return 1e-6 + (max_conflicts - conflicts) + match_bonus

def _roulette_select(pop, fits):
    s = sum(fits)
    r = random.random() * s
    acc = 0.0
    for ind, f in zip(pop, fits):
        acc += f
        if acc >= r:
            return ind
    return pop[-1]

def _reproduce(x, y):
    n = len(x)
    c = random.randint(1, n-1)
    return x[:c] + y[c:]

def _mutate(child, p=0.08):
    if random.random() < p:
        i = random.randrange(N)
        new_c = random.randrange(N)
        while new_c == child[i]:
            new_c = random.randrange(N)
        child[i] = new_c
    return child

def genetic_trace(x, pop_size=60, mutation_rate=0.08, max_gens=2000, keep_log=True):
    """
    Trả về: (path, gen, found, evo_log)
    - evo_log: [(gen, best_fit, conflicts, matches), ...] (thưa để log gọn)
    """
    target = _target_cols(x)
    population = [[random.randrange(N) for _ in range(N)] for _ in range(pop_size)]

    best_ind = None
    best_fit = -1.0
    evo_log = []

    for gen in range(1, max_gens + 1):
        fits = [_fitness(ind, target) for ind in population]

        # cập nhật best
        for ind, f in zip(population, fits):
            if f > best_fit:
                best_fit = f
                best_ind = ind[:]

        # log thưa (mỗi 10 thế hệ + thế hệ 1 + khi tìm thấy)
        if keep_log and (gen == 1 or gen % 10 == 0):
            bb = _cols_to_board(best_ind)
            evo_log.append((gen, best_fit, heuristic_cost(bb), _matches_to_target(best_ind, target)))


        if is_valid_solution(_cols_to_board(best_ind), x):
            if keep_log:
                bb = _cols_to_board(best_ind)
                evo_log.append((gen, best_fit, heuristic_cost(bb), _matches_to_target(best_ind, target)))
            path = [(r, c) for r, c in enumerate(best_ind)]
            return path, gen, True, evo_log


        new_population = []
        for _ in range(pop_size):
            xp = _roulette_select(population, fits)
            yp = _roulette_select(population, fits)
            child = _reproduce(xp, yp)
            child = _mutate(child, mutation_rate)
            new_population.append(child)
        population = new_population

    # hết max_gens
    path = [(r, c) for r, c in enumerate(best_ind)]
    return path, max_gens, False, evo_log

def beam_trace(x, K=3):
    tie = count()
    empty_board = [[0]*N for _ in range(N)]
    h0 = heuristic_cost(empty_board)
    pq = []
    heapq.heappush(pq, (h0, 0, next(tie), empty_board, []))
    
    while pq:
        h, row, _, board, path = heapq.heappop(pq)
        
        if row == N:
            if is_valid_solution(board, x):
                return path
            continue
        
        beam = []
        for col in range(N):
            new_board = copy.deepcopy(board)
            new_board[row][col] = 1
            
            newpath = path + [(row, col)]
            h_new = heuristic_cost(new_board)
            heapq.heappush(beam, (h_new, row+1, next(tie), new_board, newpath))
        
        if not beam:
            continue
    
        next_pq = []
        for _ in range(min(K, len(beam))):
            next_pq.append(heapq.heappop(beam))
            
        pq = next_pq
        heapq.heapify(pq)
    return []


#tim kiem trong moi truong khong xác định
def and_or_search(x):
    def or_search(board, row):
        if row == N:
            return {"Goal": is_valid_solution(board, x), "plan": []}

        for col in range(N):
            if isValid(board, row, col):
                new_board = copy.deepcopy(board)
                new_board[row][col] = 1
                success, child_plan = and_search([new_board], row + 1)
                if success:
                    return {"Goal": True, "plan": [(row, col), child_plan]}

        return {"Goal": False, "plan": []}

    def and_search(list_boards, row):
        results = []
        for b in list_boards:
            child = or_search(b, row)
            if not child["Goal"]:
                return False, {"Goal": False}
            results.append(child)
        return True, {"Goal": True, "children": results}

    empty_board = [[0 for _ in range(N)] for _ in range(N)]
    return or_search(empty_board, 0)


def print_plan(plan, indent=0):
    space = "  " * indent
    if not plan:
        print(space + "None")
        return

    if plan.get("Goal") is False:
        print(space + "Fail")
        return

    if "plan" in plan and plan["plan"]:
        move, child = plan["plan"]
        print(space + f"OR: đặt hậu tại {move}")
        print_plan(child, indent + 0.5)

    if "children" in plan:
        print(space + "AND:")
        for idx, child in enumerate(plan["children"]):
            print(space + f"  Nhánh {idx+1}:")
            print_plan(child, indent + 1)


def extract_path(plan):
    """
    Lấy path [(row, col), ...] từ cây kế hoạch and_or_search.
    """
    path = []
    current = plan
    while current and current.get("Goal"):
        if "plan" in current and isinstance(current["plan"], (list, tuple)) and len(current["plan"]) == 2:
            move, child = current["plan"]
            path.append(move)
            current = child
        elif "children" in current and current["children"]:
            current = current["children"][0]
        else:
            break
    print(path)
    return path

#tim kiem trong moi truong khong nhin thay
def _belief_actions(belief, row):
    cols = set()
    for idx in belief:
        board = list_solutions[idx]
        c = board[row].index(1) 
        cols.add(c)
    return sorted(cols)

def _belief_result(belief, row, col):
    return [idx for idx in belief if list_solutions[idx][row][col] == 1]

def _belief_goal(row, belief):
    return row == N and len(belief) > 0

def belief_state_search(initial_belief=None):
    if initial_belief is None:
        belief0 = list(range(len(list_solutions)))  # [0..11]
    else:
        belief0 = initial_belief[:]

    logs = []

    def dfs(row, belief):
        if _belief_goal(row, belief):
            return True, [], belief

        if row >= N or not belief:
            return False, [], belief

        for col in _belief_actions(belief, row):
            new_belief = _belief_result(belief, row, col)
            # log: (row, col, before, after)
            logs.append((row, col, belief[:], new_belief[:]))

            ok, subpath, final_bel = dfs(row + 1, new_belief)
            if ok:
                return True, [(row, col)] + subpath, final_bel

        return False, [], belief

    ok, path, final_belief = dfs(0, belief0)
    return (path if ok else [], final_belief if ok else [], logs)

def print_belief_logs(logs):
    """In logs ra console cho dễ debug."""
    for (row, col, before, after) in logs:
        print(f"Row {row}: chọn cột {col} | Belief {before} -> {after}")

def belief_pretty(plan_path, final_belief):
    """Tạo chuỗi tóm tắt: đường đi + lời giải cuối (nếu còn)."""
    moves = " -> ".join([f"({r+1},{c+1})" for (r,c) in plan_path]) if plan_path else "<rỗng>"
    fb = ", ".join(map(str, final_belief)) if final_belief else "<rỗng>"
    return f"Đường đi (Belief-State): {moves}\nBelief cuối: [{fb}]"












            


            

