# Coding Standards & Project Rules
# Circuit-Level QEC / FTQC Portfolio Project

## 1. Code Style

- **Formatter:** `black` (line length 100). Run `black qec_toolkit/ tests/` before every commit.
- **Linter:** `ruff` (run `ruff check .`). Fix all `E` and `F` errors; `W` warnings are advisory.
- **Type hints:** Add type annotations to all public functions. Not required for private helpers in early phases, but required before Phase 7 cleanup.
- **Docstrings:** Every public function/class must have a one-line summary. Complex functions get a full NumPy-style docstring with `Parameters`, `Returns`, and `Notes` sections.

## 2. Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Modules | `snake_case.py` | `gf2.py`, `ler_curves.py` |
| Classes | `PascalCase` | `CSSCode`, `MWPMDecoder` |
| Functions | `snake_case` | `gf2_rank()`, `decode_batch()` |
| Constants | `UPPER_SNAKE_CASE` | `DEFAULT_SEED = 42` |
| Private | leading underscore | `_row_reduce()` |
| Test files | `test_<module>.py` | `test_gf2.py` |
| Test functions | `test_<description>` | `test_rank_identity_matrix()` |

## 3. GF(2) / NumPy Conventions

- All parity-check matrices are stored as `np.ndarray` with `dtype=np.uint8`.
- Arithmetic over GF(2) is done via `% 2` or `& 1` — never assume implicit modular reduction.
- Sparse matrices (SciPy) are used for large codes (n > 200). Dense numpy arrays are fine for small test cases.
- Document matrix shapes in docstrings: `shape (r_x, n)` for H_X etc.

## 4. Reproducibility Rules (MANDATORY for every experiment)

Every simulation/experiment MUST have:

```
configs/<experiment_name>.yaml    ← All parameters + random seed
data/<experiment_name>_results.csv ← Raw numerical results
data/<experiment_name>_plot.png   ← Plot image
examples/<NN>_<experiment_name>.ipynb ← Notebook that reproduces all results
```

Use `configs/experiment_template.yaml` as the starting point.  
Always set `seed: <integer>` in config and pass it to numpy RNG.  
Never hard-code magic numbers in scripts — they belong in the config.

## 5. Testing Rules

- Write tests BEFORE committing implementation code (TDD encouraged).
- Every mathematical claim must have a test:  
  - `H_X @ H_Z.T % 2 == 0` for every CSS code you construct.  
  - `A @ v % 2 == 0` for every nullspace vector you compute.  
  - `n, k, d` for every reference code (repetition, Steane) match known values.
- Run `pytest tests/ -v` before every commit. All tests must pass.
- Use `pytest.mark.slow` for tests that take >5 seconds (MILP, large sims).

## 6. Git Commit Rules

- Commits are small and atomic. One logical change per commit.
- Commit message format: `[phase] short description`
  - Example: `[phase0] add README and project structure`
  - Example: `[phase1] implement gf2_rank with pivot tracking`
- Tag milestones: `git tag v0.1-phase0-done` etc.
- **Never commit:** `.venv/`, `__pycache__/`, `*.pyc`, `data/*.csv` (only configs and plot PNGs), `.ipynb_checkpoints/`.

## 7. Import Ordering

```python
# 1. Standard library
import os
from dataclasses import dataclass
from typing import Optional

# 2. Third-party
import numpy as np
import scipy.sparse as sp

# 3. Local package
from qec_toolkit.verification.gf2 import gf2_rank
```

Use `ruff` with `I` rules to enforce this automatically.

## 8. What "Definition of Done" Means

A phase is done when ALL of the following are true:
- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Ruff and black pass with zero errors
- [ ] Every new module has docstrings on public API
- [ ] At least one reproducible example notebook exists
- [ ] A config YAML exists for every simulation
- [ ] Results are saved to `data/` as CSV
- [ ] Git commit tagged with phase completion

## 9. Interview-Readiness Rule

Every module should be explainable in 2 minutes without code. If you cannot explain what `gf2_rank()` does, why `validate_css()` checks `H_X @ H_Z.T`, or what a "detector" is in Stim — write it in the docstring/notebook before moving on.
