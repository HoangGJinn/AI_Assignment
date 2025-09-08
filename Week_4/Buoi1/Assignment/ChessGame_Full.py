import tkinter as tk
#ta cung co the sai deque
from collections import deque
from queue import Queue
import copy
from twelve_queen_solutions import list_solutions
import heapq
from itertools import count

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
left = tk.Frame(root, bg="#ECE7E7", width=W + 100, height=H + 200)
right = tk.Frame(root, bg="#ECE7E7", width=W + 100, height=H + 200)
left.pack(side="left")
right.pack(side="right")
left.pack_propagate(False)
right.pack_propagate(False)

labelLeft = tk.Label(left, text="Bàn cờ ban đầu", font=("Segoe", 12), bg="#D99090")
labelRight = tk.Label(right, text="Chọn bàn cờ đích", font=("Segoe", 12), bg="#D99090")
labelLeft.pack(pady=(10, 4))
labelRight.pack(pady=(10, 4))

canvasLeft = tk.Canvas(left, width=W, height=H, bg="lightblue")
canvasRight = tk.Canvas(right, width=W, height=H, bg="lightblue")
canvasLeft.pack(pady=10, side="top")
canvasRight.pack(pady=10, side="top")

step_label = tk.Label(left, text="", font=("Segoe", 11), bg="#5BDE92")
step_label.pack(pady=(5, 3))

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

def get_target_solution():
    x = int(solution_spinbox.get()) - 1
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
    while q:
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

def animate_path(type):
    '''Nhận vào lựa chọn là bfs, dfs, hay ucs'''
    x = int(solution_spinbox.get()) - 1
    total_cost = None

    if type == "bfs":
        path = bfs_trace(x)
    elif type == "dfs":
        path = dfs_trace(x)
    else:  # ucs
        path, total_cost = ucs_trace(x)

    def step(i):
        if i > len(path):
            # Khi xong, nếu có tổng chi phí (UCS) thì báo thêm
            if total_cost is not None:
                step_label.config(text=step_label.cget("text") + f" | Tổng chi phí: {total_cost}")
            return
        draw_Board(canvasLeft)
        draw_queens(canvasLeft, path[:i])
        row, col = path[i - 1]
        if total_cost is not None:
            step_label.config(text=f"Bước {i}/{len(path)}: đặt tại ({row+1}, {col+1}) | Chi phí: {cost_estimate(row, col)}")
        else:
            step_label.config(text=f"Bước {i}/{len(path)}: đặt tại ({row+1}, {col+1})")
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

# Draw initial boards
draw_Board(canvasLeft)
draw_Board(canvasRight)


panel = tk.Frame(right, bg="#ECE7E7")
panel.pack(pady=8)

tk.Label(panel, text="Chọn bàn cờ mẫu:", font=("Segoe", 10), bg="#ECE7E7").pack()
solution_spinbox = tk.Spinbox(panel, from_=1, to=12, width=5, font=("Segoe", 12), justify="center")
solution_spinbox.pack(pady=4)

# Tạo frame con để chứa cả nút và thanh scale
row_controls = tk.Frame(left, bg="#ECE7E7")
row_controls.pack(pady=8)


run_button1 = tk.Button(row_controls, text="Chạy BFS", font=("Segoe", 11),
                        command=lambda: animate_path("bfs"))
run_button1.pack(side="left", padx=5)

run_button2 = tk.Button(row_controls, text="Chạy DFS", font=("Segoe", 11),
                        command=lambda: animate_path("dfs"))
run_button2.pack(side="left", padx=5)

run_button3 = tk.Button(row_controls, text="Chạy UCS", font=("Segoe", 11),
                        command=lambda: animate_path("ucs"))
run_button3.pack(side="left", padx=5)


delay_var = tk.IntVar(value=800)
scale_delay = tk.Scale(row_controls, from_=100, to=2000, variable=delay_var,
                       orient="horizontal", label="Tốc độ (ms)", length=200)
scale_delay.pack(side="left", padx=5)

clear_button = tk.Button(row_controls, text="🗑 Xóa bàn cờ", font=("Segoe", 11), command=clear_boards)
clear_button.pack(side="left", padx=5)


def update_right_board():
    draw_queens(canvasRight, get_target_solution())

update_right_board()
solution_spinbox.config(command=update_right_board)

root.mainloop()
