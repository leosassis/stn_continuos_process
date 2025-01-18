from pyomo.environ import *
from itertools import product

# Create a model
model = ConcreteModel()

# Define sets
model.Units = Set(initialize=['UA1', 'UA2', 'UA3'])  # Units
#model.Tasks = Set(initialize=['Task1', 'Task2'])      # Tasks
model.Tasks = Set(initialize=['Task1', 'Task2', 'Task3'])      # Tasks

# Units that can execute each task
#units_for_task = {'Task1': ['UA1', 'UA2'], 'Task2': ['UA2', 'UA3']}
units_for_task = {'Task1': ['UA1'], 'Task2': ['UA2'], 'Task3': ['UA3']}
model.UnitsForTask = Set(model.Tasks, initialize=units_for_task)

# Parameters
#epsilon_max = {'UA1': 2, 'UA2': 3, 'UA3': 1}  # Maximum batches for each unit
epsilon_max = {'UA1': 1, 'UA2': 1, 'UA3': 1}  # Maximum batches for each unit
model.epsilon_max = Param(model.Units, initialize=epsilon_max)

min_capacity = {'UA1': 5, 'UA2': 10, 'UA3': 15}  # Minimum capacity for each unit per batch
max_capacity = {'UA1': 8, 'UA2': 12, 'UA3': 20}  # Maximum capacity for each unit per batch
model.MinCapacity = Param(model.Units, initialize=min_capacity)
model.MaxCapacity = Param(model.Units, initialize=max_capacity)

# Calculate batch combinations and capacities
batch_combinations = {}
combined_capacities = {}

for task in model.Tasks:
    unit_subset = units_for_task[task]
    print(unit_subset)
    # Generate all batch combinations for the subset of units
    max_batches = [range(model.epsilon_max[unit] + 1) for unit in unit_subset]
    combinations = list(product(*max_batches))
    batch_combinations[task] = combinations
    
    # Calculate combined capacities for each combination
    combined_capacities[task] = {
        combo: {
            'min_capacity': sum(model.MinCapacity[unit] * combo[i] for (i, unit) in enumerate(unit_subset)),
            'max_capacity': sum(model.MaxCapacity[unit] * combo[i] for (i, unit) in enumerate(unit_subset))
        }
        for combo in combinations
    }

    for combo in combinations:
        for c, j in enumerate(unit_subset):
            print(f"c: {c}, j: {j}, combo[c]: {combo[c]}")

# Display results
for task in model.Tasks:
    print(f"Task: {task}")
    for combo, capacities in combined_capacities[task].items():
        print(f"  Combination: {combo} -> Min: {capacities['min_capacity']}, Max: {capacities['max_capacity']}")

