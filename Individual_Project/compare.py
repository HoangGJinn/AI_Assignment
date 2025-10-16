import os
import time
import tkinter as tk
from tkinter import messagebox, Toplevel


def _bfs_bench(target_idx):
    from queue import Queue
    from solvers.common import N, isValid, is_valid_solution
    import copy
    start = time.perf_counter()
    q = Queue(); empty = [[0]*N for _ in range(N)]; q.put((empty,0,[]))
    expanded = 0; result = []
    while not q.empty():
        board,row,path = q.get(); expanded += 1
        if row == N:
            if is_valid_solution(board, target_idx): result = path; break
        for col in range(N):
            if isValid(board,row,col):
                nb = copy.deepcopy(board); nb[row][col]=1
                q.put((nb,row+1,path+[(row,col)]))
    elapsed = time.perf_counter() - start
    return elapsed, expanded, bool(result)

def _dfs_bench(target_idx):
    from collections import deque
    from solvers.common import N, isValid, is_valid_solution
    import copy
    start = time.perf_counter(); st = deque(); empty = [[0]*N for _ in range(N)]
    st.append((empty,0,[])); expanded = 0; ok = False
    while st:
        board,row,path = st.pop(); expanded += 1
        if row == N:
            ok = is_valid_solution(board, target_idx)
            if ok: break
        for col in range(N):
            if isValid(board,row,col):
                nb = copy.deepcopy(board); nb[row][col]=1
                st.append((nb,row+1,path+[(row,col)]))
    elapsed = time.perf_counter() - start
    return elapsed, expanded, ok

def _ucs_bench(target_idx):
    import heapq, copy
    from itertools import count
    from solvers.common import N, isValid, is_valid_solution, cost_estimate
    start = time.perf_counter(); pq = []; tie = count(); empty = [[0]*N for _ in range(N)]
    heapq.heappush(pq,(0,0,next(tie),empty,[])); expanded=0; found=False
    while pq:
        cost,row,_,board,path = heapq.heappop(pq); expanded+=1
        if row==N:
            if is_valid_solution(board,target_idx): found=True; break
            continue
        for col in range(N):
            if isValid(board,row,col):
                nb = copy.deepcopy(board); nb[row][col]=1
                heapq.heappush(pq,(cost+cost_estimate(row,col),row+1,next(tie),nb,path+[(row,col)]))
    elapsed = time.perf_counter() - start
    return elapsed, expanded, found

def _dls_bench(target_idx, limit, N=8):
    from solvers.common import isValid, is_valid_solution
    import copy
    expanded = 0
    def dls(board,row,path,lim):
        nonlocal expanded; expanded += 1
        if row==N: return path if is_valid_solution(board,target_idx) else "failure"
        if lim==0: return "cutoff"
        cutoff=False
        for col in range(N):
            if isValid(board,row,col):
                nb = copy.deepcopy(board); nb[row][col]=1
                res = dls(nb,row+1,path+[(row,col)],lim-1)
                if res=="cutoff": cutoff=True
                elif res!="failure": return res
        return "cutoff" if cutoff else "failure"
    start = time.perf_counter(); empty = [[0]*N for _ in range(N)]
    res = dls(empty,0,[],limit); elapsed = time.perf_counter() - start
    return elapsed, expanded, isinstance(res,list)

def _ids_dls_bench(target_idx):
    expanded=0; start=time.perf_counter()
    for lim in range(0,9):
        t,e,ok = _dls_bench(target_idx,lim)
        expanded += e
        if ok: return time.perf_counter()-start, expanded, True
    return time.perf_counter()-start, expanded, False

def _ids_dfs_bench(target_idx):
    from collections import deque
    from solvers.common import N, isValid, is_valid_solution
    import copy
    def dfs_limit(limit):
        nonlocal expanded
        st=deque(); empty=[[0]*N for _ in range(N)]; st.append((empty,0,[],limit)); cutoff=False
        while st:
            board,row,path,lim = st.pop(); expanded+=1
            if row==N:
                if is_valid_solution(board,target_idx): return path
                continue
            if lim==0: cutoff=True; continue
            for col in range(N):
                if isValid(board,row,col):
                    nb=copy.deepcopy(board); nb[row][col]=1
                    st.append((nb,row+1,path+[(row,col)],lim-1))
        return "cutoff" if cutoff else "failure"
    start=time.perf_counter(); expanded=0
    for lim in range(0,9):
        res = dfs_limit(lim)
        if res!="cutoff" and res!="failure":
            return time.perf_counter()-start, expanded, True
    return time.perf_counter()-start, expanded, False

