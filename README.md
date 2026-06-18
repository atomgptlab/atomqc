[![name](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/knc6/jarvis-tools-notebooks/blob/master/jarvis-tools-notebooks/Qiskit_based_electronic_bandstructure_.ipynb)

# AtomQC

**Atomistic Calculations on Quantum Computers**

AtomQC is a toolkit for running materials-science electronic-structure and lattice-dynamics
calculations on quantum computers and quantum simulators. It maps the *Wannier tight-binding
Hamiltonians* (WTBH) of real materials — taken from the [JARVIS-DFT](https://jarvis.nist.gov/jarvisdft/)
database — onto qubits and solves for their eigenvalues using variational quantum algorithms such
as the **Variational Quantum Eigensolver (VQE)**, **ADAPT-VQE**, and the **Variational Quantum
Deflation (VQD)** method. From these eigenvalues it reconstructs electronic and phonon
**bandstructures** that can be compared directly against classical (NumPy) diagonalization.

The approach is described in:

> **K. Choudhary, "Quantum computation for predicting electron and phonon properties of solids",**
> *J. Phys.: Condens. Matter* **33**, 385501 (2021).
> [doi:10.1088/1361-648X/ac1154](https://iopscience.iop.org/article/10.1088/1361-648X/ac1154/meta)

Related work on AI-driven atomistic modeling:

> **AtomGPT and generative materials design**, *J. Comput. Chem.* (2025).
> [doi:10.1002/jcc.70202](https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.70202)

> **Note:** This project was originally developed under the
> [github.com/usnistgov](https://github.com/usnistgov) organization. New updates and developments
> are now carried out here.

---

## Why quantum computing for materials?

Predicting the electronic and vibrational properties of solids reduces to finding the eigenvalues
of a Hamiltonian matrix `H(k)` at each point `k` in the Brillouin zone. For a compact basis such as
maximally-localized Wannier functions, these matrices are small enough that their **qubit-mapped**
versions can be diagonalized on today's noisy quantum hardware and simulators, making materials a
practical testbed for near-term quantum algorithms.

AtomQC provides the glue between:

- **JARVIS-DFT** WTBHs (`get_wann_electron`, `get_wann_phonon`, `get_hk_tb`) — the physics inputs,
- **Qiskit** quantum algorithms and simulators — the quantum back end, and
- **jarvis-tools** `HermitianSolver` / `get_bandstruct` — the solver layer that maps `H(k)` to
  Pauli operators, runs the variational circuits, and assembles bandstructures.

---

## Features

- 🔬 **Electronic & phonon eigenvalues** of real materials from JARVIS-DFT WTBHs.
- ⚛️ **VQE** with a library of hardware-efficient ansätze (`QuantumCircuitLibrary`).
- ⚙️ **ADAPT-VQE** — iteratively grows a compact ansatz from a Pauli excitation pool, choosing the
  operator with the largest energy gradient at each step.
- 📈 **VQD bandstructures** along high-symmetry `k`-paths via `get_bandstruct`.
- 🧮 **Classical cross-check** against exact NumPy diagonalization for every run.
- 🖥️ **Multiple back ends** — exact statevector, Qiskit Aer simulators, and real IBM Quantum
  hardware (with an API token).
- 🌐 **Live web app** — interactive VQE / ADAPT-VQE / VQD explorer at
  [atomgpt.org/quantum](https://atomgpt.org/quantum).

---

## Installation

AtomQC targets Python ≥ 3.8 and builds on `jarvis-tools` and `qiskit`.

### From source

```bash
git clone https://github.com/atomgptlab/atomqc.git
cd atomqc
pip install -e .
```

### With conda (reproducible environment)

A pinned environment is provided in `environment.yml`:

```bash
conda env create -f environment.yml
conda activate my_atomqc
```

### Core dependencies

`jarvis-tools`, `qiskit`, `qiskit-aer`, `qiskit-algorithms`, `numpy`, `scipy`, `pandas`,
`scikit-learn`, `matplotlib`. For real IBM hardware also install `qiskit-ibm-runtime`.

> The Qiskit API has changed substantially over time. The example scripts in `atomqc/scripts/`
> were written against the older `qiskit.aqua` API, while the AtomGPT web app (see below) uses the
> modern `qiskit>=1.2` / `qiskit-algorithms` primitives. Match the Qiskit version to the entry
> point you intend to run.

---

## Quick start

Run a single-`k`-point VQE on FCC aluminum (`JVASP-816`) and compare against classical
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

### Full bandstructure (VQD)

```python
from jarvis.db.figshare import get_wann_electron
from jarvis.io.qiskit.inputs import get_bandstruct

w, ef, atoms = get_wann_electron(jid="JVASP-816")
out = get_bandstruct(w=w, atoms=atoms, line_density=1, savefig=True)
# out["eigvals_q"]  -> quantum (VQD) eigenvalues along the k-path
# out["eigvals_np"] -> classical reference eigenvalues
```

---

## Testing

A small, fast test suite covers the core Hamiltonian → qubit → VQE pipeline:

```bash
pip install pytest
pytest atomqc/tests/
```

The tests in `atomqc/tests/test_qiskit.py` build a small synthetic Hermitian `H(k)`,
decompose it into Pauli strings, and check that VQE reproduces the exact NumPy ground state.
They run offline in a few seconds (no JARVIS downloads), which is also what CI runs on every
push.

---

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
├── setup.py
└── README.md
```

### Example scripts

| Script | What it does |
| --- | --- |
| `aluminum_example.py` | Runs VQE on the Al Hamiltonian sweeping COBYLA, L-BFGS-B, SLSQP, CG, SPSA optimizers and plots convergence. |
| `circuit_comparison.py` | Benchmarks the six ansätze in `QuantumCircuitLibrary` at several `k`-points. |
| `compare_elect_vqe.py` | Loops over JARVIS jids, computes min/max electronic eigenvalues with VQE and NumPy, and dumps JSON. |
| `compare_phonons_vqe.py` | Same as above for phonon Hamiltonians. |

The CSV files under `atomqc/data/` hold pre-computed VQE-vs-classical benchmark results referenced
in the paper.

---

## AtomGPT.org Quantum Computation Explorer

A hosted, interactive version of these workflows runs at **[atomgpt.org/quantum](https://atomgpt.org/quantum)**.
It lets you pick a material, choose a back end, and run VQE / ADAPT-VQE at a single `k`-point or
compute a full VQD bandstructure — all from the browser, with live circuit diagrams, statevector /
Bloch-sphere visualizations, and the Hamiltonian matrix shown alongside the results.

The web app is implemented in the AtomGPT / Open WebUI backend:

- **Routes:** `my-open-webui/backend/open_webui/custom_routes/quantum.py`
- **UI:** `my-open-webui/backend/open_webui/custom_templates/quantum.html`

Endpoints exposed by the app:

| Method & path | Purpose |
| --- | --- |
| `GET  /quantum` | Serves the interactive HTML page. |
| `POST /quantum/vqe` | Run Qiskit VQE at a single `k`-point. |
| `POST /quantum/adaptvqe` | Run Qiskit ADAPT-VQE at a single `k`-point. |
| `POST /quantum/bandstructure` | Full VQD bandstructure via `get_bandstruct`. |
| `GET  /quantum/materials` | List the available demo WTBHs. |
| `GET  /quantum/backends` | List available simulator/hardware back ends. |

Demo materials include FCC Al, diamond Si, hexagonal PbS, and FCC Cu (electron Hamiltonians) plus
Al and Si phonon Hamiltonians. The same JARVIS-DFT + `HermitianSolver` machinery used in the
scripts powers the app; it adds modern `qiskit>=1.2` primitives, optional IBM Quantum hardware
execution, and per-qubit Bloch-vector / statevector extraction for visualization.

---

## Citation

If you use AtomQC in your research, please cite:

```bibtex
@article{choudhary2021quantum,
  title   = {Quantum computation for predicting electron and phonon properties of solids},
  author  = {Choudhary, Kamal},
  journal = {Journal of Physics: Condensed Matter},
  volume  = {33},
  number  = {38},
  pages   = {385501},
  year    = {2021},
  doi     = {10.1088/1361-648X/ac1154}
}
```

---

## References & links

- 📄 Paper: [J. Phys.: Condens. Matter 33, 385501 (2021)](https://iopscience.iop.org/article/10.1088/1361-648X/ac1154/meta)
- 📄 Related: [J. Comput. Chem. (2025), doi:10.1002/jcc.70202](https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.70202)
- 🌐 Web app: [atomgpt.org/quantum](https://atomgpt.org/quantum)
- 📓 Colab notebook: [Qiskit-based electronic bandstructure](https://colab.research.google.com/github/knc6/jarvis-tools-notebooks/blob/master/jarvis-tools-notebooks/Qiskit_based_electronic_bandstructure_.ipynb)
- 🧰 JARVIS-Tools: [github.com/usnistgov/jarvis](https://github.com/usnistgov/jarvis)
- ⚛️ Qiskit: [qiskit.org](https://www.qiskit.org/)

---

## License

Distributed under the terms of the [LICENSE](LICENSE.md) included in this repository.
