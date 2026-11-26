"""Fill the solution placeholders of the 2026-11-09 DP/TSP and edit-distance notebooks.

Run from the homework root:  python tools/fill_solutions_dp_edit.py
Kept as a record of what was filled in. Idempotent: the patches only replace
placeholder text, so the provided scaffolding is left untouched.
"""
import json
import os

DP_TSP = {
    "答案/dp-tsp/dp-tsp.ipynb": {
        7: (
            "    ...",
            '''    n = len(adj_list)
    if n == 0:
        return []

    # Held-Karp with city 0 fixed as the start of the tour.  dp[mask][last]
    # is the cheapest path that starts at 0, visits exactly mask, and ends at
    # last; parent[] stores only the predecessor needed to rebuild the tour.
    start = 0
    full_mask = (1 << n) - 1
    dp = [None] * (1 << n)
    parent = [None] * (1 << n)
    dp[1] = {start: 0}
    parent[1] = {start: -1}

    # Every mask containing the start is odd.
    for mask in range(1, 1 << n, 2):
        layer = dp[mask]
        if not layer:
            continue
        for last, cost in layer.items():
            for nxt, weight in adj_list[last].items():
                bit = 1 << nxt
                if mask & bit:
                    continue
                next_mask = mask | bit
                next_cost = cost + weight
                next_layer = dp[next_mask]
                if next_layer is None:
                    next_layer = {}
                    dp[next_mask] = next_layer
                    parent[next_mask] = {}
                old = next_layer.get(nxt)
                if old is None or next_cost < old:
                    next_layer[nxt] = next_cost
                    parent[next_mask][nxt] = last

    best_cost = float("inf")
    best_last = -1
    full_layer = dp[full_mask]
    if full_layer:
        for last, cost in full_layer.items():
            closing = adj_list[last].get(start)
            if closing is not None and cost + closing < best_cost:
                best_cost = cost + closing
                best_last = last

    if best_last == -1:
        return []

    tour = []
    mask = full_mask
    last = best_last
    while last != -1:
        tour.append(last)
        previous = parent[mask][last]
        mask ^= 1 << last
        last = previous
    tour.reverse()
    return tour''',
        ),
    },
}

EDIT_DIST = {
    "答案/edit-dist/edit-dist.ipynb": {
        6: ("node = ...", "node = (5, 6)"),
        9: ("ans = ...", "ans = [2, 3]"),
        12: ("ans = ...", "ans = [1, 4]"),
        15: ("ans = ...", "ans = [3, 4]"),
        19: ("ans = ...", "ans = [1, 3]"),
        22: ("ans = ...", "ans = [2]"),
        26: (
            "    ...",
            '''    n = len(x)
    m = len(y)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp[i][0] = i
    for j in range(1, m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        row = dp[i]
        previous_row = dp[i - 1]
        xi = x[i - 1]
        for j in range(1, m + 1):
            substitute = previous_row[j - 1] + (xi != y[j - 1])
            insert = row[j - 1] + 1
            delete = previous_row[j] + 1
            row[j] = substitute if substitute < insert and substitute < delete else (insert if insert < delete else delete)

    x_aligned = []
    y_aligned = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (x[i - 1] != y[j - 1]):
            x_aligned.append(x[i - 1])
            y_aligned.append(y[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            x_aligned.append(x[i - 1])
            y_aligned.append("-")
            i -= 1
        else:
            x_aligned.append("-")
            y_aligned.append(y[j - 1])
            j -= 1

    x_aligned.reverse()
    y_aligned.reverse()
    return "".join(x_aligned), "".join(y_aligned)''',
        ),
    },
}


def patch(path, replacements):
    with open(path, encoding="utf-8") as f:
        notebook = json.load(f)

    for index, (old, new) in replacements.items():
        cell = notebook["cells"][index]
        source = "".join(cell["source"])
        if new in source:
            continue
        assert source.count(old) == 1, (path, index, "placeholder not found exactly once")
        cell["source"] = source.replace(old, new).splitlines(keepends=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("patched", path)


if __name__ == "__main__":
    for solutions in (DP_TSP, EDIT_DIST):
        for notebook, replacements in solutions.items():
            patch(os.path.join(os.getcwd(), notebook), replacements)
