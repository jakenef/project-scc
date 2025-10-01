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
    
    for u in graph.keys():
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
    
    # 1. reverse the graph 
    reverseGraph: GRAPH = {}

    # Initialize all nodes in reverse graph
    for node in graph:
        reverseGraph[node] = []

    # Add reversed edges
    for node in graph:
        for neighbor in graph[node]:
            reverseGraph[neighbor].append(node)

    # 2. run DFS on reversed graph to get postorder numbers
    reverseGraphPostOrderForest = prepost(reverseGraph) 

    # 3. order the list of nodes from the graph by descending postorder
    all_nodes_with_post = []
    for tree in reverseGraphPostOrderForest:
        for node, times in tree.items():
            post_time = times[1]
            all_nodes_with_post.append((node, post_time))

    # Sort by post-order time in descending order
    all_nodes_with_post.sort(key=lambda x: x[1], reverse=True)

    # Extract just the node names
    nodesInPostOrder = [node for node, post_time in all_nodes_with_post]

    originalGraphPostOrder: GRAPH = {v: graph.get(v, []) for v in nodesInPostOrder}
    for v in graph:
        if v not in originalGraphPostOrder:
            originalGraphPostOrder[v] = graph[v]
    
    # 4. run DFS on original graph in the order of the nodes from the postorder list
    unformattedSCCs = prepost(originalGraphPostOrder)
    sccList = []

    for scc in unformattedSCCs:
        sccList.append(set(scc))

    return sccList


def classify_edges(graph: GRAPH, trees: list[dict[str, list[int]]]) -> dict[str, set[tuple[str, str]]]:
    """
    Return a dictionary containing sets of each class of edges
    """

    # 1. Get prepost numbers in a nice format

    prepostForest = trees

    prepostNodes: dict[str, tuple[int, int]] = {}
    for tree in prepostForest:
        for entry in tree.items():
            node = entry[0]
            prepostList = entry[1]
            preNumber = prepostList[0]
            postNumber = prepostList[1]
            prepostNodes[node] = (preNumber, postNumber)

    # 2. Make an edge list

    edgeList: list[tuple[str, str]] = []
    for node in graph:
        for neighbor in graph[node]:
            edgeList.append((node, neighbor))

    # 3. Classify each edge based on rules for prepost numbers

    treeForwardSet: set[tuple[str, str]] = set()
    backSet: set[tuple[str, str]] = set()
    crossSet: set[tuple[str, str]] = set()

    for edge in edgeList:
        fromNode = edge[0]
        toNode = edge[1]
        fromNodePrepost = prepostNodes[fromNode]
        toNodePrepost = prepostNodes[toNode]
        # if fromNode is an ancestor of toNode
        if fromNodePrepost[0] < toNodePrepost[0] and fromNodePrepost[1] > toNodePrepost[1]:
            treeForwardSet.add(edge)
            # if toNode is an ancestor of fromNode
        elif toNodePrepost[0] < fromNodePrepost[0] and toNodePrepost[1] > fromNodePrepost[1]:
            backSet.add(edge)
            # if they are cross
        else:
            crossSet.add(edge)

    classification = {
        # type: ignore
        'tree/forward': treeForwardSet,
        'back': backSet,
        'cross': crossSet
    }

    return classification


