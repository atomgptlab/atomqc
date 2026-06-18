"""Superquick tests for the Hamiltonian -> qiskit -> VQE pipeline.

These mirror the core of the AtomQC tutorial notebook (build a Hermitian
H(k), decompose it into Pauli strings, solve it with VQE/VQD) but use a
small synthetic matrix so they run in seconds with no network downloads.
"""
import numpy as np
import pytest

from jarvis.io.qiskit.inputs import HermitianSolver, decompose_Hamiltonian
from jarvis.core.circuits import QuantumCircuitLibrary


def _hermitian(n=4, seed=0):
    """Return a small random Hermitian matrix to stand in for H(k)."""
    rng = np.random.RandomState(seed)
    a = rng.rand(n, n) + 1j * rng.rand(n, n)
    return a + a.conj().T


def test_hermitian_solver_basics():
    """HermitianSolver pads to 2**n and reports the right qubit count."""
    hk = _hermitian(4)
    hs = HermitianSolver(hk)
    assert hs.check_hermitian()
    assert hs.n_qubits() == 2  # 4x4 -> 2 qubits


def test_pauli_decomposition_roundtrip():
    """Pauli decomposition of H reconstructs the original matrix (qiskit)."""
    hk = _hermitian(4)
    op = decompose_Hamiltonian(hk)
    assert len(op) > 0
    assert np.allclose(op.to_matrix(), hk)


def test_vqe_matches_numpy_ground_state():
    """VQE ground-state energy matches exact NumPy diagonalization."""
    hk = _hermitian(4)
    hs = HermitianSolver(hk)
    vals, _ = hs.run_numpy()
    circ = QuantumCircuitLibrary(n_qubits=hs.n_qubits(), reps=2).circuit6()
    en_vqe, _, _ = hs.run_vqe(var_form=circ, backend="statevector_simulator")
    # Variational principle: VQE can never dip below the true ground state.
    assert en_vqe >= float(vals[0]) - 1e-6
    # ...and a hardware-efficient ansatz should land near it (the classical
    # optimizer may settle in a shallow local minimum, so keep this loose).
    assert en_vqe == pytest.approx(float(vals[0]), abs=0.25)
