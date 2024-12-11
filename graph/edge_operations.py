import heapq
import random
from typing import List, Tuple

class EdgeOperations:
    def __init__(self):
        self.edge_heap: List[Tuple[int, Tuple[int, int]]] = []
        self.current_time: int = 0

    def add_new_edges(self, G, new_node: int, num_edges: int = 1) -> None:
        """Add edges connecting a new node to existing nodes"""
        existing_nodes = list(range(new_node))
        
        if num_edges is None or num_edges >= len(existing_nodes):
            nodes_to_connect = existing_nodes
        else:
            nodes_to_connect = random.sample(existing_nodes, num_edges)
        
        for existing_node in nodes_to_connect:
            G.add_edge(existing_node, new_node)
            heapq.heappush(self.edge_heap, 
                          (self.current_time, (existing_node, new_node)))
            self.current_time += 1

    def remove_old_edges(self, G, num_edges_to_remove: int = 1) -> None:
        """Remove oldest edges from the graph"""
        removed_count = 0
        while self.edge_heap and removed_count < num_edges_to_remove:
            _, (u, v) = heapq.heappop(self.edge_heap)
            if not G.has_edge(u, v):
                continue
            G.remove_edge(u, v)
            removed_count += 1

    def random_edge_removal(self, G, num_edges_to_remove: int = 1) -> None:
        """Remove random edges from the graph"""
        edges = list(G.edges())
        random.shuffle(edges)

        removed_count = 0
        for u, v in edges:
            if removed_count >= num_edges_to_remove:
                break
            G.remove_edge(u, v)
            removed_count += 1 
    
    def _graphs_are_equal(self, previous_edges, current_edges) -> bool:
        """
        Compare two graphs based on their edge sets
        
        Parameters:
        -----------
        previous_edges : set
            Edge set of the previous graph
        current_edges : set
            Edge set of the current graph
            
        Returns:
        --------
        bool
            True if graphs are equivalent, False otherwise
        """
        return previous_edges == current_edges