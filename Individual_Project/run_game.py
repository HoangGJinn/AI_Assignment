import tkinter as tk
import time
from tkinter import messagebox
import os
from tkinter import Toplevel
from compare import show_compare_menu

from solvers import (
    N, isValid, is_valid_solution, cost_estimate, heuristic_cost, f_cost,
    bfs_trace, dfs_trace, ucs_trace,
    dls_trace, ids_trace_dls, ids_trace_dfs_with_limit,
    greedy_trace, a_star_trace, hill_climbing_trace, simulated_annealing_trace,
    genetic_trace, beam_trace, and_or_search, belief_state_search,
    partial_observable_belief_search,
    backtracking, backtracking_trace, forward_backtracking_events,
    forward_backtracking_trace, extract_path, print_plan,
    ac3_trace, ac3_events
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
stop_flag = False  # Biến để kiểm soát việc dừng animation
root.title("8 Queens")
DELAY_MS = 800

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

    global after_id, stop_flag
    stop_flag = False  # Reset flag khi bắt đầu animation mới
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
    
    elif type == "and_or_search":
        update_right_board(8); root.update(); time.sleep(1)
        plan = and_or_search(8)
        path = extract_path(plan)

        # In cây vào log_box
        def log_plan(node, indent=0):
            space = "  " * indent
            if not node:
                log_box.insert(tk.END, space + "None")
                return
            if node.get("Goal") is False:
                log_box.insert(tk.END, space + "Fail")
                return
            if "plan" in node and node["plan"]:
                move, child = node["plan"]
                log_box.insert(tk.END, space + f"OR: đặt hậu tại {move}")
                log_plan(child, indent + 1)
            if "children" in node and node["children"]:
                log_box.insert(tk.END, space + "AND:")
                for idx, child in enumerate(node["children"]):
                    log_box.insert(tk.END, space + f"  Nhánh {idx+1}:")
                    log_plan(child, indent + 2)
            if not node.get("plan") and not node.get("children"):
                log_box.insert(tk.END, space + "Goal reached!")


        log_box.insert(tk.END, "== AND-OR SEARCH TREE ==")
        log_plan(plan)
        log_box.insert(tk.END, "========================")
        log_box.yview_moveto(1.0)
        
    elif type == "belief":
        root.update(); time.sleep(1)
        path, final_belief, belief_logs = belief_state_search()

        if final_belief:
            update_right_board(final_belief[0])

        if 'log_box' in globals():
            log_box.insert(tk.END, "== BELIEF-STATE SEARCH ==")
            for (row, col, bef, aft) in belief_logs:
                # Dòng 1: hành động
                log_box.insert(
                    tk.END,
                    f"Row {row+1}: chọn cột {col+1}"
                )
                # Dòng 2: thu hẹp belief
                log_box.insert(
                    tk.END,
                    f"   Belief: {bef} → {aft}"
                )
            if not final_belief:
                log_box.insert(tk.END, "Kết quả: Belief rỗng (FAIL)")
            else:
                log_box.insert(tk.END, f"Belief cuối: {final_belief}")
            log_box.yview_moveto(1.0)
    
    elif type == "partial_belief":
        target_idx = 8  # Chọn solution đích để tạo gợi ý
        update_right_board(target_idx); root.update(); time.sleep(1)
        path, final_belief, belief_logs, hints = partial_observable_belief_search(target_idx, 2)

        if final_belief:
            update_right_board(final_belief[0])

        if 'log_box' in globals():
            log_box.insert(tk.END, "== PARTIAL OBSERVABLE BELIEF-STATE ==")
            log_box.insert(tk.END, f"Gợi ý ban đầu: {[(r+1, c+1) for (r, c) in hints]}")
            log_box.insert(tk.END, "=" * 35)
            
            for (row, col, bef, aft, hint_used) in belief_logs:
                hint_str = " [GỢI Ý]" if hint_used else ""
                log_box.insert(tk.END, f"Row {row+1}: chọn cột {col+1}{hint_str}")
                log_box.insert(tk.END, f"   Belief: [{len(bef)}] → [{len(aft)}] solutions")
                if len(aft) <= 3 and aft:
                    log_box.insert(tk.END, f"   Solutions: {aft}")
            
            if not final_belief:
                log_box.insert(tk.END, "Kết quả: Belief rỗng (FAIL)")
            else:
                log_box.insert(tk.END, f"Belief cuối: {final_belief}")
            log_box.yview_moveto(1.0)
    
    elif type == "backtracking":
        target_idx = 9
        update_right_board(target_idx); root.update(); time.sleep(0.5)

        events = backtracking(target_idx)
        current_path = []

        # clear & vẽ rỗng ban đầu
        draw_Board(canvasLeft)
        draw_queens(canvasLeft, current_path)
        root.update()

        for ev in events:
            # Kiểm tra flag dừng
            if stop_flag:
                step_label.config(text="⏹ Backtracking đã dừng")
                return
                
            kind = ev[0]
            if kind == "place":
                _, r, c = ev
                current_path.append((r, c))     # đặt
                draw_Board(canvasLeft)
                draw_queens(canvasLeft, current_path)
                if 'log_box' in globals():
                    log_box.insert(tk.END, f"Đặt hậu: ({r}, {c})")
                    log_box.see(tk.END)
                root.update()
                time.sleep(0.08)

            elif kind == "remove":
                _, r, c = ev
                # gỡ: phần tử cuối phải là (r,c)
                if current_path and current_path[-1] == (r, c):
                    current_path.pop()
                else:
                    # đề phòng trái thứ tự, vẫn loại phần tử (r,c) nếu có
                    try:
                        current_path.remove((r, c))
                    except ValueError:
                        pass
                draw_Board(canvasLeft)
                draw_queens(canvasLeft, current_path)
                if 'log_box' in globals():
                    log_box.insert(tk.END, f"Gỡ hậu: ({r}, {c})")
                    log_box.see(tk.END)
                root.update()
                time.sleep(0.08)

            elif kind == "solution":
                _, sol_path = ev
                # highlight kết quả cuối
                draw_Board(canvasLeft)
                draw_queens(canvasLeft, sol_path)
                moves_str = " -> ".join([f"({r+1},{c+1})" for r, c in sol_path])
                step_label.config(text=f"Tìm thấy nghiệm: {moves_str}")
                if 'log_box' in globals():
                    log_box.insert(tk.END, f"Solution: {sol_path}")
                    log_box.see(tk.END)
                root.update()

    elif type == "backtracking_fast":
        target_idx = 9
        
        update_right_board(target_idx); root.update()

        path = backtracking_trace(target_idx)

        draw_Board(canvasLeft)
        draw_queens(canvasLeft, path)
        root.update()

        # Log/label gọn
        if path:
            moves = " -> ".join([f"({r+1},{c+1})" for r, c in path])
            step_label.config(text=f"Backtracking nhanh: {moves}")
            if 'log_box' in globals():
                log_box.insert("end", f"Backtracking (nhanh) tìm thấy: {path}\n")
                log_box.see("end")
        else:
            step_label.config(text="Backtracking nhanh: không khớp nghiệm mục tiêu")
            if 'log_box' in globals():
                log_box.insert("end", "Không tìm thấy nghiệm đúng target.\n")
                log_box.see("end")

    elif type == "forward_backtracking":
        target_idx = 9
        update_right_board(target_idx); root.update()

        events = forward_backtracking_events(target_idx)
        current_path = []

        draw_Board(canvasLeft)
        draw_queens(canvasLeft, current_path)
        root.update()

        for ev in events:
            # Kiểm tra flag dừng
            if stop_flag:
                step_label.config(text="⏹ Forward-Backtracking đã dừng")
                return
                
            kind = ev[0]
            if kind == "place":
                _, r, c = ev
                current_path.append((r, c))
                draw_Board(canvasLeft)
                draw_queens(canvasLeft, current_path)
                if 'log_box' in globals():
                    log_box.insert("end", f"Đặt hậu: ({r},{c})\n"); log_box.see("end")
                root.update(); time.sleep(0.08)

            elif kind == "remove":
                _, r, c = ev
                if current_path and current_path[-1] == (r, c):
                    current_path.pop()
                else:
                    try: current_path.remove((r, c))
                    except ValueError: pass
                draw_Board(canvasLeft)
                draw_queens(canvasLeft, current_path)
                if 'log_box' in globals():
                    log_box.insert("end", f"Gỡ hậu: ({r},{c})\n"); log_box.see("end")
                root.update(); time.sleep(0.08)

            elif kind == "solution":
                _, sol = ev
                draw_Board(canvasLeft)
                draw_queens(canvasLeft, sol)
                step_label.config(text="FB: " + " -> ".join([f"({r+1},{c+1})" for r,c in sol]))
                if 'log_box' in globals():
                    log_box.insert("end", f"Solution: {sol}\n"); log_box.see("end")
                root.update()
                
    elif type == "fb_fast":  # Forward-Backtracking vẽ nhanh
        target_idx = 9
        update_right_board(target_idx); root.update()
        path = forward_backtracking_trace(target_idx)
        draw_Board(canvasLeft)
        draw_queens(canvasLeft, path)
        root.update()
        if path:
            step_label.config(text="FB nhanh: " + " -> ".join([f"({r+1},{c+1})" for r,c in path]))
        else:
            step_label.config(text="FB nhanh: không khớp nghiệm mục tiêu")

    elif type == "ac3":
        # AC3 với animation
        target_idx = 0  # AC3 tìm nghiệm bất kỳ
        update_right_board(target_idx); root.update(); time.sleep(0.5)

        events = ac3_events(target_idx)
        current_path = []

        # clear & vẽ rỗng ban đầu
        draw_Board(canvasLeft)
        draw_queens(canvasLeft, current_path)
        root.update()

        if 'log_box' in globals():
            log_box.insert(tk.END, "== AC3 + BACKTRACKING ==")
            log_box.insert(tk.END, "Áp dụng AC3 để giảm domain...")
            log_box.yview_moveto(1.0)

        for ev in events:
            # Kiểm tra flag dừng
            if stop_flag:
                step_label.config(text="⏹ AC3 đã dừng")
                return
                
            kind = ev[0]
            if kind == "place":
                _, r, c = ev
                current_path.append((r, c))     # đặt
                draw_Board(canvasLeft)
                draw_queens(canvasLeft, current_path)
                if 'log_box' in globals():
                    log_box.insert(tk.END, f"Đặt hậu: ({r}, {c})")
                    log_box.see(tk.END)
                root.update()
                time.sleep(0.08)

            elif kind == "remove":
                _, r, c = ev
                # gỡ: phần tử cuối phải là (r,c)
                if current_path and current_path[-1] == (r, c):
                    current_path.pop()
                else:
                    # đề phòng trái thứ tự, vẫn loại phần tử (r,c) nếu có
                    try:
                        current_path.remove((r, c))
                    except ValueError:
                        pass
                draw_Board(canvasLeft)
                draw_queens(canvasLeft, current_path)
                if 'log_box' in globals():
                    log_box.insert(tk.END, f"Gỡ hậu: ({r}, {c})")
                    log_box.see(tk.END)
                root.update()
                time.sleep(0.08)

            elif kind == "solution":
                _, sol_path = ev
                # highlight kết quả cuối
                draw_Board(canvasLeft)
                draw_queens(canvasLeft, sol_path)
                moves_str = " -> ".join([f"({r+1},{c+1})" for r, c in sol_path])
                step_label.config(text=f"AC3 tìm thấy nghiệm: {moves_str}")
                if 'log_box' in globals():
                    log_box.insert(tk.END, f"Solution: {sol_path}")
                    log_box.see(tk.END)
                root.update()
                return  # Kết thúc animation

    elif type == "ac3_fast":  # AC3 vẽ nhanh
        target_idx = 0  # AC3 tìm nghiệm bất kỳ
        update_right_board(target_idx); root.update()
        path = ac3_trace(target_idx)
        draw_Board(canvasLeft)
        draw_queens(canvasLeft, path)
        root.update()
        
        if path:
            moves_str = " -> ".join([f"({r+1},{c+1})" for r, c in path])
            step_label.config(text=f"AC3 (nhanh): {moves_str}")
            if 'log_box' in globals():
                log_box.insert(tk.END, "== AC3 + BACKTRACKING (NHANH) ==")
                log_box.insert(tk.END, f"AC3 tìm thấy nghiệm: {path}")
                log_box.yview_moveto(1.0)
        else:
            step_label.config(text="AC3 (nhanh): không tìm thấy nghiệm")
            if 'log_box' in globals():
                log_box.insert(tk.END, "== AC3 + BACKTRACKING (NHANH) ==")
                log_box.insert(tk.END, "Không tìm thấy nghiệm hợp lệ")
                log_box.yview_moveto(1.0)

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
        # Kiểm tra flag dừng
        if stop_flag:
            step_label.config(text="⏹ Animation đã dừng")
            return
            
        if i > len(path):
            moves_str = " -> ".join([f"({r+1},{c+1})" for r, c in path])

            # Xác định thành công theo từng thuật toán
            success = (len(path) == N)
            if type in ("simulated_annealing", "genetic") and (found is not None):
                success = bool(found)
            elif type == "and_or_search":
                success = bool(path and len(path) == N)

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
        after_id = root.after(DELAY_MS, lambda: step(i + 1))

    step(1)

    
def clear_boards():
    global after_id, stop_flag
    stop_flag = True  # Set flag để dừng animation
    if after_id:
        root.after_cancel(after_id)
        after_id = None

    canvasLeft.delete("queen")
    draw_Board(canvasLeft)
    step_label.config(text="")
    log_box.delete(0, tk.END)

def stop_animation():
    """Dừng animation hiện tại"""
    global after_id, stop_flag
    stop_flag = True
    if after_id:
        root.after_cancel(after_id)
        after_id = None
    
    step_label.config(text="⏹ Animation đã dừng")
    if 'log_box' in globals():
        log_box.insert(tk.END, "⏹ Animation đã dừng bởi người dùng")
        log_box.yview_moveto(1.0)

draw_Board(canvasLeft)
draw_Board(canvasRight)

# Frame_right
row_controls_right = tk.Frame(right, bg="#ECE7E7")
row_controls_right.pack(pady=10)


clear_button = tk.Button(row_controls_right, text="🗑 Xóa bàn cờ", font=("Segoe", 11), command=clear_boards)
clear_button.pack(side="left", padx=5)

stop_button = tk.Button(row_controls_right, text="⏹ Dừng", font=("Segoe", 11), command=stop_animation)
stop_button.pack(side="left", padx=5)


compare_button = tk.Button(row_controls_right, text="📊 So sánh", font=("Segoe", 11), command=lambda: show_compare_menu(root))
compare_button.pack(side="left", padx=5)

# Frame_left - Menu phân nhóm thuật toán
row_controls_left = tk.Frame(left, bg="#ECE7E7")
row_controls_left.pack(pady=8)

# Định nghĩa các nhóm thuật toán
algorithm_groups = {
    "Uninformed Search": [
        ("BFS", "bfs"),
        ("DFS", "dfs"),
        ("DLS", "dls"),
        ("IDS(with DLS)", "ids_dls"),
        ("IDS(with DFS)", "ids_dfs"),
    ],
    "Informed Search": [
        ("UCS", "ucs"),
        ("Greedy", "greedy"),
        ("A Star", "a_star"),

    ],
    "Local Search": [
        ("Hill Climbing", "hill_climbing"),
        ("Simulated Annealing", "simulated_annealing"),
        ("Genetic", "genetic"),
        ("Beam (K=3)", "beam"),
    ],
    "Nondetermine search": [
        ("And Or Search", "and_or_search"),
        ("Belief-State", "belief"),
        ("Partial Observable Belief", "partial_belief"),
    ],
    "Constraint Satisfaction": [
        ("Backtracking", "backtracking"),
        ("Backtracking (nhanh)", "backtracking_fast"),
        ("FB", "forward_backtracking"),
        ("FB (nhanh)", "fb_fast"),
        ("AC3 + Backtracking", "ac3"),
        ("AC3 (nhanh)", "ac3_fast"),
    ]
}

# Tạo menu dropdown cho từng nhóm
def create_group_menu(group_name, algorithms):
    def show_submenu():
        # Xóa menu cũ nếu có
        for widget in submenu_frame.winfo_children():
            widget.destroy()
        
        # Tạo tiêu đề nhóm
        title_label = tk.Label(
            submenu_frame, 
            text=f"📁 {group_name}", 
            font=("Segoe UI", 12, "bold"), 
            bg="#D99090",
            fg="white"
        )
        title_label.pack(pady=(5, 10))
        
        buttons_frame = tk.Frame(submenu_frame, bg="#ECE7E7")
        buttons_frame.pack(fill="both", expand=True, padx=10)
        
        
        num_algorithms = len(algorithms)
        if num_algorithms <= 4:
            cols = 2
        else:
            cols = 3
        
        # Tạo các nút thuật toán trong grid
        for idx, (label, alg) in enumerate(algorithms):
            row = idx // cols
            col = idx % cols
            
            btn = tk.Button(
                buttons_frame,
                text=label,
                font=("Segoe UI", 9),
                width=15,
                height=1,
                bg="#5BDE92",
                command=lambda alg=alg: animate_path(alg)
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="ew")
        
        for i in range(cols):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Back
        back_btn = tk.Button(
            submenu_frame,
            text="🔙 Quay lại",
            font=("Segoe UI", 10),
            width=20,
            height=1,
            bg="#FFB6C1",
            command=show_main_menu
        )
        back_btn.pack(pady=(10, 5), padx=10, fill="x")
    
    return show_submenu

def show_main_menu():
    # Xóa submenu
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    
    title_label = tk.Label(
        submenu_frame, 
        text="🎯 Chọn nhóm thuật toán", 
        font=("Segoe UI", 12, "bold"), 
        bg="#D99090",
        fg="white"
    )
    title_label.pack(pady=(5, 15))
    
    groups_frame = tk.Frame(submenu_frame, bg="#ECE7E7")
    groups_frame.pack(fill="both", expand=True, padx=10)
    
    # 3 col
    group_items = list(algorithm_groups.items())
    for idx, (group_name, algorithms) in enumerate(group_items):
        row = idx // 3
        col = idx % 3
        
        btn = tk.Button(
            groups_frame,
            text=f"📂 {group_name}",
            font=("Segoe UI", 9),
            width=15,
            height=2,
            bg="#87CEEB",
            command=create_group_menu(group_name, algorithms)
        )
        btn.grid(row=row, column=col, padx=3, pady=3, sticky="ew")
    
    # Cấu hình grid weights để nút tự động mở rộng
    groups_frame.grid_columnconfigure(0, weight=1)
    groups_frame.grid_columnconfigure(1, weight=1)
    groups_frame.grid_columnconfigure(2, weight=1)

# Frame chứa submenu
submenu_frame = tk.Frame(row_controls_left, bg="#ECE7E7")
submenu_frame.pack(fill="both", expand=True)

# (Bỏ thanh tốc độ)

# Hiển thị menu chính ban đầu
show_main_menu()



def update_right_board(x):
    draw_queens(canvasRight, get_target_solution(x))


root.mainloop()
