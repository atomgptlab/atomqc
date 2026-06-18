# Installation

AtomQC targets Python ≥ 3.8 and builds on `jarvis-tools` and `qiskit`.

## From PyPI

```bash
pip install atomqc
```

## From source

```bash
git clone https://github.com/atomgptlab/atomqc.git
cd atomqc
pip install -e .
```

## With conda (reproducible environment)

A pinned environment is provided in `environment.yml`:

```bash
conda env create -f environment.yml
conda activate my_atomqc
```

## Core dependencies

`jarvis-tools`, `qiskit`, `qiskit-aer`, `qiskit-algorithms`, `numpy`, `scipy`, `pandas`,
`scikit-learn`, `matplotlib`. For real IBM hardware also install `qiskit-ibm-runtime`.

!!! warning "Match the Qiskit version to the entry point"
    The Qiskit API has changed substantially over time. The example scripts in
    `atomqc/scripts/` were written against the older `qiskit.aqua` API, while the modern
    solver path (`jarvis.io.qiskit.inputs`) and the AtomGPT web app use the
    `qiskit>=2.0` / `qiskit-algorithms` primitives. Use a recent `jarvis-tools`
    (≥ 2026.6.12) with `qiskit>=2.0` for the current code paths shown in the
    [Quick start](quickstart.md).

## Verify the install

```bash
python -c "import qiskit, jarvis; print(qiskit.__version__, jarvis.__version__)"
pip install pytest
pytest atomqc/tests/
```

See [Testing](testing.md) for what the test suite covers.
