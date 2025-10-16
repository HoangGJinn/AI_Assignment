# DFS (Depth-First Search) algorithm for N-Queens
from collections import deque
import copy
from .common import N, isValid, is_valid_solution

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
