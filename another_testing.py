from bayesian_network import *
from probability_distribution import *

buglary = Node(
    name="buglary",
    probability_distribution=Discrete_Distribution(
        {"buglary": 0.03, "no buglary": 0.97}
    ),
)

earthquake = Node(
    name="earthquake",
    probability_distribution=Discrete_Distribution(
        {"earthquake": 0.001, "no earthquake": 0.999}
    ),
)

alarm = Node(
    name="alarm",
    probability_distribution=Conditional_Probability_Table(
        [
            ["buglary", "earthquake", "alarm", 0.98],
            ["buglary", "earthquake", "no alarm", 0.02],
            ["buglary", "no earthquake", "alarm", 0.7],
            ["buglary", "no earthquake", "no alarm", 0.3],
            ["no buglary", "earthquake", "alarm", 0.4],
            ["no buglary", "earthquake", "no alarm", 0.6],
            ["no buglary", "no earthquake", "alarm", 0.01],
            ["no buglary", "no earthquake", "no alarm", 0.99],
        ],
        [buglary.distribution, earthquake.distribution],
    ),
)

call = Node(
    name="call",
    probability_distribution=Conditional_Probability_Table(
        [
            ["alarm", "call", 0.8],
            ["alarm", "no call", 0.2],
            ["no alarm", "call", 0.05],
            ["no alarm", "no call", 0.95],
        ],
        [alarm.distribution],
    ),
)

newscast = Node(
    name="newscast",
    probability_distribution=Conditional_Probability_Table(
        [
            ["earthquake", "newscast", 0.3],
            ["earthquake", "no newscast", 0.7],
            ["no earthquake", "newscast", 0.001],
            ["no earthquake", "no newscast", 0.999],
        ],
        [earthquake.distribution],
    ),
)

model = Bayesian_Network()
model.add_nodes([buglary, earthquake, alarm, call, newscast])

model.add_edge(buglary, alarm)
model.add_edge(earthquake, alarm)
model.add_edge(earthquake, newscast)
model.add_edge(alarm, call)

model.cook()

num = model.probability(["buglary", "call"])
deno = model.probability(["call"])
print(num, deno, num / deno)
# the probability of buglary changes if we know call happened
# whereas i thought they were independent
# this seriously says that i don't know anything about bayesian network and should take a break
# come back and learn bayesian network well before moving forward
