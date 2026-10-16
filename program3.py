import sys
import threading
from typing import List, Tuple


def program3(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 3
    
    Parameters:
    n (int): number of panels
    k (int): maximum number of positions in a forward jump
    costs (List[int]): the landing costs of the panels

    Returns:
    int:  minimum total energy cost
    List[int]: the indices of the visited panels in increasing order(1-indexed, including n and excluding 0)
    """
    ############################
    # Add your code here
    #
    # Naive recursion on the recurrence
    #   OPT(0) = 0
    #   OPT(i) = c_i + min{ OPT(j) : max(0, i-k) <= j <= i-1 }
    # The last jump into panel i must come from one of the k positions before it,
    # so we try all of them. Nothing is cached, so the same subproblems are solved
    # many times. Worst case (k = n): T(n) = T(n-1) + ... + T(0) = 2^(n-1), so O(2^n).

    def solve(i):
        # Returns (min cost to land on panel i, route to i).
        # The route is a linked list (previous_route, i) so building it is O(1)
        # per call and does not change the O(2^n) running time.
        if i == 0:
            return 0, None  # the dock is free and has no landings
        best_cost, best_route = float('inf'), None
        # Try every position the last jump could have come from
        for j in range(max(0, i - k), i):
            cost_j, route_j = solve(j)
            if cost_j < best_cost:
                best_cost, best_route = cost_j, route_j
        # costs is 0-indexed, so panel i costs costs[i - 1]
        return best_cost + costs[i - 1], (best_route, i)

    # Recursion depth can reach n (e.g. when k = 1), more than Python's default
    # stack allows. Run it in a thread with a bigger stack and a higher limit.
    result = []
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old_limit, n + 1000))
    old_stack = threading.stack_size()
    threading.stack_size(512 * 1024 * 1024)
    worker = threading.Thread(target=lambda: result.append(solve(n)))
    worker.start()
    worker.join()
    threading.stack_size(old_stack)
    sys.setrecursionlimit(old_limit)
    total_cost, route = result[0]

    # Unroll the linked list (it is stored from panel n back to the first landing)
    visited_indices = []
    while route is not None:
        route, panel = route
        visited_indices.append(panel)
    visited_indices.reverse()
    ############################

    return total_cost, visited_indices


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program3(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)
