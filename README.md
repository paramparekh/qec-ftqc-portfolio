# Quantum Error Correction (QEC) Simulation Toolkit

A Python toolkit for building, simulating, and evaluating quantum error-correcting codes under noise.

## What is this project?

This project is a modular Python package designed to simulate quantum error correction (QEC) and evaluate how different quantum codes perform when subjected to noise. It provides tools to define code structures, generate quantum circuits for syndrome extraction, decode error patterns, and calculate logical error rates.

## What does it do?

*   **Define Quantum Codes:** Construct stabilizer and CSS codes, including simple baseline codes (repetition and Steane codes) and advanced constructions (rotated surface codes, bivariate bicycle codes).
*   **Verify Code Properties:** Check that stabilizers commute, extract logical operators, and find the code's minimum distance.
*   **Build Noisy Circuits:** Construct quantum circuits with noise models to simulate actual quantum hardware behavior.
*   **Decode & Correct Errors:** Interface with decoders (such as Minimum Weight Perfect Matching and BP-OSD) to analyze error syndromes and determine if the correction succeeded.
*   **Analyze Performance:** Run simulations to estimate logical error rates, find thresholds, and evaluate resource requirements.

---

## Quick Start

### Prerequisites
- Python 3.11+
- Git
- Windows PowerShell (or bash on Linux/Mac)

### 1. Clone and enter the project
```bash
git clone <your-repo-url> qec-ftqc-portfolio
cd qec-ftqc-portfolio
```

### 2. Create and activate a virtual environment (no conda needed)
```powershell
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```
```bash
# Linux / Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install all dependencies
```bash
pip install -e ".[dev]"
```

### 4. Verify the install
```bash
pytest tests/ -v
```

---

## Repository Structure

*   [qec_toolkit/](file:///c:/Users/param/OneDrive/Desktop/QuantumComputing-Research/QEC-Research/qec-ftqc-portfolio/qec_toolkit) — Core Python package
    *   [codes/](file:///c:/Users/param/OneDrive/Desktop/QuantumComputing-Research/QEC-Research/qec-ftqc-portfolio/qec_toolkit/codes) — Code constructors (repetition, surface, Steane, bivariate bicycle)
    *   [verification/](file:///c:/Users/param/OneDrive/Desktop/QuantumComputing-Research/QEC-Research/qec-ftqc-portfolio/qec_toolkit/verification) — Math verifications (GF(2) linear algebra, logical checks, distance finding)
    *   [circuits/](file:///c:/Users/param/OneDrive/Desktop/QuantumComputing-Research/QEC-Research/qec-ftqc-portfolio/qec_toolkit/circuits) — Syndrome measurement circuits and fault-tolerant gadget builders
    *   [decoders/](file:///c:/Users/param/OneDrive/Desktop/QuantumComputing-Research/QEC-Research/qec-ftqc-portfolio/qec_toolkit/decoders) — Interfaces to decoders (MWPM, BP-OSD)
    *   [simulation/](file:///c:/Users/param/OneDrive/Desktop/QuantumComputing-Research/QEC-Research/qec-ftqc-portfolio/qec_toolkit/simulation) — Noise modeling and Monte Carlo simulations
    *   [plots/](file:///c:/Users/param/OneDrive/Desktop/QuantumComputing-Research/QEC-Research/qec-ftqc-portfolio/qec_toolkit/plots) — Plot generation for error rate curves
*   [examples/](file:///c:/Users/param/OneDrive/Desktop/QuantumComputing-Research/QEC-Research/qec-ftqc-portfolio/examples) — Jupyter notebooks showing how to use the toolkit
*   [tests/](file:///c:/Users/param/OneDrive/Desktop/QuantumComputing-Research/QEC-Research/qec-ftqc-portfolio/tests) — Unit tests for verifying correct behavior
*   [configs/](file:///c:/Users/param/OneDrive/Desktop/QuantumComputing-Research/QEC-Research/qec-ftqc-portfolio/configs) — Configuration files for simulations

---

## License

MIT License — see [LICENSE](file:///c:/Users/param/OneDrive/Desktop/QuantumComputing-Research/QEC-Research/qec-ftqc-portfolio/LICENSE) for details.
