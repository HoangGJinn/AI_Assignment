# AC3 (Arc Consistency 3) algorithm for N-Queens problem
from collections import deque
from .common import N, is_valid_solution

# Tạo domain cho mỗi biến (hàng).
# Mỗi biến đại diện cho một hàng và có thể nhận giá trị từ 0 đến N-1 (cột).
def create_domains():
    return [list(range(N)) for _ in range(N)]

# Tạo danh sách các ràng buộc (arcs) giữa các biến.
# Mỗi arc (i, j) đại diện cho ràng buộc giữa hàng i và hàng j.
def create_constraints():
    constraints = []
    for i in range(N):
        for j in range(N):
            if i != j:
                constraints.append((i, j))
    return constraints

def is_consistent(row1, col1, row2, col2):
    # Cùng cột
    if col1 == col2:
        return False
    
    # Cùng đường chéo chính
    if abs(row1 - row2) == abs(col1 - col2):
        return False
    
    return True

def revise(domains, xi, xj):
    """
    Hàm REVISE trong thuật toán AC3.
    Loại bỏ các giá trị từ domain của xi không nhất quán với bất kỳ giá trị nào trong domain của xj.
    """
    revised = False
    to_remove = []
    
    for value_i in domains[xi]:
        # Kiểm tra xem có tồn tại giá trị nào trong domain của xj
        # mà nhất quán với value_i không
        found_consistent = False
        for value_j in domains[xj]:
            if is_consistent(xi, value_i, xj, value_j):
                found_consistent = True
                break
        
        # Nếu không tìm thấy giá trị nhất quán, loại bỏ value_i
        if not found_consistent:
            to_remove.append(value_i)
            revised = True
    
    # Loại bỏ các giá trị không nhất quán
    for value in to_remove:
        domains[xi].remove(value)
    
    return revised

def ac3(domains, constraints):
    """
    Returns:
        True nếu CSP nhất quán, False nếu không có nghiệm
    """
    queue = deque(constraints)
    
    while queue:
        xi, xj = queue.popleft()
        
        if revise(domains, xi, xj):
            # Nếu domain của xi trống, không có nghiệm
            if not domains[xi]:
                return False
            
            # Thêm tất cả các arc (xk, xi) vào queue với xk != xi, xj
            for xk in range(N):
                if xk != xi and xk != xj:
                    queue.append((xk, xi))
    
    return True

# Kết hợp AC3 và backtracking.
# Trước tiên áp dụng AC3 để giảm domain, sau đó dùng backtracking để tìm nghiệm.
def solve_with_ac3_and_backtrack():
    domains = create_domains()
    constraints = create_constraints()
    
    # Áp dụng AC3 để giảm domain
    if not ac3(domains, constraints):
        return None, []  # Không có nghiệm
    
    # Sử dụng backtracking với domain đã giảm
    assignment = [-1] * N  # -1 nghĩa là chưa gán
    events = []
    
    def backtrack(row):
        if row == N:
            return True
        
        for col in domains[row]:
            # Kiểm tra xem có thể gán hậu vào (row, col) không
            valid = True
            for prev_row in range(row):
                if assignment[prev_row] != -1:
                    if not is_consistent(prev_row, assignment[prev_row], row, col):
                        valid = False
                        break
            
            if valid:
                assignment[row] = col
                events.append(("place", row, col))
                
                if backtrack(row + 1):
                    return True
                
                assignment[row] = -1
                events.append(("remove", row, col))
        
        return False
    
    if backtrack(0):
        return assignment, events
    else:
        return None, events
    
# Hàm trace cho AC3 + Backtracking
def ac3_trace(target_idx=0):
    assignment, events = solve_with_ac3_and_backtrack()
    
    if assignment:
        # Chuyển đổi assignment thành format tương thích
        path = [(row, col) for row, col in enumerate(assignment)]
        return path
    else:
        return []

# Hàm trả về events cho việc hiển thị animation.
def ac3_events(target_idx=0):
    assignment, events = solve_with_ac3_and_backtrack()
    
    if assignment:
        events.append(("solution", [(row, col) for row, col in enumerate(assignment)]))
    # return list
    return events
