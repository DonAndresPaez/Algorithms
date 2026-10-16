import sys
import threading
from typing import List, Tuple


def program4A(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 4A
    
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
    # Top-down dynamic programming: the same recurrence as Program 3,
    #   OPT(0) = 0
    #   OPT(i) = c_i + min{ OPT(j) : max(0, i-k) <= j <= i-1 }
    # but each OPT(i) is computed once and stored in memo[i] (memoization).
    # Panels 1..k can be reached straight from the dock, and OPT(0) = 0 is always
    # the smallest option (costs are positive), so OPT(i) = c_i there in O(1).
    # Every other panel scans k predecessors once: Theta(k + (n-k)k) total.

    memo = [None] * (n + 1)    # memo[i] = OPT(i), None means "not computed yet"
    parent = [0] * (n + 1)     # parent[i] = position the best jump into i came from
    memo[0] = 0

    def opt(i):
        if memo[i] is not None:          # already solved: reuse the answer
            return memo[i]
        if i <= k:                       # reachable from the dock, which costs 0
            memo[i] = costs[i - 1]
            parent[i] = 0
            return memo[i]
        best_j = i - k
        best = opt(best_j)
        for j in range(i - k + 1, i):    # try the other k-1 predecessors
            value = opt(j)
            if value < best:
                best, best_j = value, j
        memo[i] = costs[i - 1] + best
        parent[i] = best_j
        return memo[i]

    # The recursion can go about n levels deep, which is more than Python's default
    # stack allows for large n. Run it in a thread with a bigger stack and a higher
    # recursion limit so large inputs do not crash.
    result = []
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old_limit, n + 1000))
    old_stack = threading.stack_size()
    threading.stack_size(512 * 1024 * 1024)
    worker = threading.Thread(target=lambda: result.append(opt(n)))
    worker.start()
    worker.join()
    threading.stack_size(old_stack)
    sys.setrecursionlimit(old_limit)
    total_cost = result[0]

    # Rebuild the route by following parent pointers back from panel n
    visited_indices = []
    i = n
    while i > 0:
        visited_indices.append(i)
        i = parent[i]
    visited_indices.reverse()
    ############################

    return total_cost, visited_indices


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program4A(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)
