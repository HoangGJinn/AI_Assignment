# BFS (Breadth-First Search) algorithm for N-Queens
from queue import Queue
import copy
from .common import N, isValid, is_valid_solution

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
