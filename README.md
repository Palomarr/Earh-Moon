# Earth-Moon Graph Partitioning Project

This repository contains the implementation of algorithms and tools for partitioning graphs while maintaining properties such as planarity, chromatic number, and arboricity. The project focuses on analyzing and manipulating complete graphs (e.g., \(K_{10}\)) to explore their structural characteristics under various constraints.

## Features

- **Graph Generation**: Automatically creates complete graphs (e.g., \(K_{10}\)).
- **Planarity Testing**: Uses Hopcroft-Tarjan algorithm to check graph planarity.
- **Edge Removal Policies**:
  - **Random Edge Removal**: Randomly partitions graph edges while maintaining specific properties.
  - **Oldest Edge Removal**: Removes edges based on age while preserving key graph properties.
- **Graph Analysis**:
  - Computes the **chromatic number** of the graph.
  - Calculates **arboricity** based on edge density.
  - Computes **thickness** using a depth-first search (DFS) approach.
- **Visualization**: Displays graph structures and their properties at each step.

## Prerequisites

- Python 3.7 or higher
- Required Python packages:
  ```bash
  pip install networkx matplotlib
  ```

## Usage

To run the graph partitioning algorithm, execute the `main.py` script. This will generate and analyze a complete graph with the specified number of nodes.

```bash
python main.py
```

## Configuration

- **Graph Size**: The number of nodes in the complete graph can be adjusted in `main.py` by changing the parameter passed to `KomplettGraph`.
- **Edge Operations**: Customize edge addition and removal policies in `graph/edge_operations.py`.
- **Step Limits**: Modify `STEP_LIMIT` and `RANDOM_LIMIT` in `graph/komplett_graph.py` to control the number of iterations and randomness.

## Output

Results, including visualizations and summaries, are saved in the `results/graphs` directory. The summary includes details about the chromatic number, planarity, arboricity, and thickness of the graphs at each step.