def _greedy_bench(target_idx):
    import heapq, copy
    from itertools import count
    from solvers.common import N, heuristic_cost
    start = time.perf_counter(); pq = []; tie = count(); empty = [[0]*N for _ in range(N)]
    heapq.heappush(pq,(heuristic_cost(empty),0,next(tie),empty,[])); expanded=0; found=False
    while pq:
        h,row,_,board,path = heapq.heappop(pq); expanded+=1
        if row==N:
            found=True; break
        for col in range(N):
            nb = copy.deepcopy(board); nb[row][col]=1
            heapq.heappush(pq,(heuristic_cost(nb),row+1,next(tie),nb,path+[(row,col)]))
    return time.perf_counter()-start, expanded, found

def _astar_bench(target_idx):
    import heapq, copy
    from itertools import count
    from solvers.common import N, isValid, is_valid_solution, cost_estimate, heuristic_cost
    start = time.perf_counter(); pq=[]; tie=count(); empty=[[0]*N for _ in range(N)]
    g0=0; h0=heuristic_cost(empty); f0=g0+h0; heapq.heappush(pq,(f0,0,next(tie),empty,[]))
    expanded=0; found=False
    while pq:
        f,row,_,board,path = heapq.heappop(pq); expanded+=1
        if row==N:
            if is_valid_solution(board,target_idx): found=True; break
            continue
        for col in range(N):
            if isValid(board,row,col):
                nb = copy.deepcopy(board); nb[row][col]=1
                step = cost_estimate(row,col)
                g = (row+1) + step
                h = heuristic_cost(nb)
                heapq.heappush(pq,(g+h,row+1,next(tie),nb,path+[(row,col)]))
    return time.perf_counter()-start, expanded, found

def _hill_bench(target_idx):
    import heapq, copy
    from itertools import count
    from solvers.common import N, isValid, is_valid_solution, heuristic_cost
    start=time.perf_counter(); tie=count(); empty=[[0]*N for _ in range(N)]
    pq=[(heuristic_cost(empty),0,next(tie),empty,[])]; expanded=0; prev_h=10**9; found=False
    while pq:
        h,row,_,board,path = heapq.heappop(pq); pq.clear(); expanded+=1
        if row==N: found = is_valid_solution(board,target_idx); break
        improved=False
        for col in range(N):
            if isValid(board,row,col):
                nb=copy.deepcopy(board); nb[row][col]=1
                hn=heuristic_cost(nb); heapq.heappush(pq,(hn,row+1,next(tie),nb,path+[(row,col)]))
                if hn<prev_h: improved=True
        if not improved: break
        prev_h=h
    return time.perf_counter()-start, expanded, found

def _sa_bench(target_idx):
    from solvers.simulated_annealing import simulated_annealing_trace
    start=time.perf_counter(); path, steps, found, _ = simulated_annealing_trace(target_idx)
    return time.perf_counter()-start, len(steps), found

def _genetic_bench(target_idx):
    from solvers.genetic import genetic_trace
    start=time.perf_counter(); path, gen, found, *_ = genetic_trace(target_idx)
    return time.perf_counter()-start, gen, found

def _beam_bench(target_idx):
    from solvers.beam import beam_trace
    start=time.perf_counter(); path = beam_trace(target_idx)
    return time.perf_counter()-start, (len(path) if path else 0), bool(path)

def _andor_bench(target_idx):
    from solvers.and_or import and_or_search
    start=time.perf_counter(); plan = and_or_search(target_idx)
    def count_nodes(node):
        if not node: return 1
        cnt=1
        if isinstance(node.get("plan"),(list,tuple)) and node["plan"]:
            _,child=node["plan"]; cnt+=count_nodes(child)
        if node.get("children"):
            for ch in node["children"]: cnt+=count_nodes(ch)
        return cnt
    return time.perf_counter()-start, count_nodes(plan), bool(plan and plan.get("Goal"))

def _belief_bench():
    from solvers.belief import belief_state_search
    start=time.perf_counter(); path, final_belief, logs = belief_state_search()
    return time.perf_counter()-start, len(logs), bool(final_belief)

def _partial_belief_bench(target_idx):
    from solvers.belief import partial_observable_belief_search
    start=time.perf_counter(); path, final_belief, logs, _ = partial_observable_belief_search(target_idx, 2)
    return time.perf_counter()-start, len(logs), bool(final_belief)

def _backtracking_bench(target_idx):
    from solvers.backtracking import backtracking
    start=time.perf_counter(); events = backtracking(target_idx)
    expanded = sum(1 for e in events if e[0] in ("place","remove"))
    found = any(e[0]=="solution" for e in events)
    return time.perf_counter()-start, expanded, found

