import qiskit
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator


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


def unmajority_and_add():
    qr = QuantumRegister(3)
    circuit = QuantumCircuit(qr)
    circuit.ccx(qr[0], qr[1], qr[2])
    circuit.cx(qr[2], qr[0])
    circuit.cx(qr[0], qr[1])

    u = circuit.to_gate()
    u.name = "UMA"
    return u


def ripple_carry(nbits):
    c0 = QuantumRegister(1)
    a = QuantumRegister(nbits)
    b = QuantumRegister(nbits)
    circuit = QuantumCircuit(c0, a, b)

    for i in range(nbits):
        carry = c0[0] if i == 0 else a[i - 1]
        circuit.append(majority(), [carry, b[i], a[i]])

    u = circuit.to_gate()
    u.name = "RIPL"
    return u


def find_the_largest_number(a, b):
    # set the number of qubits
    nbits = 32

    c0 = QuantumRegister(1, name='c0')
    ar = QuantumRegister(nbits, name='a')
    br = QuantumRegister(nbits, name='b')
    cr = ClassicalRegister(1, name='msb')
    circuit = QuantumCircuit(c0, ar, br, cr)

    # convert a and b to qubits
    circuit.append(qubits_from_integer(nbits, a), ar)
    circuit.append(qubits_from_integer(nbits, b), br)
    # convert b to -b
    # -b = ~b + 1, where 1 comes from c0
    circuit.x(br)
    circuit.x(c0)

    # compute the MSB of a + (-b) = a - b
    circuit.append(ripple_carry(nbits), c0[:] + ar[:] + br[:])
    circuit.append(unmajority_and_add(),
                   [ar[nbits - 2], br[nbits - 1], ar[nbits - 1]])
    circuit.measure(br[nbits - 1], cr)

    # Print the circuit
    # print(circuit.decompose(["INT", "RIPL"]))

    # Simulate the circuit
    simulator = AerSimulator()
    counts = qiskit.execute(circuit, simulator,
                            shots=1).result().get_counts(circuit)
    # a < b iff the MSB of a - b is 1
    return b if '1' in counts else a
