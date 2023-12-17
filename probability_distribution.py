from typing import Dict, List


class Discrete_Distribution:
    def __init__(self, discrete_distribution: Dict[str, float]) -> None:
        self.table = discrete_distribution
        self.distribution = set(discrete_distribution.keys())


class Conditional_Probability_Table:
    def __init__(self, table: List[List], conditioned_upon) -> None:
        self.table = table
        self.conditioned_upon = conditioned_upon


if __name__ == "__main__":
    pass
