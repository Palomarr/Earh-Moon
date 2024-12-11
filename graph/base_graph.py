import networkx as nx
from typing import Tuple, List, Dict

class BaseGraph:
    def __init__(self, k: int = 10):
        """Base graph initialization with common graph operations"""
        self.G: nx.Graph = nx.complete_graph(k)

    def check_planarity(self) -> Tuple[bool, str]:
        """Check if the current graph G is planar."""
        is_planar = nx.check_planarity(self.G)[0]
        n_nodes = self.G.number_of_nodes()
        n_edges = self.G.number_of_edges()
        info = (f"Planar: {is_planar}\n"
                f"Nodes: {n_nodes}, Edges: {n_edges}")
        return is_planar, info

    def chromatic_number(self) -> int:
        """Calculate the chromatic number of the graph."""
        coloring = nx.coloring.greedy_color(self.G, strategy="largest_first")
        return max(coloring.values()) + 1 if coloring else 1

    def arboricity(self) -> int:
        """Calculate the arboricity of the graph."""
        max_density = 0.0
        for component in nx.connected_components(self.G):
            subg = self.G.subgraph(component)
            num_vertices = len(subg)
            num_edges = subg.number_of_edges()
            if num_vertices > 1:
                density = num_edges / (num_vertices - 1)
                max_density = max(max_density, density)
        return int(max_density) 