from typing import List, Tuple


def program1(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 1
    
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
    # Greedy idea: costs are non-increasing, so panels further right are never
    # more expensive. Every jump goes as far as allowed (k positions in this case), which both
    # minimizes the number of landings and lands on the cheapest reachable panel.
    # Runs in Theta(n/k) time: one iteration per landing.
    total_cost = 0
    visited_indices = []
    position = 0  # current position, 1-indexed panel number (0 = dock)

    while position < n:
        # Jump k forward, but never past panel n (the robot must land exactly on n)
        position = min(position + k, n)
        # costs is a 0-indexed list, so panel p costs costs[p - 1]
        total_cost += costs[position - 1]
        visited_indices.append(position)
    ############################

    return total_cost, visited_indices


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program1(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)