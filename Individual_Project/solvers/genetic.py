# Genetic Algorithm for N-Queens
import random
from .common import N, is_valid_solution, heuristic_cost
from twelve_queen_solutions import list_solutions

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
