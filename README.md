# Circuit-Level Evaluation and Fault-Tolerant Gadget Simulation for Surface and Bivariate Bicycle Codes

> **Portfolio project** targeting QEC/FTQC industry roles (Quantum Error Correction Engineer / FTQC Research Engineer).  
> **Timeline:** 24 weeks · 8–12 focused hours per week  
> **Author:** Param (Graduate Student → Industry QEC Researcher)

---

## Abstract

This project builds a **reproducible, end-to-end QEC/FTQC software and research pipeline** in Python. Starting from stabilizer parity-check matrices, the toolkit constructs quantum error-correcting codes (repetition, surface, Steane, bivariate bicycle/qLDPC), builds syndrome-extraction circuits with circuit-level noise models, generates Stim-style detector error models (DEMs), decodes noisy experiments using MWPM and BP-OSD, estimates logical error rates, and demonstrates small fault-tolerant gadgets. The project directly maps to senior QEC industry roles that require analytical depth, numerical rigor, and production-quality, maintainable code.

**Flagship result:** Circuit-level logical memory experiments for rotated surface codes and bivariate bicycle (BB) / qLDPC codes, with threshold/pseudo-threshold analysis, decoder comparison (MWPM vs BP-OSD), MILP distance verification for small instances, and FT gadget demonstrations (logical state prep, logical CNOT, magic-state resource estimation).

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

You should see all placeholder tests collected and passing.

---

## Repository Structure

```
qec-ftqc-portfolio/
├── qec_toolkit/                  # Core Python package
│   ├── codes/
│   │   ├── base.py               # CSSCode dataclass + validation
│   │   ├── repetition.py         # Repetition code baseline
│   │   ├── surface.py            # Rotated surface code
│   │   ├── steane.py             # [[7,1,3]] Steane code reference
│   │   ├── hgp.py                # Hypergraph product construction
│   │   └── bb.py                 # Bivariate bicycle (qLDPC) construction
│   ├── verification/
│   │   ├── gf2.py                # GF(2) rank, nullspace, rowspace
│   │   ├── logicals.py           # Logical operator extraction & checks
│   │   ├── distance_milp.py      # Exact distance via MILP (small codes)
│   │   └── code_checks.py        # Commutation, k, stabilizer sanity checks
│   ├── circuits/
│   │   ├── syndrome.py           # Stabilizer measurement circuits
│   │   ├── memory.py             # Logical memory experiments
│   │   ├── state_prep.py         # |0_L>, |+_L> preparation demos
│   │   ├── gadgets.py            # Logical CNOT / magic-state demos
│   │   └── export.py             # Qiskit / Cirq / Stim interfaces
│   ├── decoders/
│   │   ├── base.py               # Decoder interface (ABC)
│   │   ├── matching.py           # PyMatching (MWPM) wrapper
│   │   └── bposd.py              # BP-OSD wrapper/adapter
│   ├── simulation/
│   │   ├── noise.py              # Phenomenological & circuit-level noise models
│   │   ├── logical_error.py      # Shot runner & LER computation
│   │   └── threshold.py          # Pseudo-threshold fitting
│   ├── plots/
│   │   ├── ler_curves.py         # LER vs p plots
│   │   └── tables.py             # Code parameter & resource tables
│   └── utils/
│       └── io.py                 # Config loading, CSV saving, seed helpers
├── examples/                     # Reproducible Jupyter notebooks
│   ├── 01_gf2_stabilizer_basics.ipynb
│   ├── 02_surface_code_memory.ipynb
│   ├── 03_bb_code_reproduction.ipynb
│   ├── 04_decoder_comparison.ipynb
│   ├── 05_circuit_level_qec.ipynb
│   └── 06_ft_gadget_demo.ipynb
├── reports/
│   └── final_report.md           # 6–10 page technical write-up
├── tests/                        # pytest test suite
│   ├── test_gf2.py
│   ├── test_css_commutation.py
│   ├── test_small_codes.py
│   └── test_bb_parameters.py
├── data/                         # Saved simulation outputs (CSV, DEM files)
├── configs/                      # Experiment configuration YAML/JSON files
│   └── experiment_template.yaml
├── .github/
│   └── ISSUE_TEMPLATE/           # GitHub issue templates by phase
├── pyproject.toml                # Package metadata & dependencies
├── requirements.txt              # Pinned dependencies for reproducibility
├── CODING_STANDARDS.md           # Style, testing, and reproducibility rules
└── README.md                     # This file
```

---

## 24-Week Roadmap

| Phase | Weeks | Theme |
|-------|-------|-------|
| **0** | 0 | Kickoff: repo, env, README, issue board, scope locked |
| **1** | 1–3 | GF(2) engine + stabilizer algebra |
| **2** | 4–6 | Surface-code baseline + MWPM decoding |
| **3** | 7–10 | Bivariate bicycle / qLDPC reproduction |
| **4** | 11–14 | Circuit-level syndrome extraction + detector models |
| **5** | 15–18 | Fault-tolerant gadgets + universal FTQC bridge |
| **6** | 19–20 | Resource estimation + algorithm-level execution |
| **7** | 21–24 | Packaging, report, portfolio polish |

---

## Reproducibility Rules

Every experiment in this project **must** have:
1. A config file in `configs/` (YAML or JSON) with all parameters including a random seed.
2. A saved result in `data/` as CSV.
3. A plot saved as PNG/PDF.
4. A notebook or script in `examples/` that regenerates the result from scratch.

See `configs/experiment_template.yaml` for the standard template.

---

## Technology Stack

| Layer | Tools | Purpose |
|-------|-------|---------|
| Core math | Python 3.11, NumPy, SciPy sparse, NetworkX | GF(2) matrices, graph checks, rank/nullspace |
| QEC circuits | Stim, Sinter, Qiskit | Fast stabilizer circuits, DEMs, framework compat |
| Decoding | PyMatching, ldpc (BP-OSD) | MWPM for surface codes; BP-OSD for qLDPC/BB |
| Optimization | SciPy MILP / HiGHS | Small-n exact distance verification |
| Quality | pytest, ruff, black | Reusable package discipline |
| Reporting | Jupyter, matplotlib, pandas | Tables, plots, reproducible experiments |

---

## Target Deliverables

| Deliverable | Description |
|-------------|-------------|
| GitHub package | Clean Python package with modules for codes, circuits, decoders, simulation, plots, examples |
| Technical report | 6–10 page report: methods, experiments, plots, limitations, future work |
| Reproducible notebooks | Surface baseline, BB reproduction, decoder comparison, circuit-level memory, FT gadget demo |
| Plots | LER vs p, pseudo-thresholds, decoder comparison, distance/FOM tables |
| Interview notes | Stabilizer formalism, CSS conditions, DEMs, decoding, thresholds, magic states, code surgery |

---

## Resume Bullets (What This Builds)

- Built end-to-end QEC simulation toolkit in Python for stabilizer/CSS codes: GF(2) rank/nullspace, logical-operator checks, parity-check validation.
- Implemented logical memory experiments with detector error models and MWPM decoding → logical-error-rate and pseudo-threshold plots under circuit-level noise.
- Reproduced bivariate bicycle/qLDPC code construction from polynomial parity-check matrices; compared decoder-based distance estimates with MILP verification.
- Developed prototype FTQC gadgets: logical state prep, logical measurement, magic-state resource-estimation module.
- Packaged as reproducible notebooks with documented APIs, tests, and configuration-driven simulations.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
