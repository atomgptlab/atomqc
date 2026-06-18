# Methods

This page summarizes the physics and algorithms behind AtomQC. For the full treatment see
the reference paper, *J. Phys.: Condens. Matter* **33**, 385501 (2021),
[doi:10.1088/1361-648X/ac1154](https://iopscience.iop.org/article/10.1088/1361-648X/ac1154/meta).

## From a material to a qubit Hamiltonian

For a crystalline solid, a **Wannier tight-binding Hamiltonian** (WTBH) gives a small
Hermitian matrix $H(k)$ at every crystal momentum $k$. Diagonalizing $H(k)$ across the
Brillouin zone produces the band structure $E_n(k)$.

JARVIS ships pre-computed Wannier Hamiltonians indexed by material ID, e.g. FCC Aluminum
`JVASP-816` and diamond Silicon `JVASP-1002`. The bridge to a quantum computer is the fact
that *any* Hermitian matrix can be written as a weighted sum of **Pauli strings**,

$$ H=\sum_k c_k\, P_k,\qquad P_k\in\{I,X,Y,Z\}^{\otimes n}, $$

and Pauli strings are exactly what a quantum computer can measure. `HermitianSolver`
handles padding $H(k)$ to a power-of-two dimension so it maps onto an integer number of
qubits ($N \times N$ needs $\lceil\log_2 N\rceil$ qubits).

## VQE — Variational Quantum Eigensolver

VQE prepares a parameterized trial state $|\psi(\theta)\rangle$ (the **ansatz**), measures
its energy, and lets a **classical optimizer** push that energy down. The *variational
principle* guarantees

$$\langle\psi(\theta)|H|\psi(\theta)\rangle \;\ge\; E_{\text{ground}},$$

so "lower is always better" — VQE can never undershoot the true ground state. AtomQC uses
hardware-efficient ansätze from `QuantumCircuitLibrary`; the number of layers (`reps`)
trades expressiveness for circuit depth (and noise on real hardware).

## ADAPT-VQE — adaptively grown ansatz

Fixed-depth VQE guesses the circuit shape up front. **ADAPT-VQE** instead *builds* the
ansatz one operator at a time:

1. Start from a reference state (e.g. $|0\dots0\rangle$).
2. From a **pool** of candidate operators $\{P_j\}$, compute the energy gradient of adding each.
3. Append the operator with the **largest gradient** as $e^{i\theta_j P_j}$, then re-optimize all parameters with VQE.
4. Repeat until the largest gradient falls below a threshold (converged).

The payoff is a **compact, problem-tailored circuit** — often fewer gates than fixed VQE
for the same accuracy, which matters on noisy hardware.

## VQD — excited states and band structure

VQE finds only the **lowest** eigenvalue. A band structure needs *all* eigenvalues of
$H(k)$ at every $k$. **VQD (Variational Quantum Deflation)** finds excited states by
re-running VQE while adding a penalty that pushes each new state to be **orthogonal** to
the ones already found:

$$ E_k(\theta)=\langle\psi|H|\psi\rangle+\sum_{j<k}\beta_j\,|\langle\psi|\psi_j\rangle|^2. $$

`get_bandstruct` repeats the VQD eigenvalue solve along a standard $k$-path and overlays
the exact NumPy bands for comparison.

## Classical cross-check

Every run can be compared against exact diagonalization via `HermitianSolver.run_numpy()`
(`numpy.linalg.eigh`). This is how AtomQC validates the quantum results and how the
benchmark CSVs under `atomqc/data/` were generated — see [Example scripts](scripts.md).
