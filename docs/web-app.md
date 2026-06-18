# AtomGPT.org Quantum Computation Explorer

A hosted, interactive version of these workflows runs at
**[atomgpt.org/quantum](https://atomgpt.org/quantum)**. It lets you pick a material, choose
a back end, and run VQE / ADAPT-VQE at a single $k$-point or compute a full VQD
bandstructure — all from the browser, with live circuit diagrams, statevector /
Bloch-sphere visualizations, and the Hamiltonian matrix shown alongside the results.

The web app is implemented in the AtomGPT / Open WebUI backend:

- **Routes:** `my-open-webui/backend/open_webui/custom_routes/quantum.py`
- **UI:** `my-open-webui/backend/open_webui/custom_templates/quantum.html`

Endpoints exposed by the app:

| Method & path | Purpose |
| --- | --- |
| `GET  /quantum` | Serves the interactive HTML page. |
| `POST /quantum/vqe` | Run Qiskit VQE at a single $k$-point. |
| `POST /quantum/adaptvqe` | Run Qiskit ADAPT-VQE at a single $k$-point. |
| `POST /quantum/bandstructure` | Full VQD bandstructure via `get_bandstruct`. |
| `GET  /quantum/materials` | List the available demo WTBHs. |
| `GET  /quantum/backends` | List available simulator/hardware back ends. |

Demo materials include FCC Al, diamond Si, hexagonal PbS, and FCC Cu (electron
Hamiltonians) plus Al and Si phonon Hamiltonians. The same JARVIS-DFT + `HermitianSolver`
machinery used in the package powers the app; it adds modern `qiskit>=2.0` primitives,
optional IBM Quantum hardware execution, and per-qubit Bloch-vector / statevector
extraction for visualization.

## Related ecosystem

- **AtomGPT.org** ([atomgpt.org](https://atomgpt.org)) — foundation models + 50+ domain
  apps ([atomgpt.org/apps](https://atomgpt.org/apps)).
- **SlaKoNet** ([atomgpt.org/slakonet](https://atomgpt.org/slakonet)) — a learned
  tight-binding $H(k)$ that can feed the same VQE / VQD pipeline for materials with no
  pre-computed Wannier data.
- **ALIGNN / ALIGNN-FF** — graph-network property prediction & force fields.
