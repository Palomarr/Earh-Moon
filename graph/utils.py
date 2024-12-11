import matplotlib.pyplot as plt
import networkx as nx
import os
from typing import List, Dict


def save_graph_visualization(step: int, graph_dir: str, G) -> None:
    """Save a visualization of the current graph state"""
    plt.figure(figsize=(10, 10))
    
    # Create the layout
    pos = nx.spring_layout(G)
    
    # Draw the graph
    nx.draw(G, pos, 
            node_color='lightblue',
            node_size=500,
            with_labels=True,
            font_size=10,
            font_weight='bold',
            edge_color='gray',
            width=1,
            alpha=0.7)
    
    # Add title
    plt.title(f'Graph at Step {step}\nNodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}')
    
    # Save the figure
    filename = os.path.join(graph_dir, f'graph_step_{step}.png')
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()  # Close the figure to free memory


def store_graph_data(graph_data: List[Dict], step: int, G, chrom_num: int, 
                    is_planar: bool, arb_num: int, thickness: int) -> None:
    """Store graph data for the current step"""
    graph_data.append({
        'step': step,
        'chromatic_number': chrom_num,
        'is_planar': is_planar,
        'nodes': G.number_of_nodes(),
        'edges': G.number_of_edges(),
        'arboricity': arb_num,
        'thickness': thickness
    })


def print_current_state(step: int, chrom_num: int, is_planar: bool, 
                       arb_num: int, thickness: int) -> None:
    """Print the current state of the graph"""
    print(f"Step {step}:")
    print(f"  Chromatic Number: {chrom_num}")
    print(f"  Is Planar: {is_planar}")
    print(f"  Arboricity: {arb_num}")
    print(f"  Thickness: {thickness}")
    print("-" * 30)


def save_summary(graph_data: List[Dict], removal_policy: str, steps: int) -> None:
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
