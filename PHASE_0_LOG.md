# Phase 0 Progress Log

**Phase:** 0 — Project Kickoff & Scope Control  
**Timeline:** Week 0  
**Status:** ✅ COMPLETE

---

## Definition of Done Checklist

- [x] Repository folder structure created
- [x] README has project goal and one-paragraph abstract
- [x] Environment setup: Python venv (no conda) + `setup_env.ps1`
- [x] `pyproject.toml` with all dependencies defined
- [x] Coding standards document (`CODING_STANDARDS.md`) written
- [x] Reproducibility rules documented (experiment template YAML)
- [x] Issue board template created (`.github/ISSUE_TEMPLATE/`)
- [x] First test suite runs (`pytest tests/ -v`)
- [x] `CSSCode` dataclass skeleton created (`qec_toolkit/codes/base.py`)
- [x] `gf2.py` skeleton created with docstrings and Phase 1 TODOs
- [x] All test files created with proper xfail markers

---

## What Was Done

### Folder Structure
```
qec-ftqc-portfolio/
├── qec_toolkit/{codes,verification,circuits,decoders,simulation,plots,utils}/
├── examples/
├── reports/
├── tests/
├── data/
├── configs/
└── .github/ISSUE_TEMPLATE/
```

### Files Created
| File | Purpose |
|------|---------|
| `README.md` | Project title, abstract, setup guide, 24-week roadmap |
| `pyproject.toml` | Package config, all dependencies, tooling settings |
| `CODING_STANDARDS.md` | Style, testing, reproducibility, git rules |
| `configs/experiment_template.yaml` | Every experiment must copy this template |
| `qec_toolkit/__init__.py` | Package metadata |
| `qec_toolkit/codes/base.py` | `CSSCode` dataclass with `validate()`, `k`, `n`, `summary()` |
| `qec_toolkit/verification/gf2.py` | Skeleton for `gf2_rank`, `gf2_nullspace`, `symplectic_inner` |
| `tests/test_gf2.py` | Full contract tests for GF(2) (xfail until Phase 1) |
| `tests/test_css_commutation.py` | CSS validation tests — some run NOW in Phase 0 |
| `tests/test_small_codes.py` | Repetition/Steane tests (xfail until Phase 1) |
| `tests/test_bb_parameters.py` | BB code tests incl. [[72,12,6]] (xfail until Phase 3) |
| `setup_env.ps1` | One-command setup using Python venv |
| `.gitignore` | Excludes venv, pycache, large CSVs |
| `LICENSE` | MIT license |
| `reports/final_report.md` | Report skeleton to fill during Phases 2-7 |

### Scope Decisions (Locked)
- **Flagship result:** Circuit-level logical memory experiments for surface + BB codes
- **Baselines:** Repetition code, Steane code, rotated surface code (d=3,5,7)
- **Advanced:** Bivariate bicycle / qLDPC codes (BB construction + MILP distance)
- **Differentiator:** FT gadget demo (logical state prep, logical CNOT, magic-state estimator)
- **No conda** — using Python `venv` exclusively

---

## Next Steps: Phase 1 — GF(2) Engine (Weeks 1-3)

| Day | Task |
|-----|------|
| Day 2 | Implement `gf2_rank()` with pivot tracking → all `TestGF2Rank` tests pass |
| Day 3 | Implement `gf2_rref()` → row-reduced echelon form |
| Day 4 | Implement `gf2_nullspace()` + `gf2_in_rowspace()` → kernel tests pass |
| Day 5 | Implement `symplectic_inner()` → X/Z commutation tests pass |
| Day 6 | Implement `CSSCode.k` with real GF(2) rank → `test_css_commutation.py` passes |
| Day 7 | Implement Steane + repetition codes → `test_small_codes.py` passes |
| Day 8 | Write notebook `01_gf2_stabilizer_basics.ipynb` explaining everything |
