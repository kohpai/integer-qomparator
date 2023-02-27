from qiskit import QuantumCircuit, QuantumRegister


def qubits_from_integer(nbits, integer):
    qr = QuantumRegister(nbits)
    circuit = QuantumCircuit(qr)

    for i in range(nbits):
        if integer & (1 << i):
            circuit.x(qr[i])

    u = circuit.to_gate()
    u.name = "INT"
    return u
