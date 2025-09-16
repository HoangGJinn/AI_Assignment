        if 'log_box' in globals():
            r, c = path[i-1]
            if type in ("greedy", "a_star") and i-1 < len(step_costs):
                log_box.insert(tk.END, f"Đặt quân {i}: ({r+1}, {c+1}) | cost = {step_costs[i-1]}")
            else:
                log_box.insert(tk.END, f"Đặt quân {i}: ({r+1}, {c+1})")
            log_box.yview_moveto(1.0)