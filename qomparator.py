from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister


def qubits_from_integer(nbits, integer):
    qr = QuantumRegister(nbits)
    cr = ClassicalRegister(nbits)
    circuit = QuantumCircuit(qr, cr)

    for i in range(nbits):
        if integer & (1 << i):
            circuit.x(qr[i])

    return circuit, qr, cr
