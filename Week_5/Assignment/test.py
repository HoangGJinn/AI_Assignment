import tkinter as tk
from collections import deque
import time

# ===== Cấu hình =====
N = 8
LIGHT = "#f0d9b5"
DARK  = "#b58863"
SQ = 60
MARGIN = 20
BOARD = N * SQ
W = BOARD + MARGIN*2
H = BOARD + MARGIN*2

root = tk.Tk()
root.title("8 Queens — BFS/DFS (toàn bàn cờ) + Xem từng bước nghiệm")

# ===== GUI =====
left = tk.Frame(root, bg="#ECE7E7")
left.pack(padx=8, pady=8)

canvas = tk.Canvas(left, width=W, height=H, bg="lightblue")
canvas.grid(row=0, column=0, rowspan=8, padx=(0,12))

tk.Label(left, text="Kết quả", bg="#ECE7E7", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="w")
lbl_status = tk.Label(left, text="", bg="#ECE7E7", font=("Segoe UI", 10), justify="left", wraplength=360)
lbl_status.grid(row=1, column=1, sticky="w", pady=(0,8))

# cụm nút tìm nghiệm
btn_bfs = tk.Button(left, text="🔎 Tìm bằng BFS", font=("Segoe UI", 11))
btn_dfs = tk.Button(left, text="🔎 Tìm bằng DFS", font=("Segoe UI", 11))
btn_bfs.grid(row=2, column=1, sticky="w", pady=2)
btn_dfs.grid(row=3, column=1, sticky="w", pady=2)

# cụm điều khiển xem bước
ctrl = tk.LabelFrame(left, text="Xem từng bước nghiệm", bg="#ECE7E7", font=("Segoe UI", 9, "bold"))
ctrl.grid(row=4, column=1, sticky="we", pady=6)

delay_var = tk.IntVar(value=300)
tk.Label(ctrl, text="Tốc độ (ms):", bg="#ECE7E7", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")
tk.Scale(ctrl, from_=0, to=1000, variable=delay_var, orient="horizontal", length=180).grid(row=0, column=1, padx=6)

btn_play  = tk.Button(ctrl, text="▶ Play",  font=("Segoe UI", 10))
btn_pause = tk.Button(ctrl, text="⏸ Pause", font=("Segoe UI", 10))
btn_prev  = tk.Button(ctrl, text="⏮ Prev",  font=("Segoe UI", 10))
btn_next  = tk.Button(ctrl, text="⏭ Next",  font=("Segoe UI", 10))
btn_reset = tk.Button(ctrl, text="⟲ Reset", font=("Segoe UI", 10))
btn_prev.grid(row=1, column=0, sticky="w", pady=4)
btn_next.grid(row=1, column=1, sticky="w", pady=4)
btn_play.grid(row=2, column=0, sticky="w")
btn_pause.grid(row=2, column=1, sticky="w")
btn_reset.grid(row=3, column=0, sticky="w", pady=(4,2))

btn_clear = tk.Button(left, text="🗑 Clear", font=("Segoe UI", 10))
btn_clear.grid(row=5, column=1, sticky="w", pady=6)

# ===== Vẽ bàn cờ / quân =====
def draw_board():
    canvas.delete("all")
    x0, y0 = MARGIN, MARGIN
    for r in range(N):
        for c in range(N):
            x1 = x0 + c*SQ
            y1 = y0 + r*SQ
            x2 = x1 + SQ
            y2 = y1 + SQ
            color = LIGHT if (r+c) % 2 == 0 else DARK
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)
    # nhãn
    off = 12
    for c in range(N):
        label = chr(ord("A")+c)
        xc = x0 + c*SQ + SQ/2
        canvas.create_text(xc, y0 - off, text=label, font=("Segoe UI", 11))
        canvas.create_text(xc, y0 + BOARD + off, text=label, font=("Segoe UI", 11))
    for r in range(N):
        label = 8 - r
        yc = y0 + r*SQ + SQ/2
        canvas.create_text(MARGIN - off, yc, text=label, font=("Segoe UI", 11))
        canvas.create_text(MARGIN + BOARD + off, yc, text=label, font=("Segoe UI", 11))

def draw_queens_prefix(path, k):
    """Vẽ k nước đầu của nghiệm: k-1 quân xanh, quân thứ k màu cam."""
    canvas.delete("queen")
    x0, y0 = MARGIN, MARGIN
    for i in range(min(k, len(path))):
        r, c = path[i]
        xc = x0 + c*SQ + SQ/2
        yc = y0 + r*SQ + SQ/2
        color = "orange" if i == k-1 else "darkgreen"
        canvas.create_text(xc, yc, text="♛", font=("Segoe UI Symbol", 42),
                           tags=("queen",), fill=color)

draw_board()

# ===== Solver (toàn bàn cờ) bằng bitmask =====
# Mỗi state: (start_idx, rowsMask, colsMask, d1Mask, d2Mask, path)
# - start_idx: chỉ xét các ô có chỉ số >= start_idx để tránh hoán vị cùng một tập ô
# - rowsMask/colsMask/d1/d2 đảm bảo không ăn nhau theo hàng/cột/chéo
# Mục tiêu: đặt đủ 8 quân (len(path) == N)

