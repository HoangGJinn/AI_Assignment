import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("8 Puzzle")
root.geometry("400x400")

def open_puzzle():
    N = 3
    win = tk.Toplevel(root)
    win.title("Gameplay")
    win.geometry("900x600")
    win.minsize(700, 450)
    win.transient(root) # bám cửa sổ cha
    #exit
    win.bind("<Escape>", lambda e: win.destroy())
    win.protocol("WM_DELETE_WINDOW", win.destroy)

    # Chia 2 cột co giãn (60% | 40%)
    win.grid_columnconfigure(0, weight=3, uniform="col")
    win.grid_columnconfigure(1, weight=2, uniform="col")
    win.grid_rowconfigure(0, weight=1)

    # Hai khung: board (grid 3x3) | side (nút điều khiển)
    board = ttk.Frame(win, padding=8)
    side  = ttk.Frame(win, padding=8)
    board.grid(row=0, column=0, sticky="nsew")
    side.grid(row=0, column=1, sticky="nsew")

    # Lưới 3x3 — dùng cùng uniform cho hàng & cột để ô vuông hơn
    for i in range(N):
        board.rowconfigure(i, weight=1, uniform="cell")
        board.columnconfigure(i, weight=1, uniform="cell")

    # Style
    style = ttk.Style(win)
    style.configure("Tile.TButton", font=("Segoe UI", 18, "bold"), padding=6)

    buttons = []
    num = 1
    for r in range(N):
        row_btns = []
        for c in range(N):
            txt = "" if (r, c) == (N-1, N-1) else str(num); num += (txt != "")
            btn = ttk.Button(board, text=txt, style="Tile.TButton")
            btn.grid(row=r, column=c, sticky="nsew", padx=6, pady=6, ipady=8)
            row_btns.append(btn)
        buttons.append(row_btns)

    # Panel bên phải
    ttk.Label(side, text="Controls", font=("Segoe UI", 14, "bold")).pack(pady=(0, 8), fill="x")
    ttk.Button(side, text="Shuffle").pack(fill="x", pady=6)
    ttk.Button(side, text="Solve").pack(fill="x", pady=6)
    ttk.Separator(side).pack(fill="x", pady=8)
    ttk.Button(side, text="Close", command=win.destroy).pack(fill="x", pady=6)

tk.Label(root, text="Game 8 Puzzle", font=("Segoe UI", 16, "bold")).pack(pady=50)
tk.Button(root, text="Play?", width=14, height=2, command=open_puzzle).pack()
tk.Button(root, text="Close", width=14, height=2, command=root.destroy).pack(pady=50)
root.mainloop()
