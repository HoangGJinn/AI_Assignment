# Import all algorithms for easy access
from .common import N, isValid, is_valid_solution, cost_estimate, heuristic_cost, f_cost
from .bfs import bfs_trace
from .dfs import dfs_trace
from .ucs import ucs_trace
from .dls import dls_trace, ids_trace_dls, ids_trace_dfs_with_limit
from .greedy import greedy_trace, a_star_trace
from .hill_climbing import hill_climbing_trace
from .simulated_annealing import simulated_annealing_trace
from .genetic import genetic_trace
from .beam import beam_trace
from .and_or import and_or_search, extract_path, print_plan
from .belief import belief_state_search, partial_observable_belief_search
from .backtracking import (
    backtracking, backtracking_trace, forward_backtracking_events, 
    forward_backtracking_trace
)
from .ac3 import (
    ac3_trace, ac3_events,
    solve_with_ac3_and_backtrack
)

__all__ = [
    'N', 'isValid', 'is_valid_solution', 'cost_estimate', 'heuristic_cost', 'f_cost',
    'bfs_trace', 'dfs_trace', 'ucs_trace',
    'dls_trace', 'ids_trace_dls', 'ids_trace_dfs_with_limit',
    'greedy_trace', 'a_star_trace', 'hill_climbing_trace', 'simulated_annealing_trace',
    'genetic_trace', 'beam_trace', 'and_or_search', 'belief_state_search', 
    'partial_observable_belief_search',
    'backtracking', 'backtracking_trace', 'forward_backtracking_events',
    'forward_backtracking_trace', 'extract_path', 'print_plan',
    'ac3_trace', 'ac3_events', 'get_domain_info', 'analyze_ac3_effectiveness',
    'solve_with_ac3_and_backtrack'
]