def bfs_solve_anywhere():
    """BFS trên toàn 64 ô, trả về (path, expanded, elapsed_ms)."""
    t0 = time.perf_counter()
    q = deque()
    q.append((0, 0, 0, 0, 0, []))  # start_idx, rows, cols, d1, d2, path
    expanded = 0

    while q:
        start, rows, cols, d1, d2, path = q.popleft()
        expanded += 1
        if len(path) == N:
            return path, expanded, (time.perf_counter() - t0)*1000.0

        for idx in range(start, N*N):
            r = idx // N
            c = idx % N
            b_row = 1 << r
            b_col = 1 << c
            i1 = r - c + (N - 1)
            i2 = r + c
            if (rows & b_row) or (cols & b_col) or (d1 & (1 << i1)) or (d2 & (1 << i2)):
                continue
            q.append((
                idx + 1,                 # chỉ xét các ô phía sau để tránh hoán vị
                rows | b_row,
                cols | b_col,
                d1   | (1 << i1),
                d2   | (1 << i2),
                path + [(r, c)]
            ))
    return [], expanded, (time.perf_counter() - t0)*1000.0

def dfs_solve_anywhere():
    """DFS trên toàn 64 ô, trả về (path, expanded, elapsed_ms)."""
    t0 = time.perf_counter()
    st = [(0, 0, 0, 0, 0, [])]  # start_idx, rows, cols, d1, d2, path
    expanded = 0

    while st:
        start, rows, cols, d1, d2, path = st.pop()
        expanded += 1
        if len(path) == N:
            return path, expanded, (time.perf_counter() - t0)*1000.0

        # để khác BFS, ta duyệt ô từ cuối về đầu
        for idx in range(N*N - 1, start - 1, -1):
            r = idx // N
            c = idx % N
            b_row = 1 << r
            b_col = 1 << c
            i1 = r - c + (N - 1)
            i2 = r + c
            if (rows & b_row) or (cols & b_col) or (d1 & (1 << i1)) or (d2 & (1 << i2)):
                continue
            st.append((
                idx + 1,                 # chỉ xét các ô phía sau để tránh hoán vị
                rows | b_row,
                cols | b_col,
                d1   | (1 << i1),
                d2   | (1 << i2),
                path + [(r, c)]
            ))
    return [], expanded, (time.perf_counter() - t0)*1000.0

# ===== Logic xem từng bước =====
current_path = []
algo_name = ""
play_idx = 0
after_id = None
playing = False

def set_status(msg):
    lbl_status.config(text=msg)

def cancel_after():
    global after_id
    if after_id:
        root.after_cancel(after_id)
        after_id = None

def compute(algo="bfs"):
    """Tìm nghiệm trên toàn bàn cờ và chuẩn bị xem từng bước."""
    global current_path, algo_name, play_idx, playing
    cancel_after()
    playing = False
    draw_board()

    if algo == "bfs":
        path, expanded, ms = bfs_solve_anywhere()
        algo_name = "BFS (toàn bàn cờ)"
    else:
        path, expanded, ms = dfs_solve_anywhere()
        algo_name = "DFS (toàn bàn cờ)"

    if not path:
        current_path = []
        set_status(f"[{algo_name}] Không tìm thấy nghiệm.\nMở rộng: {expanded} | Thời gian: {ms:.2f} ms")
        canvas.delete("queen")
        return

    current_path = path
    play_idx = 0
    coords = " -> ".join([f"({r+1},{c+1})" for (r,c) in current_path])
    set_status(f"[{algo_name}] Đã tìm thấy nghiệm ({len(current_path)} bước).\n"
               f"Mở rộng: {expanded} | Thời gian: {ms:.2f} ms\n"
               f"Đường đi: {coords}")
    draw_queens_prefix(current_path, 0)

def show_step(k):
    """Vẽ k nước đầu (0..len(path))."""
    global play_idx
    if not current_path:
        return
    k = max(0, min(k, len(current_path)))
    play_idx = k
    draw_queens_prefix(current_path, play_idx)
    if play_idx == 0:
        step_msg = "Chưa đặt quân"
    else:
        r, c = current_path[play_idx-1]
        step_msg = f"Bước {play_idx}/{len(current_path)}: đặt ♛ tại (r={r+1}, c={c+1})"
    base = lbl_status.cget("text").split("\nĐường đi:")[0]
    lbl_status.config(text=base + f"\n{step_msg}")

def do_play():
    """Tự động tiến bước theo tốc độ."""
    global playing, after_id
    if not current_path:
        return
    playing = True

    def tick():
        global play_idx, after_id, playing
        if not playing:
            return
        if play_idx >= len(current_path):
            show_step(play_idx)
            playing = False
            return
        show_step(play_idx + 1)
        after_id = root.after(delay_var.get(), tick)

    cancel_after()
    tick()

def do_pause():
    global playing
    playing = False
    cancel_after()

def do_prev():
    do_pause()
    show_step(play_idx - 1)

def do_next():
    do_pause()
    show_step(play_idx + 1)

def do_reset():
    do_pause()
    show_step(0)

def clear_all():
    do_pause()
    draw_board()
    canvas.delete("queen")
    current_path.clear()
    set_status("")

# ===== Gán sự kiện =====
btn_bfs.config(command=lambda: compute("bfs"))
btn_dfs.config(command=lambda: compute("dfs"))

btn_play.config(command=do_play)
btn_pause.config(command=do_pause)
btn_prev.config(command=do_prev)
btn_next.config(command=do_next)
btn_reset.config(command=do_reset)

btn_clear.config(command=clear_all)

root.mainloop()
