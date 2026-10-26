"""Fill the solution placeholders of the 2026-10-26 DFS/SCC and shortest-path notebooks.

Run from the homework root:  python tools/fill_solutions_dfs_sp.py
Kept as a record of what was filled in. Idempotent: the patches only replace
placeholder text, so the provided scaffolding is left untouched.
"""
import json
import os

DFS_SCC = {
    "答案/dfs-scc/dfs-scc.ipynb": {
        8: (
            '''    def explore(adj_list, curr):
        """
        implements the explore subroutine from DPV, which is used in DFS. feel free to delete this 
        function and use an alternative implementation if you prefer.

        args:
            adj_list:List[List] = an adjacency list 
            curr:int = the node currently being traversed
        
        return:
            None
        """
        ...
    
    # implement the dfs and path reconstruction here
    ...''',
            '''    n = len(adj_list)
    prev = [-1] * n
    visited = [False] * n
    visited[s] = True
    stack = [s]

    # Iterative DFS; prev records the tree edge used to discover each node.
    while stack:
        u = stack.pop()
        if u == t:
            break
        for v in reversed(adj_list[u]):
            if not visited[v]:
                visited[v] = True
                prev[v] = u
                stack.append(v)

    if not visited[t]:
        return []

    path = []
    node = t
    while node != -1:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path''',
        ),
        17: (
            '''    # YOUR CODE HERE
    ...''',
            '''    n = len(adj_list)
    visited = [False] * n

    # A global clock shared by all DFS trees. Roots and neighbours are visited
    # in increasing node order, which is the required tie-breaking rule.
    for root in range(n):
        if visited[root]:
            continue
        visited[root] = True
        pre.append((root, time))
        time += 1
        stack = [(root, 0)]

        while stack:
            u, next_index = stack[-1]
            if next_index < len(adj_list[u]):
                v = adj_list[u][next_index]
                stack[-1] = (u, next_index + 1)
                if not visited[v]:
                    visited[v] = True
                    pre.append((v, time))
                    time += 1
                    stack.append((v, 0))
            else:
                stack.pop()
                post.append((u, time))
                time += 1''',
        ),
        21: (
            '''    ...''',
            '''    reversed_adj_list = [[] for _ in adj_list]
    for u, neighbors in enumerate(adj_list):
        for v in neighbors:
            reversed_adj_list[v].append(u)

    for neighbors in reversed_adj_list:
        neighbors.sort()
    return reversed_adj_list''',
        ),
        25: (
            '''    scc_list = []

    # YOUR CODE HERE
    ...''',
            '''    scc_list = []

    # Kosaraju-Sharir: decreasing post order on the reversed graph, then each
    # DFS tree in the original graph is one SCC.
    reversed_adj_list = reverse_graph(adj_list)
    _, post = get_pre_post(reversed_adj_list)

    n = len(adj_list)
    visited = [False] * n
    for node, _ in reversed(post):
        if visited[node]:
            continue

        component = set()
        visited[node] = True
        stack = [node]
        while stack:
            u = stack.pop()
            component.add(u)
            for v in adj_list[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)
        scc_list.append(component)''',
        ),
    },
}

SHORTEST_PATHS = {
    "答案/shortest-paths/shortest-paths.ipynb": {
        11: (
            '''    # TODO: your code here!
    pass''',
            '''    if dists[u] + w < dists[v]:
        dists[v] = dists[u] + w
        if prev is not None:
            prev[v] = u''',
        ),
        13: (
            '''    ...''',
            '''    n = len(G)
    INF = float("inf")
    dists = [INF] * n
    prev = [-1] * n
    dists[s] = 0

    # heapq has no decreaseKey, so stale copies are simply ignored when popped.
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dists[u]:
            continue
        if u == t:
            break
        for v, w in G[u]:
            new_dist = d + w
            if new_dist < dists[v]:
                dists[v] = new_dist
                prev[v] = u
                heapq.heappush(pq, (new_dist, v))

    if dists[t] == INF:
        return []

    path = []
    node = t
    while node != -1:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path''',
        ),
        16: (
            '''    ...''',
            '''    n = len(G)
    edges = [(u, v, w) for u in range(n) for v, w in G[u]]

    # The assignment asks for [] whenever the graph contains any negative cycle,
    # even one unreachable from s. Starting every vertex at distance 0 is
    # equivalent to adding a virtual source with 0-weight edges to all vertices.
    dists = [0] * n
    for _ in range(n):
        updated = False
        for u, v, w in edges:
            new_dist = dists[u] + w
            if new_dist < dists[v]:
                dists[v] = new_dist
                updated = True
        if not updated:
            break
    else:
        return []

    INF = float("inf")
    dists = [INF] * n
    prev = [-1] * n
    dists[s] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dists[u] != INF:
                new_dist = dists[u] + w
                if new_dist < dists[v]:
                    dists[v] = new_dist
                    prev[v] = u
                    updated = True
        if not updated:
            break

    if dists[t] == INF:
        return []

    path = []
    node = t
    while node != -1:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path''',
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
    for solutions in (DFS_SCC, SHORTEST_PATHS):
        for notebook, replacements in solutions.items():
            patch(os.path.join(os.getcwd(), notebook), replacements)
