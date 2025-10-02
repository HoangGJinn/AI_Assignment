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
    "Backtracking": [
        ("Backtracking", "backtracking"),
        ("Backtracking (nhanh)", "backtracking_fast"),
        ("FB", "forward_backtracking"),
        ("FB (nhanh)", "fb_fast"),
    ]
}