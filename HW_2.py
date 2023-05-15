import pennylane as qml
from pennylane import numpy as np
from tabulate import tabulate

#Define the adjacency matrix representing the TSP problem
adjacency_matrix = np.array([[0, 2, 9, 10],
                             [1, 0, 6, 4],
                             [15, 7, 0, 8],
                             [6, 3, 12, 0]])

#Define the number of cities
num_cities = len(adjacency_matrix)

#Number of layers in the quantum circuit
num_layers = 2 
dev = qml.device("default.qubit", wires=num_cities)

#Define the quantum circuit
@qml.qnode(dev)
def circuit(params):
    for i in range(num_cities):
        qml.RX(params[i], wires=i)

    for layer in range(num_layers):
        for i in range(num_cities):
            qml.CNOT(wires=[i, (i + 1) % num_cities])
            qml.RZ(params[i + num_cities * layer], wires=(i + 1) % num_cities)
            qml.CNOT(wires=[i, (i + 1) % num_cities])

    return qml.expval(qml.PauliZ(0))

#Define the cost function to minimize
def cost(params):
    return sum([adjacency_matrix[i, j] * circuit(params) for i in range(num_cities) for j in range(num_cities)])

#Initialize random parameters
params = np.random.uniform(0, np.pi, (num_cities * num_layers,))

#Perform Optimization
opt = qml.GradientDescentOptimizer(0.1)
steps = 100

table = []
table.append(["Step", "Cost"])
table.append(["----", "----"])

for i in range(steps):
    params = opt.step(cost, params)

    if (i + 1) % 10 == 0:
        table.append([i + 1, "{:.6f}".format(cost(params))])

#Extract the optimal parameters
optimal_params = params

#Print the optimal solution
print("Optimal Solution: ")
solution_table = []
solution_table.append(["City", "RX"])
solution_table.append(["----", "----"])

for i in range(num_cities):
    solution_table.append([i, "{:.6f}".format(optimal_params[i])])

print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
print()
print(tabulate(solution_table, headers="firstrow", tablefmt="fancy_grid"))
