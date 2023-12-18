from typing import List

from utils import Queue


class Node:
    def __init__(self, name, probability_distribution) -> None:
        self.name = name
        self.probability_distribution = probability_distribution
        self.distribution = probability_distribution.states

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and other.name == self.name

    def get_probability(self, query: List[str]):
        return self.probability_distribution.get_probability(query)


class Bayesian_Network:
    def __init__(self) -> None:
        self.nodes: List[Node] = list()
        self.edges = dict()
        self.name_to_node = dict()
        self.sorted_list = list()

    def add_nodes(self, nodes: List[Node]) -> None:
        self.nodes += nodes
        for node in nodes:
            self.name_to_node[node.name] = node

    def add_edge(self, parent_node: Node, child_node: Node) -> None:
        if child_node.name not in self.edges:
            self.edges[child_node.name] = []

        self.edges[child_node.name].append(parent_node.name)

    def find_hidden_variables(self, queried_list: List[str]):
        hidden = list()
        non_hidden_mapped_to_query = dict()
        temp = set(queried_list)

        for node in self.nodes:
            intersect = temp.intersection(node.distribution)
            if len(intersect) == 0:
                hidden.append(node.name)
            else:
                non_hidden_mapped_to_query[node.name] = list(intersect)[0]

        return hidden, non_hidden_mapped_to_query

    def get_all_possible_states(self, queried_list: List[str]):
        hidden, non_hidden_mapped_to_query = self.find_hidden_variables(queried_list)

        # return all possible states

    def probability(self, query: List[str]):
        if len(self.sorted_list) == 0:
            raise Exception("Cook the network with cook method")

        # get all possible states
        # then loop through all and find each probability
        pass

    def cook(self):
        # doing topological sorting
        degrees = [0] * len(self.nodes)
        node_to_index = dict()
        sorted_list = list()

        num_nodes = len(self.nodes)
        for n in range(num_nodes):
            node_to_index[self.nodes[n].name] = n

        for edge in self.edges:
            degrees[node_to_index[edge]] += len(self.edges[edge])

        q = Queue()
        already_checked = set()

        for i in range(num_nodes):
            if degrees[i] == 0:
                q.add(i)

        while q.empty() == False:
            elem = q.get()
            already_checked.add(elem)
            sorted_list.append(self.nodes[elem].name)

            for n in range(num_nodes):
                if (
                    self.nodes[n].name in self.edges
                    and self.nodes[elem].name in self.edges[self.nodes[n].name]
                ):
                    degrees[n] -= 1

            for i in range(num_nodes):
                if degrees[i] == 0 and i not in already_checked:
                    q.add(i)

        self.sorted_list = sorted_list
        return
