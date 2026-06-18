# AtomQC

**Atomistic Calculations on Quantum Computers**

AtomQC is a toolkit for running materials-science electronic-structure and
lattice-dynamics calculations on quantum computers and quantum simulators. It maps the
*Wannier tight-binding Hamiltonians* (WTBH) of real materials — taken from the
[JARVIS-DFT](https://jarvis.nist.gov/jarvisdft/) database — onto qubits and solves for
their eigenvalues using variational quantum algorithms such as the **Variational Quantum
Eigensolver (VQE)**, **ADAPT-VQE**, and the **Variational Quantum Deflation (VQD)** method.
From these eigenvalues it reconstructs electronic and phonon **bandstructures** that can be
compared directly against classical (NumPy) diagonalization.

The approach is described in:

> **K. Choudhary, "Quantum computation for predicting electron and phonon properties of solids",**
> *J. Phys.: Condens. Matter* **33**, 385501 (2021).
> [doi:10.1088/1361-648X/ac1154](https://iopscience.iop.org/article/10.1088/1361-648X/ac1154/meta)

!!! note
    This project was originally developed under the
    [github.com/usnistgov](https://github.com/usnistgov) organization. New updates and
    developments are now carried out at
    [github.com/atomgptlab/atomqc](https://github.com/atomgptlab/atomqc).

## Why quantum computing for materials?

Predicting the electronic and vibrational properties of solids reduces to finding the
eigenvalues of a Hamiltonian matrix $H(k)$ at each point $k$ in the Brillouin zone. For a
compact basis such as maximally-localized Wannier functions, these matrices are small
enough that their **qubit-mapped** versions can be diagonalized on today's noisy quantum
hardware and simulators, making materials a practical testbed for near-term quantum
algorithms.

AtomQC provides the glue between:

- **JARVIS-DFT** WTBHs (`get_wann_electron`, `get_wann_phonon`, `get_hk_tb`) — the physics inputs,
- **Qiskit** quantum algorithms and simulators — the quantum back end, and
- **jarvis-tools** `HermitianSolver` / `get_bandstruct` — the solver layer that maps $H(k)$
  to Pauli operators, runs the variational circuits, and assembles bandstructures.

## Features

- 🔬 **Electronic & phonon eigenvalues** of real materials from JARVIS-DFT WTBHs.
- ⚛️ **VQE** with a library of hardware-efficient ansätze (`QuantumCircuitLibrary`).
- ⚙️ **ADAPT-VQE** — iteratively grows a compact ansatz from a Pauli excitation pool.
- 📈 **VQD bandstructures** along high-symmetry $k$-paths via `get_bandstruct`.
- 🧮 **Classical cross-check** against exact NumPy diagonalization for every run.
- 🖥️ **Multiple back ends** — exact statevector, Qiskit Aer simulators, and real IBM
  Quantum hardware (with an API token).
- 🌐 **Live web app** — interactive VQE / ADAPT-VQE / VQD explorer at
  [atomgpt.org/quantum](https://atomgpt.org/quantum).

## Where to next?

- [Installation](installation.md) — set up the environment.
- [Quick start](quickstart.md) — run your first VQE and bandstructure.
- [Methods](methods.md) — the physics and algorithms behind AtomQC.
- [Example scripts](scripts.md) — the batch/benchmark scripts shipped with the package.
- [Web app](web-app.md) — the hosted AtomGPT Quantum Explorer.
