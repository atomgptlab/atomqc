# Quick start

These examples use the modern solver path in `jarvis.io.qiskit.inputs` with
`qiskit>=2.0`. They download Wannier tight-binding Hamiltonians from JARVIS-DFT on first
use.

## Single-$k$-point VQE

Run a single-$k$-point VQE on FCC aluminum (`JVASP-816`) and compare against classical
diagonalization:

```python
from jarvis.db.figshare import get_wann_electron, get_hk_tb
from jarvis.io.qiskit.inputs import HermitianSolver

# 1. Fetch the Wannier tight-binding Hamiltonian for Al from JARVIS-DFT
w, ef, atoms = get_wann_electron(jid="JVASP-816")

# 2. Build H(k) at a chosen k-point
hk = get_hk_tb(w=w, k=[0.5, 0.5, 0.0])

# 3. Solve for eigenvalues with VQE and with exact NumPy diagonalization
HS = HermitianSolver(hk)
vqe_energy, vqe_result, vqe = HS.run_vqe()      # min eigenvalue via VQE
classical_vals, classical_vecs = HS.run_numpy() # exact reference

print("VQE ground state:", vqe_energy)
print("Classical minimum:", min(classical_vals.real))
```

## Choosing an ansatz

`QuantumCircuitLibrary` provides a set of hardware-efficient ansätze. Pass one to
`run_vqe` via `var_form`:

```python
from jarvis.core.circuits import QuantumCircuitLibrary

n_qubits = HS.n_qubits()
circ = QuantumCircuitLibrary(n_qubits=n_qubits, reps=2).circuit6()
en_vqe, _, _ = HS.run_vqe(var_form=circ, backend="statevector_simulator")
```

More `reps` makes the ansatz more expressive (lower energy) but deeper — and, on real
hardware, noisier. See [Methods](methods.md) for the trade-offs.

## Pauli decomposition of $H(k)$

Any Hermitian matrix can be written as a weighted sum of Pauli strings — exactly what a
quantum computer measures:

```python
from jarvis.io.qiskit.inputs import decompose_Hamiltonian

op = decompose_Hamiltonian(hk)   # qiskit SparsePauliOp
print("Number of Pauli terms:", len(op))
```

## Full bandstructure (VQD)

VQE returns only the lowest eigenvalue. A bandstructure needs *all* eigenvalues of $H(k)$
at every $k$; **VQD** finds excited states by re-running VQE with an orthogonality
penalty. `get_bandstruct` does this along a high-symmetry $k$-path:

```python
from jarvis.db.figshare import get_wann_electron
from jarvis.io.qiskit.inputs import get_bandstruct

w, ef, atoms = get_wann_electron(jid="JVASP-816")
out = get_bandstruct(w=w, atoms=atoms, line_density=1, savefig=True)
# out["eigvals_q"]  -> quantum (VQD) eigenvalues along the k-path
# out["eigvals_np"] -> classical reference eigenvalues
```

Use `line_density=1` for a quick, crude plot; raise it (and the ansatz `reps`) for a
publication-quality figure.

## Back ends

`run_vqe` / `run_vqd` accept a `backend` argument:

- `"statevector_simulator"` — exact, noiseless (default; best for learning).
- `"aer_simulator*"` — Qiskit Aer shot-based simulators.
- an IBM backend name (e.g. `"ibm_brisbane"`) — real hardware, requires
  `qiskit-ibm-runtime` and a saved IBM Quantum token.

## A couple of materials to try

| Material            | JARVIS ID    |
| ------------------- | ------------ |
| Al (FCC metal)      | `JVASP-816`  |
| Si (semiconductor)  | `JVASP-1002` |

Swap the JID into `get_wann_electron(...)` and re-run.
