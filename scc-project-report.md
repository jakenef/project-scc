# Project Report - Network Analysis SCCs

## Baseline

### Design Experience

_Fill me in_

### Theoretical Analysis - Pre/Post Order Traversal

#### Time

#### prepost

```py
def prepost(graph: GRAPH) -> list[dict[str, list[int]]]:
    """
    Return a list of DFS trees.
    Each tree is a dict mapping each node label to a list of [pre, post] order numbers.
    The graph should be searched in order of the keys in the dictionary.
    """
    visited = set()
    forest: list[dict[str, list[int]]] = []
    clock = 1

    def explore(u: str, tree: dict[str, list[int]]) -> None:
        nonlocal clock
        visited.add(u)
        tree[u] = [clock, -1]
        clock += 1

        for v in graph.get(u, []):              # for each vertex in the edge list for this specific vertex
            if v not in visited:
                explore(v, tree)                # O(e) for every reachable vertex

        tree[u][1] = clock
        clock += 1

    for u in graph.keys():                      # O(v) for every vertex, skipping those that are already visited by explore
        if u not in visited:
            tree: dict[str, list[int]] = {}
            explore(u, tree)                    # O(e) explores every edge, marks vertices as visited, and reports back. also skips vertices already visited.
            forest.append(tree)

    return forest
```

The most time expensive operations are the for loop that goes over every vertex and the explore recursion which travels through every edge from that starting vertex. Combined, these make for a time complexity of **O(v+e)** where v is the number if vertices and e is the number of edges.

#### Space

#### prepost

```py
def prepost(graph: GRAPH) -> list[dict[str, list[int]]]:
    """
    Return a list of DFS trees.
    Each tree is a dict mapping each node label to a list of [pre, post] order numbers.
    The graph should be searched in order of the keys in the dictionary.
    """
    visited = set()                             # O(v) will grow to hold all vertices
    forest: list[dict[str, list[int]]] = []     # O(v) also will grow for all vertices
    clock = 1

    def explore(u: str, tree: dict[str, list[int]]) -> None:
        nonlocal clock
        visited.add(u)
        tree[u] = [clock, -1]
        clock += 1

        for v in graph.get(u, []):
            if v not in visited:
                explore(v, tree)                # O(density) might affect space based on density of tree for recursion stack memory

        tree[u][1] = clock
        clock += 1

    for u in graph.keys():
        if u not in visited:
            tree: dict[str, list[int]] = {}
            explore(u, tree)                    # O(v) explores every edge, stores vertices and their pre/postorders in a dict
            forest.append(tree)

    return forest
```

Not counting the input, most space expensive operations are storing the visited nodes in a set, and storing the trees in a forest. Combined, these make for a space complexity of **O(v)** where v is the number if vertices.

### Empirical Data

