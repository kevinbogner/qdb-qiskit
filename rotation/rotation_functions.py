"""This module contains common functions used in quantum computing notebooks.

It includes functions to encode and decode messages using quantum circuits.

Some functions are adapted from:
https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/quantum-key-distribution.ipynb
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from IPython.display import display


def encode_message(bits, bases, n):
    """
    This function encodes a message into a quantum circuit based on the provided bits and bases.

    Parameters:
    bits (list): A list of bits to be encoded. Each bit should be either 0 or 1.
    bases (list): A list of bases for each bit. Each base should be either 0 or 1.
    n (int): The number of bits to encode.

    Returns:
    list: A list of QuantumCircuit objects, each representing an encoded bit.

    The function works as follows:
    For each bit in the input:
    - If the base is 0 (Computational Basis):
        - If the bit is 0, it does nothing (|0> state).
        - If the bit is 1, it applies an X gate (|1> state).
    - If the base is 1 (Hadamard Basis):
        - If the bit is 0, it applies a Hadamard gate (|+> state).
        - If the bit is 1, it applies an X gate followed by a Hadamard gate (|-> state).
    After encoding each bit, it adds a barrier to the circuit.
    """
    message = []
    for i in range(n):
        qc = QuantumCircuit(1, 1)
        if bases[i] == 0:  # Computational basis
            if bits[i] == 0:
                pass  # |0>
            else:
                qc.x(0)  # |1>
        else:  # Hadamard basis
            if bits[i] == 0:
                qc.h(0)  # |+>
            else:
                qc.x(0)
                qc.h(0)  # |->
        qc.barrier()
        message.append(qc)
    return message


def apply_specific_rotation(a_bases, b_bases, message):
    """
    This function applies a specific rotation to each circuit based on the conditions:
    - If a=0 and b=1, then rotate anticlockwise (counterclockwise) by 90° (+π/2).
    - If a=1 and b=0, then rotate clockwise by 90° (-π/2).

    Parameters:
    a_bases (list): A list of bases where each base is either 0 or 1.
    b_bases (list): A list of bases where each base is either 0 or 1.
    message (list): A list of QuantumCircuit objects, each representing an encoded bit.

    Returns:
    list: The updated list of QuantumCircuit objects after applying the rotations.
    """
    for i, (a_base, b_base) in enumerate(zip(a_bases, b_bases)):
        if a_base == 0 and b_base == 1:
            # Anticlockwise (counterclockwise) rotation by 90°
            message[i].ry(np.pi / 2, 0)
        elif a_base == 1 and b_base == 0:
            # Clockwise rotation by 90°
            message[i].ry(-np.pi / 2, 0)

    return message


def decode_message(message, bases, n, draw_circuit=False):
    """
    This function decodes a message by measuring the state in the specified basis.

    Parameters:
    message (list): A list of QuantumCircuit objects, each representing an encoded bit.
    bases (list): A list of bases for each bit. Each base should be either 0 or 1.
    n (int): The number of bits to decode.
    draw_circuit (bool, optional): If True, the function will draw and display each quantum circuit.

    Returns:
    list: A list of measurement results. Each result is either 0 or 1.

    The function works as follows:
    For each bit in the input:
    - If the base is 0 (Computational Basis), it measures the state of the circuit in the Comp. Bas.
    - If the base is 1 (Hadamard Basis), it applies Hadamard gate to the circuit before measurement.
    - It executes the quantum circuit on a quantum simulator and extracts the measurement result.
    - If draw_circuit is True, it draws and displays the quantum circuit.
    """
    backend = Aer.get_backend("aer_simulator")
    __ = backend  # dummy operation to suppress warning
    measurements = []
    for q in range(n):
        # Apply the measurement basis transformation if necessary
        if bases[q] == 1:  # Measuring in Hadamard basis
            message[q].h(0)
        message[q].measure(0, 0)

        # Draw the circuit if the flag is set to True
        if draw_circuit:
            print(f"Circuit {q}:")
            display(message[q].draw(output="mpl"))

        # Execute the circuit on a quantum simulator
        aer_sim = Aer.get_backend("aer_simulator")
        result = aer_sim.run(
            transpile(message[q], aer_sim), shots=1, memory=True
        ).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    return measurements


def remove_garbage(a_bases, b_bases, bits, n):
    """
    This removes the bits from the message, if the bases to encode and measure it are different.

    Parameters:
    a_bases (list): A list of bases used by A. Each base should be either 0 or 1.
    b_bases (list): A list of bases used by B. Each base should be either 0 or 1.
    bits (list): A list of bits to be filtered. Each bit should be either 0 or 1.
    n (int): The number of bits to filter.

    Returns:
    list: A list of 'good' bits, if the bases used by A and B to encode and measure it are the same.

    The function works as follows:
    For each bit in the input:
    - If the bases used by Alice and Bob are the same, it adds the bit to the list of 'good' bits.
    """
    good_bits = []
    for q in range(n):
        if a_bases[q] == b_bases[q]:
            good_bits.append(bits[q])
    return good_bits


def sample_bits(bits, selection):
    """
    This function samples bits from a list at the indices specified in the selection list.

    Parameters:
    bits (list): A list of bits to sample from. Each bit should be either 0 or 1.
    selection (list): A list of indices to sample. Each index should be a non-negative integer.

    Returns:
    list: A list of sampled bits.

    The function works as follows:
    For each index in the selection list:
    - It uses np.mod to ensure the index is within the range of the list.
    - It removes the bit at the index from the list and adds it to the list of sampled bits.
    """
    sample = []
    for i in selection:
        i = np.mod(i, len(bits))
        sample.append(bits.pop(i))
    return sample
