# Common functions for N-Queens algorithms
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

def f_cost(i, j, board):
    return cost_estimate(i, j) + heuristic_cost(board)
