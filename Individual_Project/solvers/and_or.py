# And-Or Search algorithm for N-Queens
import copy
from .common import N, isValid, is_valid_solution

def and_or_search(x):
    def or_search(board, row):
        if row == N:
            return {"Goal": is_valid_solution(board, x), "plan": []}

        for col in range(N):
            if isValid(board, row, col):
                new_board = copy.deepcopy(board)
                new_board[row][col] = 1
                success, child_plan = and_search([new_board], row + 1)
                if success:
                    return {"Goal": True, "plan": [(row, col), child_plan]}

        return {"Goal": False, "plan": []}

    def and_search(list_boards, row):
        results = []
        for b in list_boards:
            child = or_search(b, row)
            if not child["Goal"]:
                return False, {"Goal": False}
            results.append(child)
        return True, {"Goal": True, "children": results}

    empty_board = [[0 for _ in range(N)] for _ in range(N)]
    return or_search(empty_board, 0)

def print_plan(plan, indent=0):
    space = "  " * indent
    if not plan:
        print(space + "None")
        return

    if plan.get("Goal") is False:
        print(space + "Fail")
        return

    if "plan" in plan and plan["plan"]:
        move, child = plan["plan"]
        print(space + f"OR: đặt hậu tại {move}")
        print_plan(child, indent + 0.5)

    if "children" in plan:
        print(space + "AND:")
        for idx, child in enumerate(plan["children"]):
            print(space + f"  Nhánh {idx+1}:")
            print_plan(child, indent + 1)

def extract_path(plan):
    """
    Lấy path [(row, col), ...] từ cây kế hoạch and_or_search.
    """
    path = []
    current = plan
    while current and current.get("Goal"):
        if "plan" in current and isinstance(current["plan"], (list, tuple)) and len(current["plan"]) == 2:
            move, child = current["plan"]
            path.append(move)
            current = child
        elif "children" in current and current["children"]:
            current = current["children"][0]
        else:
            break
    print(path)
    return path
