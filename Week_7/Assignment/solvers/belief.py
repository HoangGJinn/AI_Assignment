# Belief-State Search algorithm for N-Queens
from twelve_queen_solutions import list_solutions
from .common import N
import random

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


# PARTIAL OBSERVABLE BELIEF-STATE SEARCH 
# gợi ý 2 quân cờ

def _get_random_hints(target_solution_idx, num_hints=2):
    """
    Tạo gợi ý ngẫu nhiên về vị trí của num_hints quân cờ từ solution đích.
    """
    if target_solution_idx >= len(list_solutions):
        return []
    
    board = list_solutions[target_solution_idx]
    positions = [(r, board[r].index(1)) for r in range(N)]
    
    # Chọn ngẫu nhiên num_hints vị trí
    return random.sample(positions, min(num_hints, len(positions)))

def _filter_belief_with_hints(belief, hints):
    """
    Lọc belief state dựa trên các gợi ý đã cho.
    """
    filtered = []
    for idx in belief:
        board = list_solutions[idx]
        valid = True
        for (hint_row, hint_col) in hints:
            if board[hint_row][hint_col] != 1:
                valid = False
                break
        if valid:
            filtered.append(idx)
    return filtered

def _partial_belief_actions(belief, row, known_positions):

    # Nếu vị trí của row này đã biết, chỉ trả về cột đó
    if row in known_positions:
        return [known_positions[row]]
    
    # Ngược lại, tìm tất cả các cột khả thi từ belief
    cols = set()
    for idx in belief:
        board = list_solutions[idx]
        c = board[row].index(1)
        cols.add(c)
    return sorted(cols)

def partial_observable_belief_search(target_solution_idx=0, num_hints=2):
    """
    Belief-state search với khả năng quan sát một phần (có gợi ý).
    Returns:
        Tuple (path, final_belief, logs, hints_used)
    """
    # Khởi tạo belief ban đầu với tất cả solutions
    belief0 = list(range(len(list_solutions)))
    
    # Tạo gợi ý ngẫu nhiên từ solution đích
    hints = _get_random_hints(target_solution_idx, num_hints)
    known_positions = {row: col for (row, col) in hints}
    
    # Lọc belief ban đầu dựa trên gợi ý
    initial_filtered_belief = _filter_belief_with_hints(belief0, hints)
    
    logs = []
    
    def dfs(row, belief):
        if _belief_goal(row, belief):
            return True, [], belief
        
        if row >= N or not belief:
            return False, [], belief
        
        for col in _partial_belief_actions(belief, row, known_positions):
            new_belief = _belief_result(belief, row, col)
            
            # Thêm thông tin về việc sử dụng gợi ý
            hint_used = row in known_positions
            logs.append((row, col, belief[:], new_belief[:], hint_used))
            
            ok, subpath, final_bel = dfs(row + 1, new_belief)
            if ok:
                return True, [(row, col)] + subpath, final_bel
        
        return False, [], belief
    
    ok, path, final_belief = dfs(0, initial_filtered_belief)
    
    return (
        path if ok else [], 
        final_belief if ok else [], 
        logs,
        hints
    )

def print_partial_belief_logs(logs, hints):
    """In logs cho partial observable belief search."""
    print("=== PARTIAL OBSERVABLE BELIEF-STATE SEARCH ===")
    print(f"Gợi ý ban đầu: {[(r+1, c+1) for (r, c) in hints]}")
    print("=" * 45)
    
    for (row, col, before, after, hint_used) in logs:
        hint_str = " [GỢI Ý]" if hint_used else ""
        print(f"Row {row+1}: chọn cột {col+1}{hint_str}")
        print(f"   Belief: [{len(before)} solutions] -> [{len(after)} solutions]")
        if len(after) <= 3:
            print(f"   Solutions còn lại: {after}")

def partial_belief_pretty(plan_path, final_belief, hints):
    """Tạo chuỗi tóm tắt cho partial observable belief search."""
    moves = " -> ".join([f"({r+1},{c+1})" for (r,c) in plan_path]) if plan_path else "<rỗng>"
    fb = ", ".join(map(str, final_belief)) if final_belief else "<rỗng>"
    hints_str = ", ".join([f"({r+1},{c+1})" for (r,c) in hints])
    
    return f"Đường đi (Partial Belief): {moves}\nGợi ý: [{hints_str}]\nBelief cuối: [{fb}]"
