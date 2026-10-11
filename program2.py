from typing import List, Tuple


def program2(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 2
    
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
    # Our idea: the costs rise up to a peak p, then fall. Split any route at the peak:
    #   x = the last landing before p (or p itself, if the route lands on the peak)
    #   b = the first landing after p
    # Left of the peak, costs are non-decreasing, so the cheapest way to reach x
    # is a greedy that works backward from x with max jumps (x, x-k, x-2k, ...).
    # Right of the peak, costs are non-increasing, so the cheapest way from b to n
    # is the Program 1 greedy idea: step forward with max jumps (b, b+k, b+2k, ..., n).
    # Only the crossing point near the peak needs a choice: x in [p-k, p] and
    # b in [p+1, x+k], which is O(k) candidates. Total time here would be Theta(n).

    c = [0] + costs  # shift to 1-indexed so c[i] is panel i (c[0] = dock, free)

    # Step 1: find the peak index p with one linear scan. Theta(n)
    p = 1
    for i in range(2, n + 1):
        if c[i] > c[p]:
            p = i

    # Step 2: f[x] = min cost to reach x using only panels before the peak.
    # Backward greedy: land on x, then x-k, x-2k, ... until reaching the dock.
    # Theta(p)
    f = [0] * (p + 1)
    for x in range(1, p):
        f[x] = c[x] + (f[x - k] if x - k > 0 else 0)

    # Also allow landing on the peak: f[p] = c[p] + best f[a] for a in [p-k, p-1].
    # (Sometimes cheaper. For example, n=4, k=2, c=[50,100,60,1] -> optimal route [2, 4].)
    lo = max(0, p - k)
    best_a = lo
    for a in range(lo, p):
        if f[a] < f[best_a]:
            best_a = a
    f[p] = c[p] + f[best_a]

    # Step 3: g[b] = cost of the forward greedy route b -> n (including b).
    # g[b] = c[b] + g[min(b+k, n)], filled right to left. Theta(n - p)
    g = [0] * (n + 1)
    g[n] = c[n]
    for b in range(n - 1, p, -1):
        g[b] = c[b] + g[min(b + k, n)]

    # Step 4: join the two sides at the peak.
    # best_b[t] = the b in [p+1, t] with the smallest g[b] (a running minimum).
    hi = min(p + k, n)
    best_b = [0] * (hi + 1)
    best_b[p + 1] = p + 1
    for t in range(p + 2, hi + 1):
        best_b[t] = t if g[t] < g[best_b[t - 1]] else best_b[t - 1]

    # Try every crossing point x in [p-k, p]; the best partner b must lie in
    # [p+1, x+k], so it is best_b[x+k]. O(k) work.
    best_total = float('inf')
    best_x = best_bb = -1
    for x in range(lo, p + 1):
        t = min(x + k, n)
        if t < p + 1:  # cannot jump past the peak from x
            continue
        b = best_b[t]
        if f[x] + g[b] < best_total:
            best_total, best_x, best_bb = f[x] + g[b], x, b

    # Step 5: rebuild the route from the chosen x and b.
    def backward_chain(x):
        # landings x, x-k, x-2k, ... (> 0), returned in increasing order
        out = []
        while x > 0:
            out.append(x)
            x -= k
        return out[::-1]

    if best_x == p:  # route lands on the peak
        visited_indices = backward_chain(best_a) + [p]
    else:
        visited_indices = backward_chain(best_x)

    position = best_bb  # forward greedy from b to n
    visited_indices.append(position)
    while position < n:
        position = min(position + k, n)
        visited_indices.append(position)
    ############################

    return best_total, visited_indices


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program2(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)