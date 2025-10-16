# Greedy and A* algorithms for N-Queens
import heapq
from itertools import count
import copy
from .common import N, isValid, is_valid_solution, heuristic_cost, cost_estimate, f_cost

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
