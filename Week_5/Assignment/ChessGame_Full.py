import tkinter as tk
#ta cung co the sai deque
from collections import deque
from queue import Queue
import copy
from twelve_queen_solutions import list_solutions
import heapq
from itertools import count
import time

#Nguyen Hoang Giap - 23110096

N = 8
LIGHT = "#f0d9b5"
DARK = "#b58863"
SQ = 60
board_size = N * SQ
margin = 20
W = board_size + margin * 2
H = board_size + margin * 2

root = tk.Tk()
after_id = None
root.title("8 Queens")

# ===== GUI setup =====
left = tk.Frame(root, bg="#ECE7E7", width=W, height=H + 150)
right = tk.Frame(root, bg="#ECE7E7", width=W, height=H + 150)
panel_detail = tk.Frame(root, bg="#ECE7E7", width=W/1.5, height=H + 150)
left.pack(side="left")
right.pack(side="left")
panel_detail.pack(side="right")

left.pack_propagate(False)
right.pack_propagate(False)
panel_detail.pack_propagate(False)

labelLeft = tk.Label(left, text="Bàn cờ ban đầu", font=("Segoe", 12), bg="#D99090")
labelRight = tk.Label(right, text="Chọn bàn cờ đích", font=("Segoe", 12), bg="#D99090")
labelLeft.pack(pady=(10, 4))
labelRight.pack(pady=(10, 4))

canvasLeft = tk.Canvas(left, width=W, height=H, bg="lightblue")
canvasRight = tk.Canvas(right, width=W, height=H, bg="lightblue")
canvasLeft.pack(pady=10, side="top")
canvasRight.pack(pady=10, side="top")

# ==== STEP ====
step_label = tk.Label(
    panel_detail,
    text="",
    font=("Segoe", 11),
    bg="#5BDE92",
    justify="left",
    anchor="w",
    wraplength=int(W/1.5) - 30,
    padx=8, pady=6
)

title_detail = tk.Label(panel_detail, text="Thông tin bước / Kết quả", font=("Segoe", 12, "bold"), bg="#ECE7E7")
title_detail.pack(anchor="w", padx=10, pady=(10, 4))
step_label.pack(side="top", fill="x", padx=10, pady=(0, 8))

log_label = tk.Label(panel_detail, text="Log đặt quân", font=("Segoe", 12, "bold"), bg="#ECE7E7")
log_label.pack(anchor="w", padx=10, pady=(10, 4))

log_box = tk.Listbox(panel_detail, font=("Consolas", 11), height=10, width=40)
log_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))


def draw_Board(canvas):
    x0, y0 = margin, margin
    for r in range(N):
        for c in range(N):
            x1 = x0 + c * SQ
            y1 = y0 + r * SQ
            x2 = x1 + SQ
            y2 = y1 + SQ
            color = LIGHT if (r + c) % 2 == 0 else DARK
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

    offset = 12  # khoảng cách chữ với bàn cờ

    # nhãn cột A-H
    for c in range(N):
        label = chr(ord("A") + c)
        xc = x0 + c * SQ + SQ / 2
        canvas.create_text(xc, y0 - offset, text=label, font=("Segoe UI", 12))
        canvas.create_text(xc, y0 + board_size + offset, text=label, font=("Segoe UI", 12))

    # nhãn hàng 8-1
    for r in range(N):
        label = 8 - r
        yc = y0 + r * SQ + SQ / 2
        canvas.create_text(x0 - offset, yc, text=label, font=("Segoe UI", 12))
        canvas.create_text(x0 + board_size + offset, yc, text=label, font=("Segoe UI", 12))

def draw_queens(canvas, positions, symbol="♛"):
    canvas.delete("queen")
    font = ("Segoe UI Symbol", 42)
    x0, y0 = margin, margin
    for (r, c) in positions:
        xc = x0 + c * SQ + SQ / 2
        yc = y0 + r * SQ + SQ / 2
        canvas.create_text(xc, yc, text=symbol, font=font, tags=("queen",))

def get_target_solution(x):
    board = list_solutions[x]
    return [(r, board[r].index(1)) for r in range(8)]

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

#f_cost for a* algorithm
def f_cost(i, j, board):
    return cost_estimate(i, j) + heuristic_cost(board)
    
def greedy_trace(x):
    pq = []
    tie = count()
    empty_board = [[0 for _ in range(N)] for _ in range(N)]
    # (heuristic, row, board, path, costs)
    heapq.heappush(pq, (heuristic_cost(empty_board), 0, next(tie), empty_board, [], []))

    while pq:
        h, row, _, board, path, costs = heapq.heappop(pq)
        if row == N:
            if is_valid_solution(board, x):
                return path, costs
            else:
                continue
        for col in range(N):
            if isValid(board, row, col):
                new_board = copy.deepcopy(board)
                new_board[row][col] = 1
                newpath = path + [(row, col)]
                step_cost = cost_estimate(row, col)
                newcosts = costs + [step_cost]
                hc = heuristic_cost(new_board)
                heapq.heappush(pq, (hc, row+1, next(tie), new_board, newpath, newcosts))
    return [], []


