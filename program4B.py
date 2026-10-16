from typing import List, Tuple


def program4B(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 4B
    
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
    # Bottom-up dynamic programming: fill OPT[0..n] from left to right using
    #   OPT[0] = 0
    #   OPT[i] = c_i + min{ OPT[j] : max(0, i-k) <= j <= i-1 }
    # When we reach panel i, every OPT[j] with j < i is already in the table.
    # Panels 1..k are reachable from the dock (cost 0), so OPT[i] = c_i there.
    # Every other panel scans k predecessors: Theta(k + (n-k)k) total.

    opt = [0] * (n + 1)      # opt[i] = minimum energy to land on panel i
    parent = [0] * (n + 1)   # parent[i] = position the best jump into i came from

    # Panels reachable directly from the dock: O(1) each
    for i in range(1, min(k, n) + 1):
        opt[i] = costs[i - 1]
        parent[i] = 0

    # Remaining panels: pick the cheapest of the k positions before i
    for i in range(k + 1, n + 1):
        best_j = i - k
        for j in range(i - k + 1, i):
            if opt[j] < opt[best_j]:
                best_j = j
        opt[i] = costs[i - 1] + opt[best_j]
        parent[i] = best_j

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

    m, indices = program4B(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)
