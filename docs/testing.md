# Testing

A small, fast test suite covers the core Hamiltonian → qubit → VQE pipeline:

```bash
pip install pytest
pytest atomqc/tests/
```

The tests in `atomqc/tests/test_qiskit.py` build a small synthetic Hermitian $H(k)$,
decompose it into Pauli strings, and check the solver against exact NumPy diagonalization.
They run offline in a few seconds (no JARVIS downloads), which is also what CI runs on
every push.

## What the tests check

- **`test_hermitian_solver_basics`** — `HermitianSolver` pads $H(k)$ to a power of two and
  reports the right qubit count.
- **`test_pauli_decomposition_roundtrip`** — `decompose_Hamiltonian` reproduces the
  original matrix from its Pauli-string expansion.
- **`test_vqe_matches_numpy_ground_state`** — VQE on the statevector simulator respects the
  variational principle ($E_\text{VQE} \ge E_\text{ground}$) and lands near the exact
  ground state. The closeness bound is intentionally loose because the classical optimizer
  may settle in a shallow local minimum, which is not reproducible across machines.

## Continuous integration

GitHub Actions builds the conda environment from `environment.yml`, installs the package,
and runs the suite under coverage on every push and pull request. The workflow lives at
`.github/workflows/main.yml`.
