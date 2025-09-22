import tkinter as tk
import time

from solvers.algorithms import (
    N,
    bfs_trace, dfs_trace, ucs_trace,
    dls_trace, ids_trace_dls, ids_trace_dfs_with_limit,
    greedy_trace, a_star_trace,
    hill_climbing_trace, simulated_annealing_trace,
    genetic_trace, beam_trace,
    cost_estimate, heuristic_cost, f_cost,
    isValid, is_valid_solution
)

from twelve_queen_solutions import list_solutions
# ==================================

#Nguyen Hoang Giap - 23110096


N = 8
LIGHT = "#f0d9b5"
DARK = "#b58863"
SQ = 50
board_size = N * SQ
margin = 20
W = board_size + margin * 2
H = board_size + margin * 2

root = tk.Tk()
after_id = None
root.title("8 Queens")

# ===== GUI setup =====
left = tk.Frame(root, bg="#ECE7E7", width=450, height=700)
right = tk.Frame(root, bg="#ECE7E7", width=450, height=700)
panel_detail = tk.Frame(root, bg="#ECE7E7", width=450, height=500 + 200)
left.pack(side="left")
right.pack(side="left")
panel_detail.pack(side="left")

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

log_box = tk.Listbox(panel_detail, font=("Consolas", 11), height=25, width=50)
log_box.pack(fill="both", expand=True, padx=2, pady=(0, 10))


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
    font = ("Segoe UI Symbol", 35)
    x0, y0 = margin, margin
    for (r, c) in positions:
        xc = x0 + c * SQ + SQ / 2
        yc = y0 + r * SQ + SQ / 2
        canvas.create_text(xc, yc, text=symbol, font=font, tags=("queen",))

def get_target_solution(x):
    board = list_solutions[x]
    return [(r, board[r].index(1)) for r in range(8)]


            
