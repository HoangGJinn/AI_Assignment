# DLS (Depth-Limited Search) and IDS (Iterative Deepening Search) algorithms for N-Queens
from collections import deque
import copy
from .common import N, isValid, is_valid_solution

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
