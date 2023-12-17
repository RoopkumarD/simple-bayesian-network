from typing import List


class Node:
    def __init__(self, name, probability_distribution) -> None:
        self.name = name
        self.probability_distribution = probability_distribution

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and other.name == self.name


class Bayesian_Network:
    def __init__(self) -> None:
        self.nodes = list()
        self.edges = dict()
        self.name_to_node = dict()

    def add_nodes(self, nodes: List[Node]) -> None:
        self.nodes += nodes
        for node in nodes:
            self.name_to_node[node.name] = node

    def add_edge(self, parent_node: Node, child_node: Node) -> None:
        if parent_node not in self.edges:
            self.edges[parent_node.name] = []

        self.edges[parent_node.name].append(child_node.name)

    def cook(self):
        # sort the node in [node1.name, node2.name]
        # then for later retrieval when calculating probability
        # will use name_to_node dictionary to get the node
        pass
