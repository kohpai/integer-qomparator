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


def majority():
    qr = QuantumRegister(3)
    circuit = QuantumCircuit(qr)
    circuit.cx(qr[2], qr[1])
    circuit.cx(qr[2], qr[0])
    circuit.ccx(qr[0], qr[1], qr[2])

    u = circuit.to_gate()
    u.name = "MAJ"
    return u


# def unmajority_and_add():
#     qr = QuantumRegister(3)
#     circuit = QuantumCircuit(qr)
#     circuit.ccx(qr[0], qr[1], qr[2])
#     circuit.cx(qr[2], qr[0])
#     circuit.cx(qr[0], qr[1])
#
#     u = circuit.to_gate()
#     u.name = "UMA"
#     return u


def adder(nbits):
    c0 = QuantumRegister(1)
    a = QuantumRegister(nbits)
    b = QuantumRegister(nbits)
    # z = QuantumRegister(1)
    circuit = QuantumCircuit(c0, a, b)

    for i in range(nbits):
        carry = c0[0] if i == 0 else a[i - 1]
        circuit.append(majority(), [carry, b[i], a[i]])

    # circuit.cx(a[nbits - 1], z[0])
    #
    # for i in range(nbits - 1, -1, -1):
    #     carry = c0[0] if i == 0 else a[i - 1]
    #     circuit.append(unmajority_and_add(), [carry, b[i], a[i]])

    u = circuit.to_gate()
    u.name = "ADD"
    return u
