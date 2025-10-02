# Backtracking and Forward-Backtracking algorithms for N-Queens
from .common import N, isValid, is_valid_solution

# fast solution
def events_to_path(events):
    for ev in events:
        if ev[0] == "solution":
            return list(ev[1])
    return []

# --- backtracking nhanh (classic)
def backtracking_trace(target_idx):
    return events_to_path(backtracking(target_idx))

# --- forward-backtracking nhanh
def forward_backtracking_trace(target_idx):
    return events_to_path(forward_backtracking_events(target_idx))

def backtracking(x):
    board = [[0]*N for _ in range(N)]
    stack = []
    events = []
    found = False

    def dfs(row):
        nonlocal found
        if found:
            return
        if row == N:
            if is_valid_solution(board, x):
                events.append(("solution", stack.copy()))
                found = True
            return

        for col in range(N):
            if isValid(board, row, col):
                # đặt
                board[row][col] = 1
                stack.append((row, col))
                events.append(("place", row, col))

                dfs(row + 1)
                if found:
                    return

                # backtrack (gỡ)
                events.append(("remove", row, col))
                stack.pop()
                board[row][col] = 0

    dfs(0)
    return events

# ===== Forward-Backtracking (đặt là đánh dấu ngay các ô bị khống chế) =====

EMPTY, BLOCKED, QUEEN = 0, 1, 2

def _mark_attacks(board, r, c):
    """
    Đánh dấu tất cả ô bị khống chế bởi hậu (r,c) thành 1 nếu đang là 0.
    Trả về danh sách các ô đã đổi để hoàn tác khi backtrack.
    """
    Nn = len(board)
    changed = []

    # hàng
    for j in range(Nn):
        if j != c and board[r][j] == EMPTY:
            board[r][j] = BLOCKED
            changed.append((r, j))

    # cột
    for i in range(Nn):
        if i != r and board[i][c] == EMPTY:
            board[i][c] = BLOCKED
            changed.append((i, c))

    # chéo chính
    i, j = r - 1, c - 1
    while i >= 0 and j >= 0:
        if board[i][j] == EMPTY:
            board[i][j] = BLOCKED
            changed.append((i, j))
        i -= 1; j -= 1

    i, j = r + 1, c + 1
    while i < Nn and j < Nn:
        if board[i][j] == EMPTY:
            board[i][j] = BLOCKED
            changed.append((i, j))
        i += 1; j += 1

    # chéo phụ
    i, j = r - 1, c + 1
    while i >= 0 and j < Nn:
        if board[i][j] == EMPTY:
            board[i][j] = BLOCKED
            changed.append((i, j))
        i -= 1; j += 1

    i, j = r + 1, c - 1
    while i < Nn and j >= 0:
        if board[i][j] == EMPTY:
            board[i][j] = BLOCKED
            changed.append((i, j))
        i += 1; j -= 1

    return changed

def _unmark(board, changed):
    """Hoàn tác các ô đã đánh dấu (trả về 0)."""
    for i, j in changed:
        board[i][j] = EMPTY

def _board_from_path(path):
    """Dựng bảng 0/1 từ path để tái dùng is_valid_solution(board, x)."""
    B = [[0]*N for _ in range(N)]
    for r, c in path:
        B[r][c] = 1
    return B

def forward_backtracking_events(target_idx):
    board = [[EMPTY]*N for _ in range(N)]
    path = []
    events = []
    found = False

    def dfs(row):
        nonlocal found
        if found:
            return
        if row == N:
            if is_valid_solution(_board_from_path(path), target_idx):
                events.append(("solution", path.copy()))
                found = True
            return

        for col in range(N):
            if board[row][col] != BLOCKED and board[row][col] != QUEEN:
                # đặt hậu
                board[row][col] = QUEEN
                path.append((row, col))
                events.append(("place", row, col))

                # đánh dấu các ô bị khống chế
                changed = _mark_attacks(board, row, col)

                dfs(row + 1)
                if found:
                    return

                # backtrack: gỡ đánh dấu và gỡ hậu
                _unmark(board, changed)
                events.append(("remove", row, col))
                path.pop()
                board[row][col] = EMPTY

    dfs(0)
    return events
