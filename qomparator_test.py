import unittest

import qiskit
import qomparator as qmp
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator


class TestQomparator(unittest.TestCase):

    def test_qubits_from_negative_integer(self):
        nbits = 4
        qr = QuantumRegister(nbits)
        cr = ClassicalRegister(nbits)
        circuit = QuantumCircuit(qr, cr)

        circuit.append(qmp.qubits_from_integer(nbits, -5), qr)
        circuit.measure(qr, cr)

        simulator = AerSimulator()
        counts = qiskit.execute(circuit, simulator,
                                shots=10).result().get_counts(circuit)
        self.assertEqual(10, counts['1011'])

    def test_qubits_from_positive_integer(self):
        nbits = 4
        qr = QuantumRegister(nbits)
        cr = ClassicalRegister(nbits)
        circuit = QuantumCircuit(qr, cr)

        circuit.append(qmp.qubits_from_integer(nbits, 5), qr)
        circuit.measure(qr, cr)

        simulator = AerSimulator()
        counts = qiskit.execute(circuit, simulator,
                                shots=10).result().get_counts(circuit)
        self.assertEqual(10, counts['0101'])

    def test_adder(self):
        nbits = 4
        c0 = QuantumRegister(1)
        a = QuantumRegister(nbits)
        b = QuantumRegister(nbits)
        cr = ClassicalRegister(1)
        circuit = QuantumCircuit(c0, a, b, cr)

        circuit.append(qmp.qubits_from_integer(nbits, 8), a)
        circuit.append(qmp.qubits_from_integer(nbits, -8), b)
        circuit.append(qmp.adder(nbits), c0[:] + a[:] + b[:])
        circuit.measure(a[nbits-1], cr)

        simulator = AerSimulator()
        counts = qiskit.execute(circuit, simulator,
                                shots=10).result().get_counts(circuit)
        self.assertEqual(10, counts['1'])


if __name__ == '__main__':
    unittest.main()
