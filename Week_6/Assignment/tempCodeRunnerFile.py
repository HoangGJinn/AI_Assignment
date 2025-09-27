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