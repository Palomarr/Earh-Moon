import networkx as nx
import matplotlib.pyplot as plt
import heapq
import random
import os

class K10Graph:
    def __init__(self, k=10):
        # Create K_10 graph
        self.G = nx.complete_graph(k)
        # Initialize edge heap with (timestamp, edge) tuples
        self.edge_heap = [(0, (u, v)) for u, v in self.G.edges()]
        heapq.heapify(self.edge_heap)
        self.current_time = len(self.edge_heap)
    
    def check_planarity(self):
        """Check if graph is planar and return result with explanation"""
        is_planar = nx.check_planarity(self.G)[0]
        n_nodes = self.G.number_of_nodes()
        n_edges = self.G.number_of_edges()
        return (is_planar, 
                f"Planar: {is_planar}\n"
                f"Nodes: {n_nodes}, Edges: {n_edges}")
    
    def add_new_edges(self, new_node):
        """Add edges connecting new node to all existing nodes"""
        # Connect the new node to all existing nodes
        for existing_node in range(new_node):
            self.G.add_edge(existing_node, new_node)
            # Add new edge to heap with current timestamp
            heapq.heappush(self.edge_heap, (self.current_time, (existing_node, new_node)))
            self.current_time += 1

    def remove_old_edges(self):
        """Remove oldest edges while maintaining chromatic number of 10"""
        while self.edge_heap:
            # Get oldest edge but don't remove it yet
            oldest_time, (u, v) = heapq.heappop(self.edge_heap)
            
            # Skip if edge no longer exists (already removed)
            if not self.G.has_edge(u, v):
                continue
            
            # Try removing the edge
            self.G.remove_edge(u, v)
            if self.chromatic_number() != 10:  # If removing edge changes chromatic number
                self.G.add_edge(u, v)  # Put it back
                heapq.heappush(self.edge_heap, (oldest_time, (u, v)))  # Put back in heap
                break

    def random_edge_removal(self):
        """Random Edge Removal Algorithm"""
        edges = list(self.G.edges())
        random.shuffle(edges)  # Shuffle edges randomly

        for u, v in edges:
            # Try removing the edge
            self.G.remove_edge(u, v)
            if self.chromatic_number() != 10:  # If removing edge changes chromatic number
                self.G.add_edge(u, v)  # Put it back
    
    def add_edge_step(self, step, removal_policy="old"):
        """Add a new node and apply the selected edge removal policy"""
        # Add a new node
        new_node = self.G.number_of_nodes()
        self.G.add_node(new_node)
        
        # Add new edges
        self.add_new_edges(new_node)
        
        # Apply removal policy
        if removal_policy == "old":
            self.remove_old_edges()
        elif removal_policy == "random":
            self.random_edge_removal()
    
    def chromatic_number(self):
        """
        Calculates the chromatic number of the graph using the greedy coloring algorithm.
        """
        # Use the greedy coloring algorithm to color the graph
        coloring = nx.coloring.greedy_color(self.G, strategy="largest_first")
        
        # The chromatic number is the number of unique colors used
        chromatic_num = max(coloring.values()) + 1
        return chromatic_num
    
    def arboricity(self):
        """
        Calculate the arboricity of the graph using the edge density formula.
        """
        max_density = 0
        for subgraph in nx.connected_components(self.G):
            subg = self.G.subgraph(subgraph)
            # Compute the number of vertices and edges for the subgraph
            num_vertices = len(subg)
            num_edges = subg.number_of_edges()
            
            # Avoid division by zero for single-vertex subgraphs
            if num_vertices > 1:
                density = num_edges / (num_vertices - 1)
                max_density = max(max_density, density)
        
        # Arboricity is the ceiling of the maximum density
        return int(max_density)
            
    def create_k10_plus_edges(self, removal_policy="old"):
        """Generate graph, adding and removing edges, using the selected policy"""
        # Initialize step counter and data storage
        i = 0
        graph_data = []
        
        try:
            while True:
                if i > 0:
                    self.add_edge_step(i, removal_policy)
                
                # Check planarity, chromatic number, and arboricity
                is_planar, planar_info = self.check_planarity()
                chrom_num = self.chromatic_number()
                arb_num = self.arboricity()
                
                # Store data
                graph_data.append({
                    'step': i,
                    'chromatic_number': chrom_num,
                    'is_planar': is_planar,
                    'nodes': self.G.number_of_nodes(),
                    'edges': self.G.number_of_edges(),
                    'arboricity': arb_num
                })
                
                # Print current state
                print(f"Step {i}:")
                print(f"Chromatic Number: {chrom_num}")
                print(f"Is Planar: {is_planar}")
                print(f"Arboricity: {arb_num}")
                print("-" * 30)
                
                # Stop conditions
                if is_planar:
                    print(f"Found planar graph at step {i}")
                    break
                if arb_num >= 7:
                    print(f"Arboricity reached 7 at step {i}")
                    break
                    
                i += 1
                
        except KeyboardInterrupt:
            print("\nComputation stopped by user")
            
        # Print and save summary table
        summary = "\nSummary of Generated Graphs:\n"
        summary += "-" * 85 + "\n"
        summary += f"{'Step':^10}{'Nodes':^10}{'Edges':^10}{'Chromatic #':^15}{'Arboricity':^15}{'Is Planar':^15}\n"
        summary += "-" * 85 + "\n"
        
        for data in graph_data:
            row = f"{data['step']:^10}{data['nodes']:^10}{data['edges']:^10}" \
                  f"{data['chromatic_number']:^15}{data['arboricity']:^15}{str(data['is_planar']):^15}\n"
            summary += row
            
        summary += "-" * 85 + "\n"
        
        # Print to console
        print(summary)
        
        # Save to file in specific directory
        save_dir = "results"
        os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist
        
        filename = os.path.join(save_dir, f"graph_summary_{removal_policy}_{i}_steps.txt")
        with open(filename, 'w') as f:
            f.write(summary)
        print(f"\nSummary saved to {filename}")

# Run the visualization
if __name__ == "__main__":
    k10 = K10Graph()
    # Use "random" or "old" as the removal policy
    k10.create_k10_plus_edges(removal_policy="old")