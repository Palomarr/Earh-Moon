import os
import random
from typing import List, Dict
import matplotlib.pyplot as plt
import networkx as nx


from .base_graph import BaseGraph
from .edge_operations import EdgeOperations
from .thickness import ThicknessCalculator
from .utils import save_graph_visualization, store_graph_data, print_current_state, save_summary

# Create directories for saving graphs
SAVE_DIR = "results"
GRAPH_DIR = os.path.join(SAVE_DIR, "graphs")
os.makedirs(GRAPH_DIR, exist_ok=True)

STEP_LIMIT = 10000
RANDOM_LIMIT = 1000

class KomplettGraph(BaseGraph):
    def __init__(self, k: int = 10):
        super().__init__(k)
        self.edge_ops = EdgeOperations()
        self.thickness_calc = ThicknessCalculator()
        # Initialize edge heap
        self.edge_ops.edge_heap = [(0, (u, v)) for u, v in self.G.edges()]
        self.edge_ops.current_time = len(self.edge_ops.edge_heap)


    def add_edge(self, step: int, chromatic_num_original, removal_policy, num_edges_to_add: int = 1, num_edges_to_remove: int = 1):
        """Add edges and apply removal policy with constraint checking"""
        original_graph = self.G.copy()
        original_heap = self.edge_ops.edge_heap.copy()
        original_time = self.edge_ops.current_time

        new_node = self.G.number_of_nodes()
        self.G.add_node(new_node)
        self.edge_ops.add_new_edges(self.G, new_node, num_edges_to_add)
        
        if removal_policy == "old":
            self.edge_ops.remove_old_edges(self.G, num_edges_to_remove)
        elif removal_policy == "random":
            self.edge_ops.random_edge_removal(self.G, num_edges_to_remove)

        chrom_num = self.chromatic_number()
        arb_num = self.arboricity()

        # Revert if constraints are violated
        if chrom_num != chromatic_num_original:
            self.G = original_graph
            self.edge_heap = original_heap
            self.current_time = original_time
            error_message = (f"Chromatic number not {chromatic_num_original} at step {step}")
            return False, error_message
        
        if arb_num > 9:
            self.G = original_graph
            self.edge_heap = original_heap
            self.current_time = original_time
            error_message = (f"Arboricity reached 9 at step {step}")
            return False, error_message
            
        return True, None


    def generator(self, removal_policy: str = "random") -> None:
        """Main graph generation and analysis method trying all combinations of add/remove edges"""

        i = 0
        graph_data = []
        chromatic_num_original = self.chromatic_number()
        previous_edges = set()

        # Create all possible combinations of add/remove
        edge_combinations = [(add, remove) 
                            for add in range(1, RANDOM_LIMIT + 1)
                            for remove in range(1, RANDOM_LIMIT + 1)]
        random.shuffle(edge_combinations)  # Randomize the order
        
        try:
            while i < STEP_LIMIT and edge_combinations:
                if i > 0:
                    num_edges_to_add, num_edges_to_remove = edge_combinations.pop()

                    success, error_message = self.add_edge(i, chromatic_num_original, 
                                                              removal_policy, num_edges_to_add, num_edges_to_remove)
                    if not success:
                        print(f"{error_message} (tried with {num_edges_to_add} edges to add and {num_edges_to_remove} edges to remove)")
                        i += 1
                        continue

                    current_edges = set(self.G.edges())
                    if self.edge_ops._graphs_are_equal(previous_edges, current_edges):
                        print(f"Step {i}: Skipping duplicate graph")
                        continue

                    previous_edges = current_edges
                
                is_planar, planar_info = self.check_planarity()
                chrom_num = self.chromatic_number()
                arb_num = self.arboricity()
                thickness = self.thickness_calc.check_thickness(self.G)
                
                # Store and print current state
                self._store_graph_data(graph_data, i, chrom_num, is_planar, arb_num, thickness)
                self._print_current_state(i, chrom_num, is_planar, arb_num, thickness)
                
                # Save visualization for valid graphs
                self._save_graph_visualization(i, GRAPH_DIR)
                
                if chrom_num != chromatic_num_original:
                    print(f"Chromatic number not {chromatic_num_original} at step {i}")
                    break
                if is_planar:
                    print(f"Found planar graph at step {i}")
                if arb_num >= 7:
                    print(f"Arboricity reached 7 at step {i}")
                
                i += 1
                
        except KeyboardInterrupt:
            print("\nComputation stopped by user")
            
        self._save_summary(graph_data, removal_policy, i)
        print(f"Remaining unused combinations: {len(edge_combinations)}")


    def _save_graph_visualization(self, step: int, graph_dir: str) -> None:
        save_graph_visualization(step, graph_dir, self.G)

    def _store_graph_data(self, graph_data, step, chrom_num, is_planar, arb_num, thickness):
        store_graph_data(graph_data, step, self.G, chrom_num, is_planar, arb_num, thickness)

    def _print_current_state(self, step, chrom_num, is_planar, arb_num, thickness):
        print_current_state(step, chrom_num, is_planar, arb_num, thickness)

    def _save_summary(self, graph_data, removal_policy, steps):
        save_summary(graph_data, removal_policy, steps)

