from pulp import *

# Warehouses and supply
warehouses = ['W1', 'W2', 'W3']
supply = {'W1': 50, 'W2': 60, 'W3': 25}

# Stores and demand
stores = ['S1', 'S2', 'S3', 'S4']
demand = {'S1': 30, 'S2': 35, 'S3': 25, 'S4': 45}

# Shipping cost matrix
costs = {
    ('W1', 'S1'): 2, ('W1', 'S2'): 3, ('W1', 'S3'): 1, ('W1', 'S4'): 4,
    ('W2', 'S1'): 3, ('W2', 'S2'): 2, ('W2', 'S3'): 2, ('W2', 'S4'): 3,
    ('W3', 'S1'): 4, ('W3', 'S2'): 3, ('W3', 'S3'): 2, ('W3', 'S4'): 1,
}
# Create LP problem
model = LpProblem("Minimize_Transportation_Costs", LpMinimize)

# Define variables
x = LpVariable.dicts("route", (warehouses, stores), lowBound=0, cat='Continuous')

# Objective function
model += lpSum(costs[(w, s)] * x[w][s] for w in warehouses for s in stores), "Total_Transport_Cost"
# Supply constraints
for w in warehouses:
    model += lpSum(x[w][s] for s in stores) <= supply[w], f"Supply_{w}"

# Demand constraints
for s in stores:
    model += lpSum(x[w][s] for w in warehouses) == demand[s], f"Demand_{s}"
model.solve()

print(f"Status: {LpStatus[model.status]}")
print(f"Total Transportation Cost: ₹{value(model.objective)}\n")

for w in warehouses:
    for s in stores:
        if x[w][s].varValue > 0:
            print(f"Ship {x[w][s].varValue} units from {w} to {s}")


