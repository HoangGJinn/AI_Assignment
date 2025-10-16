# UCS (Uniform Cost Search) algorithm for N-Queens
import heapq
from itertools import count
import copy
from .common import N, isValid, is_valid_solution, cost_estimate

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
