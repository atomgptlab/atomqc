# Example scripts

The package ships a handful of batch/benchmark scripts under `atomqc/scripts/`.

| Script | What it does |
| --- | --- |
| `aluminum_example.py` | Runs VQE on the Al Hamiltonian sweeping COBYLA, L-BFGS-B, SLSQP, CG, SPSA optimizers and plots convergence, alongside VQD electron and phonon bandstructures. |
| `circuit_comparison.py` | Benchmarks the ansätze in `QuantumCircuitLibrary` at several $k$-points. |
| `compare_elect_vqe.py` | Loops over JARVIS jids, computes min/max electronic eigenvalues with VQE and NumPy, and dumps JSON. |
| `compare_phonons_vqe.py` | Same as above for phonon Hamiltonians. |

!!! warning "Qiskit API version"
    `aluminum_example.py` and the other scripts were written against the older
    `qiskit.aqua` API (`from qiskit.aqua ... import VQE, QuantumInstance`, `EfficientSU2`,
    `op_converter`). They are kept as historical references for the workflow used in the
    paper. For current `qiskit>=2.0`, use the `HermitianSolver` / `get_bandstruct` paths
    shown in the [Quick start](quickstart.md) and [Methods](methods.md) pages.

## Benchmark data

The CSV files under `atomqc/data/` hold pre-computed VQE-vs-classical benchmark results
referenced in the paper:

- `electron_vqe_np_jid.csv` — electron VQE vs classical eigenvalues per JARVIS id.
- `phonon_vqe_np_jid.csv` — phonon VQE vs classical eigenvalues per JARVIS id.

## Repository layout

```
atomqc/
├── atomqc/
│   ├── __init__.py                 # version
│   ├── scripts/
│   │   ├── aluminum_example.py     # VQE on Al with several classical optimizers
│   │   ├── circuit_comparison.py   # compare ansätze from QuantumCircuitLibrary
│   │   ├── compare_elect_vqe.py    # batch electron VQE vs NumPy over JARVIS jids
│   │   └── compare_phonons_vqe.py  # batch phonon VQE vs NumPy over JARVIS jids
│   ├── tests/
│   │   └── test_qiskit.py          # fast offline tests: H(k) -> Pauli -> VQE
│   └── data/
│       ├── electron_vqe_np_jid.csv # benchmark: electron VQE vs classical
│       └── phonon_vqe_np_jid.csv   # benchmark: phonon VQE vs classical
├── environment.yml                 # pinned conda environment
├── mkdocs.yml                      # documentation site config
├── docs/                           # documentation sources
├── setup.py
└── README.md
```
