# Hill Climbing algorithm for N-Queens
import heapq
from itertools import count
import copy
from .common import N, isValid, is_valid_solution, heuristic_cost

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
