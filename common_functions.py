"""
This module contains common functions used in quantum computing notebooks.

It includes functions to encode and decode messages using quantum circuits.

Functions are adapted from:
https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/quantum-key-distribution.ipynb
"""

from qiskit import QuantumCircuit, Aer


def encode_message(bits, bases, n):
    """
    Encodes a message using quantum circuits based on the provided bits and bases.

    Parameters:
    bits (list): A list of bits to encode.
    bases (list): A list of bases to use for encoding.
    n (int): The length of the message.

    Returns:
    list: A list of QuantumCircuit objects representing the encoded message.
    """
    message = []
    for i in range(n):
        qc = QuantumCircuit(1, 1)
        if bases[i] == 0:  # Prepare qubit in Z-basis
            if bits[i] == 0:
                pass
            else:
                qc.x(0)
        else:  # Prepare qubit in X-basis
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        qc.barrier()
        message.append(qc)
    return message


def encode_message_range(bits, bases, start, end, n):
    """
    Encodes a message using quantum circuits based on the provided bits and bases.

    Parameters:
    bits (list): A list of bits to encode.
    bases (list): A list of bases to use for encoding.
    start (int): The starting index of the range of qubits to encode.
    end (int): The ending index of the range of qubits to encode.
    n (int): The length of the message.

    Returns:
    list: A list of QuantumCircuit objects representing the encoded message.
    """
    message = []
    for i in range(start, min(end, start + n)):
        qc = QuantumCircuit(1)  # Create a QuantumCircuit with one quantum bit
        if bases[i] == 0:  # Prepare qubit in Z-basis
            if bits[i] == 0:
                pass
            else:
                qc.x(0)
        else:  # Prepare qubit in X-basis
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        message.append(qc)
    return message


def decode_message(message, bases, n):
    """
    Decodes a message using quantum circuits based on the provided message and bases.

    Parameters:
    message (list): A list of QuantumCircuit objects representing the encoded message.
    bases (list): A list of bases to use for decoding.
    n (int): The length of the message.

    Returns:
    list: A list of bits representing the decoded message.
    """
    backend = Aer.get_backend("aer_simulator")
    __ = backend  # dummy operation to suppress warning
    measurements = []
    for q in range(n):
        if bases[q] == 0:  # measuring in Z-basis
            message[q].measure(0, 0)
        if bases[q] == 1:  # measuring in X-basis
            message[q].h(0)
            message[q].measure(0, 0)
        aer_sim = Aer.get_backend("aer_simulator")
        result = aer_sim.run(message[q], shots=1, memory=True).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    return measurements
