# defining distribution used for each node

from typing import Dict, List, Set


class Discrete_Distribution:
    def __init__(self, discrete_distribution: Dict[str, float]) -> None:
        self.probability = dict()
        self.states = set(discrete_distribution.keys())
        self.conditioned = set()

        for key in discrete_distribution:
            self.probability[(key,)] = discrete_distribution[key]

    def get_probability(self, query: List[str]):
        if len(query) != 1:
            raise Exception(
                "Queried conditional probability over discrete_distribution"
            )
        elif query[0] not in self.states:
            raise Exception(f"Queried {query[0]} on this {self.probability}")

        return self.probability[tuple(query)]


class Conditional_Probability_Table:
    def __init__(self, table: List[List], dependency: List[Set[str]]) -> None:
        self.probability = dict()
        self.states = set(list(zip(*table))[-2])
        self.conditioned = set()

        for d in dependency:
            self.conditioned = self.conditioned.union(d)

        for line in table:
            self.probability[tuple(sorted(line[:-1]))] = float(line[-1])

    def get_probability(self, query: List[str]):
        temp = self.states.union(self.conditioned)
        for q in query:
            if q not in temp:
                raise Exception(f"Queried {query[0]} on this {self.probability}")

        return self.probability[tuple(sorted(query))]


if __name__ == "__main__":
    pass
