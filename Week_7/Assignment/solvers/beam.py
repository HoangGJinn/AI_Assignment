# Beam Search algorithm for N-Queens
import heapq
from itertools import count
import copy
from .common import N, is_valid_solution, heuristic_cost

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
