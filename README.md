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
- **Visualization**: Displays graph structures and their properties at each step.

## Prerequisites

Ensure you have the following installed:
- Python 3.7 or higher
- Required Python packages:
  ```bash
  pip install networkx matplotlib