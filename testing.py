# python script used for testing the code

from bayesian_network import *
from probability_distribution import *

# Rain node has no parents
rain = Node(
    name="rain",
    probability_distribution=Discrete_Distribution(
        {"none": 0.7, "light": 0.2, "heavy": 0.1}
    ),
)

# Track maintenance node is conditional on rain
maintenance = Node(
    "maintenance",
    Conditional_Probability_Table(
        [
            ["none", "yes", 0.4],
            ["none", "no", 0.6],
            ["light", "yes", 0.2],
            ["light", "no", 0.8],
            ["heavy", "yes", 0.1],
            ["heavy", "no", 0.9],
        ],
        [rain.distribution],
    ),
)

# Train node is conditional on rain and maintenance
train = Node(
    "train",
    Conditional_Probability_Table(
        [
            ["none", "yes", "on time", 0.8],
            ["none", "yes", "delayed", 0.2],
            ["none", "no", "on time", 0.9],
            ["none", "no", "delayed", 0.1],
            ["light", "yes", "on time", 0.6],
            ["light", "yes", "delayed", 0.4],
            ["light", "no", "on time", 0.7],
            ["light", "no", "delayed", 0.3],
            ["heavy", "yes", "on time", 0.4],
            ["heavy", "yes", "delayed", 0.6],
            ["heavy", "no", "on time", 0.5],
            ["heavy", "no", "delayed", 0.5],
        ],
        [rain.distribution, maintenance.distribution],
    ),
)

# Appointment node is conditional on train
appointment = Node(
    "appointment",
    Conditional_Probability_Table(
        [
            ["on time", "attend", 0.9],
            ["on time", "miss", 0.1],
            ["delayed", "attend", 0.6],
            ["delayed", "miss", 0.4],
        ],
        [train.distribution],
    ),
)

# Create a Bayesian Network and add states
model = Bayesian_Network()
model.add_nodes([rain, maintenance, train, appointment])

# Add edges connecting nodes
model.add_edge(rain, maintenance)
model.add_edge(rain, train)
model.add_edge(maintenance, train)
model.add_edge(train, appointment)

# Finalize model
model.cook()

N = 1000
query = ["attend"]
times_occured = 0

for i in range(N):
    if len(set(query).intersection(model.generate_sample())) == len(query):
        times_occured += 1

print(times_occured / N)

print(model.probability(query))
