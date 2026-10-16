from collections import deque
from typing import List, Tuple


def program5(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 5
    
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
    # Same recurrence as Program 4,
    #   OPT[i] = c_i + min{ OPT[j] : i-k <= j <= i-1 },
    # but the min over the last k values is done with a sliding-window minimum.
    # The deque holds positions whose OPT values increase from front to back,
    # so the front is always the cheapest position inside the current window.
    # Each position is added once and removed at most once, so the whole loop
    # does Theta(n) work even though a single step can remove many positions.

    opt = [0] * (n + 1)      # opt[i] = minimum energy to land on panel i
    parent = [0] * (n + 1)   # parent[i] = position the best jump into i came from
    window = deque([0])      # start with the dock (position 0, cost 0)

    for i in range(1, n + 1):
        # 1) Drop positions that are more than k behind panel i (out of jump range)
        while window[0] < i - k:
            window.popleft()

        # 2) The front of the deque is the cheapest position we can jump from
        best_j = window[0]
        opt[i] = costs[i - 1] + opt[best_j]
        parent[i] = best_j

        # 3) Before adding i, remove positions from the back that are at least as
        #    expensive as i. They are older than i, so they leave the window first,
        #    and they are never cheaper: they can never be the minimum again.
        while window and opt[window[-1]] >= opt[i]:
            window.pop()
        window.append(i)

    # Rebuild the route by following parent pointers back from panel n
    visited_indices = []
    i = n
    while i > 0:
        visited_indices.append(i)
        i = parent[i]
    visited_indices.reverse()
    total_cost = opt[n]
    ############################

    return total_cost, visited_indices


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program5(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)
