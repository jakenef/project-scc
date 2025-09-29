import random
import sys
from time import time

GRAPH = dict[str, list[str]]
sys.setrecursionlimit(10000)


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

        for v in graph.get(u, []):
            if v not in visited:
                explore(v, tree)
        
        tree[u][1] = clock
        clock += 1
    
    for u in sorted(graph.keys()):
        if u not in visited:
            tree: dict[str, list[int]] = {}
            explore(u, tree)
            forest.append(tree)
    
    return forest


def find_sccs(graph: GRAPH) -> list[set[str]]:
    """
    Return a list of the strongly connected components in the graph.
    The list should be returned in order of sink-to-source
    """
    postOrderForest = prepost(graph)

    nodesInPostOrder = [str] # get list of nodes in descending postorder from postOrderForest

    reverseGraph: GRAPH = {}

    for node, edges in graph.items():
        for edge in edges:
            if edge not in reverseGraph:
                reverseGraph[edge] = []
            reverseGraph[edge].append(node)
    
    reverseGraphPostOrder: GRAPH = {} # for v in nodesInPostOrder, reverseGraphPostOrder[v] = reverseGraph.get(v)

    unformattedSCCs = prepost(reverseGraphPostOrder)
    sccList = []

    for scc in unformattedSCCs:
        sccList.append(set(scc))

    return sccList


def classify_edges(graph: GRAPH, trees: list[dict[str, list[int]]]) -> dict[str, set[tuple[str, str]]]:
    """
    Return a dictionary containing sets of each class of edges
    """

    classification = {
        # type: ignore
        'tree/forward': set(),
        'back': set(),
        'cross': set()
    }

    return classification