def _fb_bench(target_idx):
    from solvers.backtracking import forward_backtracking_events
    start=time.perf_counter(); events = forward_backtracking_events(target_idx)
    expanded = sum(1 for e in events if e[0] in ("place","remove"))
    found = any(e[0]=="solution" for e in events)
    return time.perf_counter()-start, expanded, found

def _ac3_bench(target_idx):
    from solvers.ac3 import ac3_events
    start=time.perf_counter(); events = ac3_events(target_idx)
    expanded = sum(1 for e in events if e[0] in ("place","remove"))
    found = any(e[0]=="solution" for e in events)
    return time.perf_counter()-start, expanded, found

def _ac3_fast_bench(target_idx):
    from solvers.ac3 import ac3_trace
    start=time.perf_counter(); path = ac3_trace(target_idx)
    return time.perf_counter()-start, (len(path) if path else 0), bool(path)

def _save_fig(fig, filename):
    out_dir = os.path.join(os.path.dirname(__file__), 'image')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    fig.savefig(path, dpi=120, bbox_inches='tight')
    return path

def _render_fig_in_tk(root, fig, title):
    try:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    except Exception:
        return
    win = Toplevel(root)
    win.title(title)
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def show_compare_menu(root):
    menu = Toplevel(root)
    menu.title("Chọn nhóm so sánh")
    menu.geometry("360x260")
    menu.configure(bg="#ECE7E7")

    tk.Label(menu, text="Chọn nhóm thuật toán để so sánh", font=("Segoe UI", 11, "bold"), bg="#ECE7E7").pack(pady=(10,6))

    def run_and_show(kind):
        menu.destroy()
        try:
            import matplotlib.pyplot as plt
        except Exception:
            messagebox.showerror("Thiếu thư viện", "Cần cài matplotlib để vẽ biểu đồ.")
            return

        target_idx = 8

        if kind == "uninformed":
            labels = ["BFS", "DFS", "DLS", "IDS(with DLS)", "IDS(with DFS)"]
            funcs = [_bfs_bench, _dfs_bench, lambda idx: _dls_bench(idx, limit=8), _ids_dls_bench, _ids_dfs_bench]
            times=[]; nodes=[]
            for f in funcs:
                t,n,_=f(target_idx); times.append(t*1000.0); nodes.append(n)
            fig,(ax1,ax2)=plt.subplots(2,1,figsize=(8,6)); fig.suptitle("So sánh - Uninformed Search")
            b=ax1.bar(labels,times,color="#AC6BCF"); ax1.set_title("Thời gian thực thi"); ax1.set_ylabel("Milli-giây")
            [ax1.text(x.get_x()+x.get_width()/2,x.get_height(),f"{v:.2f}",ha='center',va='bottom') for x,v in zip(b,times)]
            c=ax2.bar(labels,nodes,color="#7D6BCF"); ax2.set_title("Số node mở rộng"); ax2.set_ylabel("Số node")
            [ax2.text(x.get_x()+x.get_width()/2,x.get_height(),f"{v}",ha='center',va='bottom') for x,v in zip(c,nodes)]
            fig.tight_layout(rect=[0,0.03,1,0.95]); _save_fig(fig,'uninformed_compare.png'); _render_fig_in_tk(root, fig, "Uninformed Search")

        elif kind == "informed":
            labels=["UCS","Greedy","A* Search"]; funcs=[_ucs_bench,_greedy_bench,_astar_bench]
            times=[]; nodes=[]
            for f in funcs:
                t,n,_=f(target_idx); times.append(t*1000.0); nodes.append(n)
            fig,(ax1,ax2)=plt.subplots(2,1,figsize=(8,6)); fig.suptitle("So sánh - Informed Search")
            b=ax1.bar(labels,times,color="#C56BD1"); ax1.set_title("Thời gian thực thi"); ax1.set_ylabel("Milli-giây")
            [ax1.text(x.get_x()+x.get_width()/2,x.get_height(),f"{v:.2f}",ha='center',va='bottom') for x,v in zip(b,times)]
            c=ax2.bar(labels,nodes,color="#8F6BD1"); ax2.set_title("Số node mở rộng"); ax2.set_ylabel("Số node")
            [ax2.text(x.get_x()+x.get_width()/2,x.get_height(),f"{v}",ha='center',va='bottom') for x,v in zip(c,nodes)]
            fig.tight_layout(rect=[0,0.03,1,0.95]); _save_fig(fig,'informed_compare.png'); _render_fig_in_tk(root, fig, "Informed Search")

        elif kind == "local":
            labels=["Hill","SA","Genetic","Beam"]; funcs=[_hill_bench,_sa_bench,_genetic_bench,_beam_bench]
            times=[]; nodes=[]
            for f in funcs:
                t,n,_=f(target_idx); times.append(t*1000.0); nodes.append(n)
            fig,(ax1,ax2)=plt.subplots(2,1,figsize=(8,6)); fig.suptitle("So sánh - Local Search")
            b=ax1.bar(labels,times,color="#6BCFAE"); ax1.set_title("Thời gian thực thi"); ax1.set_ylabel("Milli-giây")
            [ax1.text(x.get_x()+x.get_width()/2,x.get_height(),f"{v:.2f}",ha='center',va='bottom') for x,v in zip(b,times)]
            c=ax2.bar(labels,nodes,color="#6B9BCF"); ax2.set_title("Số node mở rộng"); ax2.set_ylabel("Số node")
            [ax2.text(x.get_x()+x.get_width()/2,x.get_height(),f"{v}",ha='center',va='bottom') for x,v in zip(c,nodes)]
            fig.tight_layout(rect=[0,0.03,1,0.95]); _save_fig(fig,'local_compare.png'); _render_fig_in_tk(root, fig, "Local Search")

        elif kind == "nondet":
            labels=["AND-OR","Belief","Partial Belief"]; funcs=[_andor_bench, lambda _: _belief_bench(), _partial_belief_bench]
            times=[]; nodes=[]
            for f,lab in zip(funcs,labels):
                if lab=="Belief": t,n,_=f(None)
                else: t,n,_=f(target_idx)
                times.append(t*1000.0); nodes.append(n)
            fig,(ax1,ax2)=plt.subplots(2,1,figsize=(8,6)); fig.suptitle("So sánh - Nondeterministic")
            b=ax1.bar(labels,times,color="#CF6B8E"); ax1.set_title("Thời gian thực thi"); ax1.set_ylabel("Milli-giây")
            [ax1.text(x.get_x()+x.get_width()/2,x.get_height(),f"{v:.2f}",ha='center',va='bottom') for x,v in zip(b,times)]
            c=ax2.bar(labels,nodes,color="#CF6BA3"); ax2.set_title("Số node mở rộng"); ax2.set_ylabel("Số node")
            [ax2.text(x.get_x()+x.get_width()/2,x.get_height(),f"{v}",ha='center',va='bottom') for x,v in zip(c,nodes)]
            fig.tight_layout(rect=[0,0.03,1,0.95]); _save_fig(fig,'nondeterministic_compare.png'); _render_fig_in_tk(root, fig, "Nondeterministic")

        elif kind == "backtracking":
            labels=["Backtracking","Forward-Backtracking","AC3 + Backtracking"]; funcs=[_backtracking_bench,_fb_bench,_ac3_bench]
            times=[]; nodes=[]
            for f in funcs:
                t,n,_=f(target_idx); times.append(t*1000.0); nodes.append(n)
            fig,(ax1,ax2)=plt.subplots(2,1,figsize=(10,6)); fig.suptitle("So sánh - Backtracking Algorithms")
            b=ax1.bar(labels,times,color=["#B0CF6B","#89CF6B","#6BA3CF"]); ax1.set_title("Thời gian thực thi"); ax1.set_ylabel("Milli-giây")
            [ax1.text(x.get_x()+x.get_width()/2,x.get_height(),f"{v:.2f}",ha='center',va='bottom') for x,v in zip(b,times)]
            c=ax2.bar(labels,nodes,color=["#B0CF6B","#89CF6B","#6BA3CF"]); ax2.set_title("Số node mở rộng"); ax2.set_ylabel("Số node")
            [ax2.text(x.get_x()+x.get_width()/2,x.get_height(),f"{v}",ha='center',va='bottom') for x,v in zip(c,nodes)]
            fig.tight_layout(rect=[0,0.03,1,0.95]); _save_fig(fig,'backtracking_compare.png'); _render_fig_in_tk(root, fig, "Backtracking Algorithms")

    tk.Button(menu, text="Uninformed", width=22, bg="#AC6BCF", fg="white", command=lambda: run_and_show("uninformed")).pack(pady=6)
    tk.Button(menu, text="Informed", width=22, bg="#C56BD1", fg="white", command=lambda: run_and_show("informed")).pack(pady=6)
    tk.Button(menu, text="Local Search", width=22, bg="#6BCFAE", fg="white", command=lambda: run_and_show("local")).pack(pady=6)
    tk.Button(menu, text="Nondeterministic", width=22, bg="#CF6B8E", fg="white", command=lambda: run_and_show("nondet")).pack(pady=6)
    tk.Button(menu, text="Backtracking", width=22, bg="#89CF6B", fg="white", command=lambda: run_and_show("backtracking")).pack(pady=6)


