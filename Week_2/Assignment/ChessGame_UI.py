import tkinter as tk

N = 8
LIGHT = "#f0d9b5"
DARK  = "#b58863"

root = tk.Tk()
root.title("Chess")
SQ = 60
board_size = N*SQ
margin = 20

W = board_size + margin*2
H = board_size + margin*2

def draw_Board(canvas):
    x0, y0 = margin, margin
    for r in range(N):
        for c in range(N):
            x1 = x0 + c*SQ
            y1 = y0 + r*SQ
            x2 = x1 + SQ
            y2 = y1 + SQ
            color = LIGHT if (r+c) % 2 == 0 else DARK
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)
            
    offset = 12  # khoảng cách chữ với bàn cờ

    # nhãn cột A-H
    for c in range(N):
        label = chr(ord("A") + c)
        xc = x0 + c*SQ + SQ/2
        canvas.create_text(xc, y0 - offset, text=label, font=("Segoe UI", 12))
        canvas.create_text(xc, y0 + board_size + offset, text=label, font=("Segoe UI", 12))

    # nhãn hàng 8-1
    for r in range(N):
        label = 8 - r
        yc = y0 + r*SQ + SQ/2
        canvas.create_text(x0 - offset, yc, text=label, font=("Segoe UI", 12))
        canvas.create_text(x0 + board_size + offset, yc, text=label, font=("Segoe UI", 12))

def draw_queens(canvas, positions, symbol="♛"):
    canvas.delete("queen")
    font = ("Segoe UI Symbol", 42)
    x0, y0 = margin, margin
    for (r, c) in positions:
        xc = x0 + c*SQ + SQ/2
        yc = y0 + r*SQ + SQ/2
        canvas.create_text(xc, yc, text=symbol, font=font, tags=("queen",))
        
left = tk.Frame(root, bg="#ECE7E7", width=W+100, height=H+200)
right = tk.Frame(root, bg="#ECE7E7", width=W+100, height=H+200)

left.pack(side="left")
right.pack(side="right")

left.pack_propagate(False)
right.pack_propagate(False)


canvasLeft  = tk.Canvas(left, width=W, height=H, bg="lightblue")
canvasRight = tk.Canvas(right, width=W, height=H, bg="lightblue")
canvasLeft.pack(pady=30, side="top")
canvasRight.pack(pady=30, side="top")

labelLeft  = tk.Label(left,  text="Bàn cờ ban đầu", font=("Segoe", 12), bg="#D99090")
labelRight = tk.Label(right, text="Bàn cờ lúc sau",  font=("Segoe", 12), bg="#D99090")
labelLeft.pack(pady=0, side="top")
labelRight.pack(pady=0, side="top")

draw_Board(canvasLeft)
draw_Board(canvasRight)

panel = tk.Frame(right, bg="#ECE7E7")
panel.pack(pady=8)
tk.Label(panel, text="Move Queens (0->7)", font=("Segoe", 10), bg="#ECE7E7").grid(row=0, column=0, columnspan=8, pady=(0,4))

col_vars = [tk.IntVar(value=v) for v in [0, 4, 7, 5, 2, 6, 1, 3]]
spins = []
#variable class: StringVar, IntVar, DoubleVar, BooleanVar
#giá trị ở trong spinbox thay đổi thì trong mảng cũng thay đổi do sử dụng IntVar
for r in range(8):
    sb = tk.Spinbox(panel, from_=0, to=7, width=3, textvariable=col_vars[r], font=("Segoe", 10), justify="center")
    sb.grid(row=1, column=r, padx=2)
    spins.append(sb)

cols_label = tk.Label(panel, text="", font=("Consolas", 10), bg="#ECE7E7")
cols_label.grid(row=2, column=0, columnspan=8, pady=(6,0))

def current_positions():
    return [(r, col_vars[r].get()) for r in range(8)]

def refresh_cols_label():
    arr = [v.get() for v in col_vars]
    cols_label.configure(text=f"cols = {arr}")
    
def on_col_change(*_):
    draw_queens(canvasRight, current_positions(), symbol="♛")
    refresh_cols_label()

for v in col_vars:
    v.trace_add("write", on_col_change)

on_col_change()

root.mainloop()
