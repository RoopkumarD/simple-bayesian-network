# defining distribution used for each node

import random
from typing import Dict, List, Set


class Discrete_Distribution:
    def __init__(self, discrete_distribution: Dict[str, float]) -> None:
        self.probability = dict()
        self.states = set(discrete_distribution.keys())
        self.conditioned = set()

        for key in discrete_distribution:
            self.probability[(key,)] = discrete_distribution[key]

    # using inverse transform sampling
    def sample(self, parents: List[str]):
        if len(parents) != 0:
            raise Exception(
                "Queried conditional probability over discrete_distribution"
            )

        uniform_random_number = random.uniform(0.0, 1.0)
        state_order = sorted(list(self.states))
        cdf_trailing_value = 0.0
        returning_sample = None

        for state in state_order:
            if (
                self.probability[(state,)] + cdf_trailing_value
            ) >= uniform_random_number:
                returning_sample = state
                break
            cdf_trailing_value += self.probability[(state,)]

        if returning_sample == None:
            raise Exception("sample is not selected")

        return returning_sample

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

    # based on inverse transform sampling
    def sample(self, parents: List[str]):
        for p in parents:
            if p not in self.conditioned:
                raise Exception(
                    f"Given this parent {parents} on this {self.probability}"
                )

        conditioned_table: Dict[str, float] = dict()
        state_order = sorted(list(self.states))
        for state in state_order:
            p = self.get_probability([state] + parents)
            conditioned_table[state] = p

        uniform_random_number = random.uniform(0.0, 1.0)
        cdf_trailing_value = 0.0
        returning_sample = None

        for key in conditioned_table:
            if conditioned_table[key] + cdf_trailing_value >= uniform_random_number:
                returning_sample = key
                break
            cdf_trailing_value += conditioned_table[key]

        if returning_sample == None:
            raise Exception("sample is not selected")

        return returning_sample

    def get_probability(self, query: List[str]):
        temp = self.states.union(self.conditioned)
        for q in query:
            if q not in temp:
                raise Exception(f"Queried {query[0]} on this {self.probability}")

        return self.probability[tuple(sorted(query))]


if __name__ == "__main__":
    pass