| Density Factor | Size | V      | E       | Time (sec) |
| -------------- | ---- | ------ | ------- | ---------- |
| 0.25           | 10   | 10.0   | 12.8    | 0.0        |
| 0.25           | 50   | 50.0   | 61.6    | 0.0        |
| 0.25           | 100  | 100.0  | 123.5   | 0.0        |
| 0.25           | 500  | 500.0  | 616.1   | 0.0        |
| 0.25           | 1000 | 1000.0 | 1242.3  | 0.0        |
| 0.25           | 2000 | 2000.0 | 2496.5  | 0.001      |
| 0.25           | 4000 | 4000.0 | 4982.6  | 0.001      |
| 0.25           | 8000 | 8000.0 | 9967.0  | 0.003      |
| 0.5            | 10   | 10.0   | 17.7    | 0.0        |
| 0.5            | 50   | 50.0   | 85.2    | 0.0        |
| 0.5            | 100  | 100.0  | 173.1   | 0.0        |
| 0.5            | 500  | 500.0  | 872.2   | 0.0        |
| 0.5            | 1000 | 1000.0 | 1770.4  | 0.0        |
| 0.5            | 2000 | 2000.0 | 3551.4  | 0.001      |
| 0.5            | 4000 | 4000.0 | 7147.2  | 0.002      |
| 0.5            | 8000 | 8000.0 | 14361.9 | 0.003      |
| 1              | 10   | 10.0   | 24.5    | 0.0        |
| 1              | 50   | 50.0   | 134.1   | 0.0        |
| 1              | 100  | 100.0  | 272.5   | 0.0        |
| 1              | 500  | 500.0  | 1429.5  | 0.0        |
| 1              | 1000 | 1000.0 | 2921.5  | 0.0        |
| 1              | 2000 | 2000.0 | 5928.1  | 0.001      |
| 1              | 4000 | 4000.0 | 12010.6 | 0.002      |
| 1              | 8000 | 8000.0 | 24327.1 | 0.004      |
| 2              | 10   | 10.0   | 36.1    | 0.0        |
| 2              | 50   | 50.0   | 239.4   | 0.0        |
| 2              | 100  | 100.0  | 499.2   | 0.0        |
| 2              | 500  | 500.0  | 2710.2  | 0.0        |
| 2              | 1000 | 1000.0 | 5589.5  | 0.001      |
| 2              | 2000 | 2000.0 | 11450.9 | 0.001      |
| 2              | 4000 | 4000.0 | 23462.8 | 0.003      |
| 2              | 8000 | 8000.0 | 47740.4 | 0.004      |
| 3              | 10   | 10.0   | 46.0    | 0.0        |
| 3              | 50   | 50.0   | 356.9   | 0.0        |
| 3              | 100  | 100.0  | 766.3   | 0.0        |
| 3              | 500  | 500.0  | 4321.3  | 0.0        |
| 3              | 1000 | 1000.0 | 8788.2  | 0.002      |
| 3              | 2000 | 2000.0 | 17810.6 | 0.001      |
| 3              | 4000 | 4000.0 | 36212.5 | 0.003      |
| 3              | 8000 | 8000.0 | 73442.4 | 0.005      |

### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: **O(v+e)**
- Measured constant of proportionality for theoretical order: **1.381965691368153e-07**

![theoreticalEmpirical](./_analysis/prepost.svg)

- Empirical order of growth (if different from theoretical): **N/A**

![img](img.png) <- do i need this?

In quite the contrast to our last project, RSA encryption, this prepost function actually lines up almost perfectly with the theoretical analysis I did on it for time complexity. The empirical data and the theoretical prediction are almost completely in sync. I believe this is because we are no longer dealing with bit-level predictions which can be tricky and more machine-dependent.

## Core

### Design Experience

_Fill me in_

### Theoretical Analysis - SCC

#### Time

_Fill me in_

#### Space

_Fill me in_

### Empirical Data

| size  | density factor | V+E | runtime |
| ----- | -------------- | --- | ------- |
| 10    | 0.25           |     |         |
| 20    | 0.25           |     |         |
| 100   | 0.25           |     |         |
| 200   | 0.25           |     |         |
| 1000  | 0.25           |     |         |
| 2000  | 0.25           |     |         |
| 10000 | 0.25           |     |         |
| 10    | 0.5            |     |         |
| 20    | 0.5            |     |         |
| 100   | 0.5            |     |         |
| 200   | 0.5            |     |         |
| 1000  | 0.5            |     |         |
| 2000  | 0.5            |     |         |
| 10000 | 0.5            |     |         |
| 10    | 1              |     |         |
| 20    | 1              |     |         |
| 100   | 1              |     |         |
| 200   | 1              |     |         |
| 1000  | 1              |     |         |
| 2000  | 1              |     |         |
| 10000 | 1              |     |         |
| 10    | 2              |     |         |
| 20    | 2              |     |         |
| 100   | 2              |     |         |
| 200   | 2              |     |         |
| 1000  | 2              |     |         |
| 2000  | 2              |     |         |
| 10000 | 2              |     |         |
| 10    | 3              |     |         |
| 20    | 3              |     |         |
| 100   | 3              |     |         |
| 200   | 3              |     |         |
| 1000  | 3              |     |         |
| 2000  | 3              |     |         |
| 10000 | 3              |     |         |

### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: _copy from section above_
- Measured constant of proportionality for theoretical order:
- Empirical order of growth (if different from theoretical):
- Measured constant of proportionality for empirical order:

![img](img.png)

_Fill me in_

## Stretch 1

### Design Experience

_Fill me in_

### Articulation Points Discussion

_Fill me in_

## Stretch 2

### Design Experience

_Fill me in_

### Dataset Description

_Fill me in_

### Findings Discussion

_Fill me in_

## Project Review

_Fill me in_