def a_star_trace(x):
    pq = []
    tie = count()
    empty_board = [[0 for _ in range(N)] for _ in range(N)]
    # (f, row, board, path, costs)
    heapq.heappush(pq, (0, 0, next(tie), empty_board, [], []))

    while pq:
        f, row, _, board, path, costs = heapq.heappop(pq)
        if row == N:
            if is_valid_solution(board, x):
                return path, costs
            else:
                continue
        for col in range(N):
            if isValid(board, row, col):
                new_board = copy.deepcopy(board)
                new_board[row][col] = 1
                newpath = path + [(row, col)]
                step_cost = cost_estimate(row, col)
                newcosts = costs + [step_cost]

                fc = f_cost(row, col, new_board)

                heapq.heappush(
                    pq,
                    (fc, row+1, next(tie), new_board, newpath, newcosts)
                )
    return [], []



def animate_path(type):
    """Nhận vào lựa chọn là bfs, dfs, ucs, dls, ids,.."""
    # reset trạng thái hiển thị
    step_label.config(text="")
    if 'log_box' in globals():
        log_box.delete(0, tk.END)

    global after_id
    if after_id:
        root.after_cancel(after_id)
        after_id = None

    total_cost = None
    limit = None

    if type == "bfs":
        update_right_board(1); root.update(); time.sleep(2)
        path = bfs_trace(1)
    elif type == "dfs":
        update_right_board(2); root.update(); time.sleep(2)
        path = dfs_trace(2)
    elif type == "dls":
        update_right_board(3); root.update(); time.sleep(2)
        empty_board = [[0 for _ in range(8)] for _ in range(8)]
        path = dls_trace(empty_board, 0, [], 8, 3)
    elif type == "ids_dls":
        update_right_board(4); root.update(); time.sleep(2)
        path, limit = ids_trace_dls(4)
    elif type == "ids_dfs":
        update_right_board(5); root.update(); time.sleep(2)
        path, limit = ids_trace_dfs_with_limit(5)
    elif type == "greedy":
        update_right_board(6); root.update(); time.sleep(2)
        path, step_costs = greedy_trace(6)
    elif type == "a_star":
        update_right_board(8); root.update(); time.sleep(2)
        path, step_costs = a_star_trace(8)
    else:  # ucs
        update_right_board(7); root.update(); time.sleep(2)
        path, total_cost = ucs_trace(7)

    if not isinstance(path, list):
        step_label.config(text=f"Kết quả: {path}")
        return

    def step(i):
        if i > len(path):
            moves_str = " -> ".join([f"({r+1},{c+1})" for r, c in path])
            msg = f"Đường đi: {moves_str}"
            if total_cost is not None: msg += f" | Tổng chi phí: {total_cost}"
            if type in ("ids_dls", "ids_dfs"): msg += f" | Limit: {limit}"
            step_label.config(text=msg)
            return

        draw_Board(canvasLeft)
        draw_queens(canvasLeft, path[:i])

        moves_str = " -> ".join([f"({r+1},{c+1})" for r, c in path[:i]])
        step_label.config(text=f"Đường đi hiện tại: {moves_str}")

        if 'log_box' in globals():
            r, c = path[i-1]
            if type in ("greedy", "a_star") and i-1 < len(step_costs):
                log_box.insert(tk.END, f"Đặt quân {i}: ({r+1}, {c+1}) | cost = {step_costs[i-1]}")
            else:
                log_box.insert(tk.END, f"Đặt quân {i}: ({r+1}, {c+1})")
            log_box.yview_moveto(1.0)

        global after_id
        after_id = root.after(delay_var.get(), lambda: step(i + 1))

    step(1)

    
def clear_boards():
    global after_id
    if after_id:
        root.after_cancel(after_id)
        after_id = None

    canvasLeft.delete("queen")
    draw_Board(canvasLeft)
    step_label.config(text="")
    log_box.delete(0, tk.END)


# Draw initial boards
draw_Board(canvasLeft)
draw_Board(canvasRight)

# Frame_right
row_controls_right = tk.Frame(right, bg="#ECE7E7")
row_controls_right.pack(pady=8)

delay_var = tk.IntVar(value=800)
scale_delay = tk.Scale(row_controls_right, from_=100, to=2000, variable=delay_var,
                       orient="horizontal", label="Tốc độ (ms)", length=200)
scale_delay.pack(side="left", padx=5)

clear_button = tk.Button(row_controls_right, text="🗑 Xóa bàn cờ", font=("Segoe", 11), command=clear_boards)
clear_button.pack(side="left", padx=5)

# Frame_left
row_controls_left = tk.Frame(left, bg="#ECE7E7")
row_controls_left.pack(pady=8)

buttons = [
    ("BFS", "bfs"),
    ("DFS", "dfs"),
    ("UCS", "ucs"),
    ("DLS", "dls"),
    ("IDS(with DLS)", "ids_dls"),
    ("IDS(with DFS)", "ids_dfs"),
    ("Greedy", "greedy"),
    ("A Star", "a_star")
]

for idx, (label, alg) in enumerate(buttons):
    r, c = divmod(idx, 4)  # 4 nút mỗi hàng
    btn = tk.Button(row_controls_left, text=label, font=("Segoe", 11),
                    command=lambda alg=alg: animate_path(alg))
    btn.grid(row=r, column=c, padx=5, pady=5)



def update_right_board(x):
    draw_queens(canvasRight, get_target_solution(x))


root.mainloop()
