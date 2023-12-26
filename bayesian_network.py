# defined Node and Bayesian_Network Class

from functools import cache
from typing import Dict, List, Tuple

from utils import Queue


class Node:
    def __init__(self, name, probability_distribution) -> None:
        self.name = name
        self.probability_distribution = probability_distribution
        self.distribution = probability_distribution.states

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and other.name == self.name

    def __repr__(self) -> str:
        return f"{self.name}"

    def sample(self, parents: List[str]):
        return self.probability_distribution.sample(parents)

    def get_probability(self, query: List[str]):
        return self.probability_distribution.get_probability(query)

    def is_node_conditioned(self, node_state: str):
        return node_state in self.probability_distribution.conditioned


class Bayesian_Network:
    def __init__(self) -> None:
        self.nodes: List[Node] = list()
        self.edges = dict()
        self.name_to_node: Dict[str, Node] = dict()
        self.sorted_list: List[str] = list()

    def add_nodes(self, nodes: List[Node]) -> None:
        self.nodes += nodes
        for node in nodes:
            self.name_to_node[node.name] = node

    def add_edge(self, parent_node: Node, child_node: Node) -> None:
        if child_node.name not in self.edges:
            self.edges[child_node.name] = []

        self.edges[child_node.name].append(parent_node.name)

    # return list sorted in order of sorted_list
    def find_hidden_variables(self, queried_list: List[str]):
        sorted_acc_to_list = list()
        temp = set(queried_list)

        for node in self.sorted_list:
            intersect = temp.intersection(self.name_to_node[node].distribution)
            if len(intersect) == 0:
                sorted_acc_to_list.append(None)
            else:
                sorted_acc_to_list.append(list(intersect)[0])

        return sorted_acc_to_list

    # in this function, i break everything into piece using recursion and later return
    @cache
    def get_all_possible_states(
        self,
        sorted_acc_to_list: Tuple[str, ...],
        conditioned_list: Tuple[str, ...] | Tuple[()] = (),
        index: int = 0,
    ):
        if len(sorted_acc_to_list) == 0:
            return 1

        current = sorted_acc_to_list[0]

        current_conditioned = [
            c
            for c in conditioned_list
            if self.name_to_node[self.sorted_list[index]].is_node_conditioned(c)
        ]

        total = 0

        if current == None:
            for state in self.name_to_node[self.sorted_list[index]].distribution:
                new_conditioned_list: List[str] = []
                temp = conditioned_list + (state,)
                for i in range(index, len(self.sorted_list)):
                    for c in temp:
                        if (
                            self.name_to_node[self.sorted_list[i]].is_node_conditioned(
                                c
                            )
                            == True
                        ) and c not in new_conditioned_list:
                            new_conditioned_list.append(c)

                total += self.name_to_node[self.sorted_list[index]].get_probability(
                    [state] + current_conditioned
                ) * self.get_all_possible_states(
                    sorted_acc_to_list[1:], tuple(new_conditioned_list), index + 1
                )
        else:
            new_conditioned_list: List[str] = []

            temp = conditioned_list + (current,)
            for i in range(index, len(self.sorted_list)):
                for c in temp:
                    if (
                        self.name_to_node[self.sorted_list[i]].is_node_conditioned(c)
                        == True
                    ) and c not in new_conditioned_list:
                        new_conditioned_list.append(c)

            total += self.name_to_node[self.sorted_list[index]].get_probability(
                [current] + current_conditioned
            ) * self.get_all_possible_states(
                sorted_acc_to_list[1:], tuple(new_conditioned_list), index + 1
            )

        return total

    # calculating the probability of query
    def probability(self, query: List[str]):
        if len(self.sorted_list) == 0:
            raise Exception("Cook the network with cook method")

        sorted_acc_to_list: List[str] = self.find_hidden_variables(query)
        total = self.get_all_possible_states(tuple(sorted_acc_to_list))
        return total

    def generate_sample(self):
        s = set()
        parents = list()
        for node in self.sorted_list:
            current_conditioned = [
                c for c in parents if self.name_to_node[node].is_node_conditioned(c)
            ]
            g = self.name_to_node[node].sample(current_conditioned)
            s.add(g)
            parents.append(g)

        return s

    def generate_likelihood_sample(self, evidence_variable_with_state: Dict[str, str]):
        s = set()
        parents = list()
        weight_of_sample = 1.0
        for node in self.sorted_list:
            current_conditioned = [
                c for c in parents if self.name_to_node[node].is_node_conditioned(c)
            ]

            if node in evidence_variable_with_state:
                s.add(evidence_variable_with_state[node])
                parents.append(evidence_variable_with_state[node])
                weight_of_sample *= self.name_to_node[node].get_probability(
                    [evidence_variable_with_state[node]] + current_conditioned
                )
            else:
                g = self.name_to_node[node].sample(current_conditioned)
                s.add(g)
                parents.append(g)

        return s, weight_of_sample

    # doing topological sorting for defining conditional dependency later on
    def cook(self):
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
                if degrees[i] == 0 and i not in already_checked and i not in q.queue:
                    q.add(i)

        self.sorted_list = sorted_list
        return
