import unittest

import qiskit
import qomparator as qmp
from qiskit_aer import AerSimulator


class TestQomparator(unittest.TestCase):
    def test_qubits_from_negative_integer(self):
        integer = -5

        circuit, integer_qr, integer_bin = qmp.qubits_from_integer(4, integer)
        circuit.measure(integer_qr, integer_bin)

        simulator = AerSimulator()
        counts = qiskit.execute(circuit, simulator, shots=10).result().get_counts(circuit)
        self.assertEqual(10, counts['1011'])

    def test_qubits_from_positive_integer(self):
        integer = 5

        circuit, integer_qr, integer_bin = qmp.qubits_from_integer(4, integer)
        circuit.measure(integer_qr, integer_bin)

        simulator = AerSimulator()
        counts = qiskit.execute(circuit, simulator, shots=10).result().get_counts(circuit)
        self.assertEqual(10, counts['0101'])


if __name__ == '__main__':
    unittest.main()
