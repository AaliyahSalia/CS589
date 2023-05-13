from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_bloch_multivector, plot_histogram
import matplotlib.pyplot as plt


#Set the matplotlib backend to interactive
plt.ion()

#Create a quantum circuit with two qubits
qc = QuantumCircuit(2, 2)

#Apply the Hadamard gate to the first qubit
qc.h(0)

#Apply the controlled-NOT gate (CNOT gate) with the first qubit as the control and the second qubit as the target.
qc.cx(0, 1)

#Measure both qubits and store the measurement results in classical bits.
qc.measure([0, 1], [0, 1])

#Use the local simulate backend
simulator = Aer.get_backend('statevector_simulator')

#Execute the circuit on the simulate
job = execute(qc, simulator, shots=1024)

#Get the result of the simulation
result = job.result()

#Get the counts of each measurement outcome
counts = result.get_counts(qc)

#Print the counts
print("\nTotal count for 00 and 11 are:", counts, flush=True)

#Plot the histogram of the measurement outcomes
plot_histogram(counts)
plt.show()

#Execute the circuit on the simulator to get the final state
job_state = execute(qc, simulator)

#Get the final state
state = job_state.result().get_statevector()

#Plot the Block sphere representation of the state
plot_bloch_multivector(state)

#Block the execution until the plots are closed
plt.show(block=True)

#Draw the Quantum Circuit
print(qc.draw(output='text'))





