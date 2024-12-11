import heapq
import os
import random
from typing import List, Tuple, Dict, Optional

import matplotlib.pyplot as plt
import networkx as nx

num_of_edges = random.randint(1, 10)

class KomplettGraph:
    def __init__(self, k: int = 10):
        """
        Initialize a KomplettGraph instance, which starts with a complete graph of size k.
        
        Parameters
        ----------
        k : int
            The initial number of vertices in the complete graph. Defaults to 10.
        """
        # Create K_k graph
        self.G: nx.Graph = nx.complete_graph(k)
        
        # Initialize edge heap with (timestamp, edge) tuples
        # The timestamp tracks the insertion order of edges.
        self.edge_heap: List[Tuple[int, Tuple[int, int]]] = [(0, (u, v)) for u, v in self.G.edges()]
        heapq.heapify(self.edge_heap)
        self.current_time: int = len(self.edge_heap)


    def check_planarity(self) -> Tuple[bool, str]:
        """
        Check if the current graph G is planar.
        
        Returns
        -------
        is_planar : bool
            True if the graph is planar, False otherwise.
        info : str
            A string with planarity info, including node and edge counts.
        """
        is_planar = nx.check_planarity(self.G)[0]
        n_nodes = self.G.number_of_nodes()
        n_edges = self.G.number_of_edges()
        info = (f"Planar: {is_planar}\n"
                f"Nodes: {n_nodes}, Edges: {n_edges}")
        return is_planar, info
    

    def chromatic_number(self) -> int:
        """
        Calculate the chromatic number of the graph using a greedy coloring algorithm.
        
        Returns
        -------
        int
            The chromatic number of the current graph.
        """
        coloring = nx.coloring.greedy_color(self.G, strategy="largest_first")
        # The chromatic number is the count of unique colors used
        return max(coloring.values()) + 1 if coloring else 1


    def arboricity(self) -> int:
        """
        Calculate the arboricity of the graph.
        
        Arboricity is defined as the minimum number of forests into which the edges 
        of the graph can be partitioned. This rough calculation uses the maximum 
        edge-density-based heuristic.
        
        Returns
        -------
        int
            The arboricity of the current graph.
        """
        max_density = 0.0
        for component in nx.connected_components(self.G):
            subg = self.G.subgraph(component)
            num_vertices = len(subg)
            num_edges = subg.number_of_edges()
            if num_vertices > 1:
                density = num_edges / (num_vertices - 1)
                max_density = max(max_density, density)
        
        # Arboricity is roughly the ceiling of the maximum density
        return int(max_density)


    @staticmethod
    def thickness_dfs(v: int,
            u: int,
            adj: Dict[int, List[int]],
            NUMBER: List[int],
            tree_arcs: List[Tuple[int, int]],
            fronds: List[Tuple[int, int]],
            numbering_counter: int) -> int:
        """
        Perform DFS on the graph from vertex v, with u as v's parent, 
        to classify edges as tree arcs or fronds.
        
        Parameters
        ----------
        v : int
            Current vertex being explored.
        u : int
            Parent vertex of v in the DFS tree (-1 or None if v is root).
        adj : Dict[int, List[int]]
            Adjacency list representation of the graph.
        NUMBER : List[int]
            Array that stores the DFS number for each vertex (0 if unvisited).
        tree_arcs : List[Tuple[int, int]]
            Collects edges that are identified as tree edges.
        fronds : List[Tuple[int, int]]
            Collects edges that are identified as back edges (fronds).
        numbering_counter : int
            Counter used to assign DFS order numbers.
        
        Returns
        -------
        int
            The updated numbering_counter after processing v.
        """
        numbering_counter += 1
        NUMBER[v] = numbering_counter

        for w in adj[v]:
            if NUMBER[w] == 0:
                # w is a new vertex -> tree arc
                tree_arcs.append((v, w))
                numbering_counter = KomplettGraph.thickness_dfs(w, v, adj, NUMBER, tree_arcs, fronds, numbering_counter)
            elif NUMBER[w] < NUMBER[v] and w != u:
                # (v,w) is a back edge (frond)
                fronds.append((v, w))

        return numbering_counter


    def check_thickness(self) -> int:
        """
        Perform DFS numbering on the current graph and return the highest DFS number assigned.
        
        Returns
        -------
        int
            The highest DFS numbering assigned to any vertex after a full DFS traversal.
        """
        n = self.G.number_of_nodes()
        NUMBER = [0] * n
        tree_arcs = []
        fronds = []
        adj = {node: list(self.G[node]) for node in self.G.nodes()}
        numbering_counter = 0

        # Run DFS from each unvisited node to ensure all nodes are numbered
        for node in range(n):
            if NUMBER[node] == 0:
                numbering_counter = self.thickness_dfs(node, -1, adj, NUMBER, tree_arcs, fronds, numbering_counter)

        return numbering_counter


    def add_new_edges(self, new_node: int, num_edges: int = None) -> None:
        """
        Add edges connecting a newly added node to a specified number of existing nodes.
        
        Parameters
        ----------
        new_node : int
            The index of the new node being added to the graph.
        num_edges : int, optional
            The number of edges to add. If None, adds edges to all existing nodes.
            If greater than the number of existing nodes, connects to all existing nodes.
        """
        existing_nodes = list(range(new_node))
        
        # If num_edges is None or exceeds available nodes, connect to all nodes
        if num_edges is None or num_edges >= len(existing_nodes):
            nodes_to_connect = existing_nodes
        else:
            nodes_to_connect = random.sample(existing_nodes, num_edges)
        
        for existing_node in nodes_to_connect:
            self.G.add_edge(existing_node, new_node)
            # Add new edge to heap with current timestamp
            heapq.heappush(self.edge_heap, (self.current_time, (existing_node, new_node)))
            self.current_time += 1


    def remove_old_edges(self, num_edges_to_remove: int = 1) -> None:
        """
        Remove a specified number of the oldest edges while maintaining a chromatic number of 10.
        Uses a heap structure to ensure that edges are removed in the order they were added.
        
        Parameters
        ----------
        num_edges_to_remove : int
            The number of edges to attempt to remove.
        """
        removed_count = 0
        while self.edge_heap and removed_count < num_edges_to_remove:
            u, v = self.edge_heap.pop()
            # Skip if edge no longer exists
            if not self.G.has_edge(u, v):
                continue
            
            # Tentatively remove the edge
            self.G.remove_edge(u, v)
            removed_count += 1

    def random_edge_removal(self, num_edges_to_remove: int = 1) -> None:
        """
        Randomly attempt to remove a specified number of edges while maintaining a chromatic number of 10.
        If removing an edge changes the chromatic number, revert the removal.
        
        Parameters
        ----------
        num_edges_to_remove : int
            The number of edges to attempt to remove.
        """
        edges = list(self.G.edges())
        random.shuffle(edges)  # Shuffle edges for random removal attempt

        removed_count = 0
        for u, v in edges:
            if removed_count >= num_edges_to_remove:
                break
            self.G.remove_edge(u, v)
            removed_count += 1

    def add_edge_step(self, step: int, chromatic_num_original, removal_policy: str = "old", num_edges = num_of_edges) -> bool:
        """
        Perform a single step of adding a new node and its edges, 
        then remove edges according to the specified removal policy.
        Reverts changes if constraints are violated.
        
        Parameters
        ----------
        step : int
            The current step count.
        removal_policy : str
            The policy for removing edges. Options:
            - "old": Remove oldest edges first.
            - "random": Remove random edges.
        num_edges : int, optional
            The number of edges to add for the new node. If None, adds edges to all existing nodes.
            
        Returns
        -------
        bool
            True if changes were successful, False if changes were reverted
        """
        # Store the current state of the graph
        original_graph = self.G.copy()
        original_heap = self.edge_heap.copy()
        original_time = self.current_time

        # Try making changes
        new_node = self.G.number_of_nodes()
        self.G.add_node(new_node)
        self.add_new_edges(new_node, num_edges)
        
        # Apply removal policy
        if removal_policy == "old":
            self.remove_old_edges(num_edges)
        elif removal_policy == "random":
            self.random_edge_removal(num_edges)

        # Check constraints
        chrom_num = self.chromatic_number()
        arb_num = self.arboricity()
        
        # Revert if constraints are violated
        # if chrom_num != chromatic_num_original:
        #     self.G = original_graph
        #     self.edge_heap = original_heap
        #     self.current_time = original_time
        #     print(f"Chromatic number not {chromatic_num_original} at step {step}")
        if arb_num > 9:
            self.G = original_graph
            self.edge_heap = original_heap
            self.current_time = original_time
            error_message = (f"Arboricity reached 9 at step {step}")
            return False, error_message
        
        return True


    def create_k_plus_edges(self, removal_policy: str = "old") -> None:
        """
        Generate and analyze graphs by iteratively adding nodes and edges
        and then removing edges according to a chosen policy. 
        Collect and display statistics at each step.
        
        Parameters
        ----------
        removal_policy : str
            The policy for removing edges. Options:
            - "old": Remove oldest edges first.
            - "random": Remove random edges.
        """
        i = 0
        graph_data = []
        chromatic_num_original = self.chromatic_number()
        try:
            while True:
                if i > 0:
                    success, error_message = self.add_edge_step(i, chromatic_num_original, removal_policy)
                    if not success:
                        print(error_message)
                        continue
                
                # Check properties
                is_planar, planar_info = self.check_planarity()
                chrom_num = self.chromatic_number()
                arb_num = self.arboricity()

                # Perform DFS numbering after modifications
                thickness = self.check_thickness()
                
                # Store current state
                graph_data.append({
                    'step': i,
                    'chromatic_number': chrom_num,
                    'is_planar': is_planar,
                    'nodes': self.G.number_of_nodes(),
                    'edges': self.G.number_of_edges(),
                    'arboricity': arb_num,
                    'thickness': thickness
                })
                
                # Print current state
                print(f"Step {i}:")
                print(f"  Chromatic Number: {chrom_num}")
                print(f"  Is Planar: {is_planar}")
                print(f"  Arboricity: {arb_num}")
                print(f"  Thickness: {thickness}")
                print("-" * 30)
                
                # Stop conditions

                if chrom_num != chromatic_num_original:
                    print(f"Chromatic number not {chromatic_num_original} at step {i}")
                    break
                if is_planar:
                    print(f"Found planar graph at step {i}")
                    # break
                if arb_num >= 7:
                    print(f"Arboricity reached 7 at step {i}")
                    # break
                
                i += 1

                
        except KeyboardInterrupt:
            print("\nComputation stopped by user")
            
        # Print and save summary table
        self._save_summary(graph_data, removal_policy, i)
        

    def _save_summary(self, graph_data: List[Dict], removal_policy: str, steps: int) -> None:
        """
        Save a summary of the collected graph data to a text file.
        
        Parameters
        ----------
        graph_data : List[Dict]
            The collected statistics for each step.
        removal_policy : str
            The removal policy used ("old" or "random").
        steps : int
            The final number of steps completed.
        """
        summary = "\nSummary of Generated Graphs:\n"
        summary += "-" * 105 + "\n"
        summary += f"{'Step':^10}{'Nodes':^10}{'Edges':^10}{'Chromatic #':^15}{'Arboricity':^15}{'Thickness':^10}{'Is Planar':^15}\n"
        summary += "-" * 105 + "\n"
        
        for data in graph_data:
            row = (f"{data['step']:^10}"
                   f"{data['nodes']:^10}"
                   f"{data['edges']:^10}"
                   f"{data['chromatic_number']:^15}"
                   f"{data['arboricity']:^15}"
                   f"{data['thickness']:^10}"
                   f"{str(data['is_planar']):^15}\n")
            summary += row
            
        summary += "-" * 105 + "\n"
        
        # Print to console
        print(summary)
        
        # Save to file in a specific directory
        save_dir = "results"
        os.makedirs(save_dir, exist_ok=True)  # Create directory if not existing
        
        filename = os.path.join(save_dir, f"graph_summary_{removal_policy}_{steps}_steps.txt")
        with open(filename, 'w') as f:
            f.write(summary)
        print(f"\nSummary saved to {filename}")


if __name__ == "__main__":
    # Example usage:
    k10 = KomplettGraph(19)
    k10.create_k_plus_edges(removal_policy="random")