#!/usr/bin/env python3

import csv
from scc import GRAPH, find_sccs, prepost, classify_edges

def load_wiki_graph(file_path: str, vote_filter=None) -> GRAPH:
    """
    Load the Wiki RfA dataset and convert it to GRAPH format.
    
    Args:
        file_path: Path to the wikiRfA.csv file
        vote_filter: Optional filter for VOTE column (1 for positive votes, -1 for negative, 0 for neutral)
    
    Returns:
        GRAPH: Dictionary mapping source nodes to lists of target nodes
    """
    graph: GRAPH = {}
    
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            source = row['SOURCE']
            target = row['TARGET']
            vote = int(row['VOTE'])
            
            # Apply vote filter if specified
            if vote_filter is not None and vote != vote_filter:
                continue
            
            # Initialize source node if not exists
            if source not in graph:
                graph[source] = []
            
            # Add edge from source to target
            if target not in graph[source]:
                graph[source].append(target)
            
            # Ensure target node exists (even if it has no outgoing edges)
            if target not in graph:
                graph[target] = []
    
    return graph

def get_sample_subgraph(graph: GRAPH, max_size: int = 100) -> GRAPH:
    """Get a smaller connected subgraph for detailed analysis"""
    if len(graph) <= max_size:
        return graph
        
    subgraph: GRAPH = {}
    visited = set()
    start_nodes = list(graph.keys())[:3]  # Start from first few nodes
    queue = start_nodes.copy()
    
    while queue and len(subgraph) < max_size:
        node = queue.pop(0)
        if node in visited:
            continue
            
        visited.add(node)
        if node in graph:
            subgraph[node] = graph[node].copy()
            # Add neighbors to queue
            for neighbor in graph[node]:
                if neighbor not in visited and len(subgraph) < max_size:
                    queue.append(neighbor)
    
    return subgraph

def analyze_wiki_with_scc():
    """Analyze the Wiki RfA graph using the original SCC functions"""
    dataset_path = "/Users/jakenef/.cache/kagglehub/datasets/boneacrabonjac/wiki-rfa/versions/1/wikiRfA.csv"
    
    print("🔍 Loading Wiki RfA dataset using your SCC functions...")
    print("=" * 60)
    
    # Load different versions of the graph
    print("📊 Loading different graph variants...")
    all_votes_graph = load_wiki_graph(dataset_path)
    positive_votes_graph = load_wiki_graph(dataset_path, vote_filter=1)
    negative_votes_graph = load_wiki_graph(dataset_path, vote_filter=-1)
    
    print(f"✅ All votes graph: {len(all_votes_graph)} nodes")
    print(f"✅ Positive votes graph: {len(positive_votes_graph)} nodes") 
    print(f"✅ Negative votes graph: {len(negative_votes_graph)} nodes")
    
    # Create a smaller sample for detailed analysis
    print(f"\n🔬 Creating sample subgraph for detailed analysis...")
    sample_graph = get_sample_subgraph(all_votes_graph, max_size=50)
    
    # Analyze each graph
    graphs_to_analyze = [
        ("📋 Sample Graph (Detailed)", sample_graph, True),
        ("🌐 All Votes Graph", all_votes_graph, False),
        ("👍 Positive Votes Graph", positive_votes_graph, False),
        ("👎 Negative Votes Graph", negative_votes_graph, False)
    ]
    
    for graph_name, graph, do_detailed in graphs_to_analyze:
        print(f"\n{'='*60}")
        print(f"{graph_name}")
        print(f"{'='*60}")
        
        if len(graph) == 0:
            print("❌ Empty graph, skipping...")
            continue
            
        # Basic stats
        total_edges = sum(len(neighbors) for neighbors in graph.values())
        print(f"📈 Nodes: {len(graph):,}")
        print(f"🔗 Edges: {total_edges:,}")
        print(f"📊 Avg degree: {total_edges/len(graph):.2f}")
        
        # Find SCCs using your function
        print(f"\n🔍 Finding strongly connected components...")
        sccs = find_sccs(graph)
        print(f"🎯 Number of SCCs: {len(sccs)}")
        
        # Analyze SCC sizes
        scc_sizes = [(len(scc), scc) for scc in sccs]
        scc_sizes.sort(reverse=True)
        
        print(f"\n🏆 Top 5 largest SCCs:")
        for i, (size, scc) in enumerate(scc_sizes[:5]):
            if size > 1:  # Only show non-trivial SCCs
                print(f"  🔸 SCC {i+1}: {size} nodes")
                if size <= 10:  # Show members if small enough
                    members = sorted(list(scc))
                    print(f"    👥 Members: {members}")
                else:
                    sample = sorted(list(scc))[:5]
                    print(f"    👥 Sample: {sample}...")
            else:
                break
        
        # Count trivial vs non-trivial SCCs
        trivial_sccs = sum(1 for scc in sccs if len(scc) == 1)
        non_trivial_sccs = len(sccs) - trivial_sccs
        print(f"\n📊 SCC Summary:")
        print(f"  • Trivial SCCs (size 1): {trivial_sccs}")
        print(f"  • Non-trivial SCCs (size > 1): {non_trivial_sccs}")
        
        # Detailed analysis for small graphs
        if do_detailed and len(graph) <= 100:
            print(f"\n🔬 Detailed Analysis:")
            
            # DFS Trees
            trees = prepost(graph)
            print(f"🌳 DFS trees: {len(trees)}")
            
            # Show some prepost numbers
            print(f"⏱️  Sample prepost numbers:")
            count = 0
            for tree in trees[:2]:  # First 2 trees
                for node, times in list(tree.items())[:5]:  # First 5 nodes per tree
                    print(f"    {node}: pre={times[0]}, post={times[1]}")
                    count += 1
                if count >= 10:
                    break
            
            # Edge Classification
            print(f"\n🏷️  Classifying edges...")
            edge_classification = classify_edges(graph, trees)
            
            tree_forward = len(edge_classification['tree/forward'])
            back = len(edge_classification['back'])
            cross = len(edge_classification['cross'])
            total_classified = tree_forward + back + cross
            
            print(f"  🔸 Tree/Forward edges: {tree_forward}")
            print(f"  🔙 Back edges: {back}")
            print(f"  ↔️  Cross edges: {cross}")
            print(f"  📊 Total classified: {total_classified}")
            
            if total_classified > 0:
                print(f"  📈 Edge distribution:")
                print(f"    • Tree/Forward: {tree_forward/total_classified*100:.1f}%")
                print(f"    • Back: {back/total_classified*100:.1f}%") 
                print(f"    • Cross: {cross/total_classified*100:.1f}%")
        
        elif len(graph) > 100:
            print(f"⚠️  Skipping detailed analysis (graph too large: {len(graph)} nodes)")

if __name__ == "__main__":
    analyze_wiki_with_scc()