def animate_path(type):
    """Nhận vào lựa chọn là bfs, dfs, ucs, dls, ids,.."""
    clear_boards()
    step_label.config(text="")
    if 'log_box' in globals():
        log_box.delete(0, tk.END)

    global after_id
    if after_id:
        root.after_cancel(after_id)
        after_id = None

    # ======= BIẾN MẶC ĐỊNH AN TOÀN =======
    total_cost = None
    limit = None
    step_costs = []    # cho a_star/hill_climbing/simulated_annealing
    found = None       # cho simulated_annealing/genetic
    attempt = None     # cho simulated_annealing
    gen = None         # cho genetic
    evo_log = []       # log tiến hoá cho genetic

    # ======= CHỌN THUẬT TOÁN =======
    if type == "bfs":
        update_right_board(1); root.update(); time.sleep(1)
        path = bfs_trace(1)

    elif type == "dfs":
        update_right_board(2); root.update(); time.sleep(1)
        path = dfs_trace(2)

    elif type == "dls":
        update_right_board(3); root.update(); time.sleep(1)
        empty_board = [[0 for _ in range(8)] for _ in range(8)]
        path = dls_trace(empty_board, 0, [], 8, 3)

    elif type == "ids_dls":
        update_right_board(4); root.update(); time.sleep(1)
        path, limit = ids_trace_dls(4)

    elif type == "ids_dfs":
        update_right_board(5); root.update(); time.sleep(1)
        path, limit = ids_trace_dfs_with_limit(5)

    elif type == "greedy":
        update_right_board(6); root.update(); time.sleep(1)
        path = greedy_trace(6)

    elif type == "a_star":
        update_right_board(8); root.update(); time.sleep(1)
        path, step_costs = a_star_trace(8)

    elif type == "hill_climbing":
        update_right_board(3); root.update(); time.sleep(1)
        path, step_costs = hill_climbing_trace(3)

    elif type == "simulated_annealing":
        update_right_board(10); root.update(); time.sleep(1)
        path, step_costs, found, attempt = simulated_annealing_trace(10)

    elif type == "genetic":
        update_right_board(11); root.update(); time.sleep(1)
        try:
            path, gen, found, evo_log = genetic_trace(11)
        except Exception:
            path, gen, found = genetic_trace(11)
    elif type == "beam":
        update_right_board(0); root.update(); time.sleep(1)
        path = beam_trace(0)

    else:  # ucs
        update_right_board(7); root.update(); time.sleep(1)
        path, total_cost = ucs_trace(7)

    if not isinstance(path, list):
        step_label.config(text=f"Kết quả: {path}")
        return

    # ======= LOG RIÊNG CHO GENETIC =======
    if type == "genetic" and evo_log and 'log_box' in globals():
        log_box.insert(tk.END, "== GENETIC: tiến trình (mỗi ~10 thế hệ) ==")
        for g, fit, conf, match in evo_log:
            log_box.insert(tk.END, f"Gen {g}: best_fit={fit:.2f} | cost={conf} | match={match}/8")
        log_box.yview_moveto(1.0)

    # ======= ANIMATE ĐẶT QUÂN =======
    def step(i):
        if i > len(path):
            moves_str = " -> ".join([f"({r+1},{c+1})" for r, c in path])

            # Xác định thành công theo từng thuật toán
            success = (len(path) == N)
            if type in ("simulated_annealing", "genetic") and (found is not None):
                success = bool(found)

            if not success:
                msg = f"Không tìm thấy nghiệm với {type.upper()} (local minimum).\nĐường đi sinh ra: {moves_str}"
            else:
                msg = f"Đường đi: {moves_str}"
                if total_cost is not None:
                    msg += f" | Tổng chi phí: {total_cost}"
                if type in ("ids_dls", "ids_dfs") and (limit is not None):
                    msg += f" | Limit: {limit}"
                if type == "genetic" and (gen is not None):
                    if found:
                        msg += f" | Tìm thấy ở thế hệ {gen}"
                    else:
                        msg += f" | Không tìm thấy sau {gen} thế hệ"
                if (type == "simulated_annealing") and (attempt is not None) and found:
                    msg += f" | Tìm thấy ở lần restart: {attempt}"

            step_label.config(text=msg)
            return

        # Vẽ từng bước
        draw_Board(canvasLeft)
        draw_queens(canvasLeft, path[:i])

        moves_str = " -> ".join([f"({r+1},{c+1})" for r, c in path[:i]])
        step_label.config(text=f"Đường đi hiện tại: {moves_str}")

        # Log theo từng bước
        if 'log_box' in globals():
            r, c = path[i-1]
            if type == "simulated_annealing" and i-1 < len(step_costs):
                delta, T, prob, accept, _ = step_costs[i-1]
                log_box.insert(tk.END,
                    f"Đặt quân {i}: ({r+1}, {c+1}) | ΔE={delta}, T={T:.2f}, prob={prob:.4f}, accept={accept}"
                )
            elif type in ("a_star", "hill_climbing") and i-1 < len(step_costs):
                val = step_costs[i-1]
                if type == "a_star" and isinstance(val, (tuple, list)) and len(val) == 3:
                    g_i, h_i, f_i = val
                    log_box.insert(tk.END,
                        f"Đặt quân {i}: ({r+1}, {c+1}) | g={g_i}, h={h_i}, f={f_i}"
                    )
                else:
                    log_box.insert(tk.END,
                        f"Đặt quân {i}: ({r+1}, {c+1}) | cost={val}"
                    )
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
    ("A Star", "a_star"),
    ("Hill Climbing", "hill_climbing"),
    ("Simulated Annealing", "simulated_annealing"),
    ("Genetic", "genetic"),
    ("Beam (K=3)", "beam")
]

for idx, (label, alg) in enumerate(buttons):
    r, c = divmod(idx, 4)
    btn = tk.Button(
        row_controls_left,
        text=label,
        font=("Segoe UI", 10),
        width=12,                
        height=1,              
        command=lambda alg=alg: animate_path(alg)
    )
    btn.grid(row=r, column=c, padx=3, pady=3, ipadx=2, ipady=1)



def update_right_board(x):
    draw_queens(canvasRight, get_target_solution(x))


root.mainloop()
