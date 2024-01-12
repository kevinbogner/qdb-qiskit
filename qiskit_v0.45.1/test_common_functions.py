"""
This module contains test cases for the functions defined in the common_functions module. 
It aims to ensure that each function performs as expected under various scenarios, 
including normal operation, boundary conditions, and potential error cases.

Tests include:
- Testing the encoding and decoding of quantum messages.
- Verifying the removal of 'garbage' bits in quantum key distribution.
- Ensuring correct sampling of bits.
- Testing the creation and measurement of Bell states in a quantum circuit.
"""

from rotation.rotation_functions import (
    encode_message,
    decode_message,
    remove_garbage,
    sample_bits,
    create_and_measure_bell_state,
    execute_and_extract_results,
)


def test_encode_message():
    """
    Test the encode_message function to ensure it correctly encodes a list of bits
    based on provided bases and returns the appropriate quantum circuits.
    """
    bits = [0, 1]
    bases = [0, 1]
    n = 2
    encoded_message = encode_message(bits, bases, n)

    assert len(encoded_message) == 2  # Check the number of circuits

    # Test specific gates in the circuit
    for i in range(n):
        gate_sequence = list(map(lambda x: x[0].name, encoded_message[i].data))
        if bases[i] == 0:  # Z-basis
            if bits[i] == 0:
                assert "x" not in gate_sequence
            else:
                assert "x" in gate_sequence
        else:  # X-basis
            if bits[i] == 0:
                assert "h" in gate_sequence
            else:
                assert "x" in gate_sequence and "h" in gate_sequence


def test_decode_message():
    """
    Test the decode_message function to ensure it accurately decodes a message
    that was encoded using the encode_message function, using the same bases.
    """
    bits = [0, 1]
    bases = [0, 1]
    n = 2
    encoded_message = encode_message(bits, bases, n)
    decoded_bits = decode_message(encoded_message, bases, n)
    assert isinstance(decoded_bits, list)
    assert decoded_bits == bits


def test_remove_garbage():
    """
    Test the remove_garbage function to verify that it correctly filters out the 'garbage' bits
    where the bases of Alice and Bob do not align.
    """
    a_bases = [0, 1, 0, 1]
    b_bases = [1, 1, 0, 0]
    bits = [1, 0, 1, 1]
    n = 4
    good_bits = remove_garbage(a_bases, b_bases, bits, n)
    assert good_bits == [0, 1]

    # Testing with empty or mismatched inputs
    assert not remove_garbage(
        [], [], [], 0
    )  # Asserts that the result is an empty list (Falsey)
    assert not remove_garbage([0], [1], [0], 1)  # Same as above


def test_sample_bits():
    """
    Test the sample_bits function to ensure that it correctly samples and removes
    bits from the original list based on the given selection indices.
    """
    bits = [0, 1, 0, 1]
    selection = [1, 2]
    sampled_bits = sample_bits(bits, selection)
    assert sampled_bits == [1, 1]
    assert bits == [0, 0]
    # Test with out-of-range selection
    bits = [0, 1, 0, 1]
    selection = [10]
    sampled_bits = sample_bits(bits, selection)
    assert len(sampled_bits) == 1
    assert len(bits) == 3


def test_create_and_measure_bell_state():
    """
    Test the create_and_measure_bell_state function to ensure it creates a quantum circuit
    that prepares the specified number of Bell states and measures them correctly.
    """
    n = 2
    bell_circuit = create_and_measure_bell_state(n)
    assert len(bell_circuit.qubits) == 4
    assert len(bell_circuit.clbits) == 4
    for i in range(n):
        assert "h" in [gate.name for gate, _, _ in bell_circuit.data[2 * i : 2 * i + 2]]
        assert "cx" in [
            gate.name for gate, _, _ in bell_circuit.data[2 * i : 2 * i + 2]
        ]
        assert "measure" in [gate.name for gate, _, _ in bell_circuit.data[-2 * n :]]


def test_execute_and_extract_results():
    """
    Execute the Bell state circuit on a quantum simulator, extract, and process the results.
    """
    n = 1
    bell_circuit = create_and_measure_bell_state(n)
    m_bits, m_prime_bits = execute_and_extract_results(bell_circuit, shots=1024)
    assert all(m == m_prime for m, m_prime in zip(m_bits, m_prime_bits))
