from typing import List, Tuple, Dict

class ThicknessCalculator:
    @staticmethod
    def thickness_dfs(v: int,
            u: int,
            adj: Dict[int, List[int]],
            NUMBER: List[int],
            tree_arcs: List[Tuple[int, int]],
            fronds: List[Tuple[int, int]],
            numbering_counter: int) -> int:
        """DFS implementation for thickness calculation"""
        numbering_counter += 1
        NUMBER[v] = numbering_counter

        for w in adj[v]:
            if NUMBER[w] == 0:
                tree_arcs.append((v, w))
                numbering_counter = ThicknessCalculator.thickness_dfs(
                    w, v, adj, NUMBER, tree_arcs, fronds, numbering_counter)
            elif NUMBER[w] < NUMBER[v] and w != u:
                fronds.append((v, w))

        return numbering_counter

    def check_thickness(self, G) -> int:
        """Calculate thickness using DFS numbering"""
        n = G.number_of_nodes()
        NUMBER = [0] * n
        tree_arcs = []
        fronds = []
        adj = {node: list(G[node]) for node in G.nodes()}
        numbering_counter = 0

        for node in range(n):
            if NUMBER[node] == 0:
                numbering_counter = self.thickness_dfs(
                    node, -1, adj, NUMBER, tree_arcs, fronds, numbering_counter)

        return numbering_counter 