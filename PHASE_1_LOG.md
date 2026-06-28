# Phase 1 Progress Log

**Phase:** 1 - Stabilizer Algebra and GF(2) Engine  
**Status:** COMPLETE

## Definition of Done Checklist

- [x] `gf2_rank()` uses GF(2) row reduction
- [x] `gf2_rref()` returns RREF and pivot columns
- [x] `gf2_nullspace()` returns a kernel basis
- [x] `gf2_in_rowspace()` checks GF(2) row-span membership
- [x] `symplectic_inner()` checks binary Pauli commutation
- [x] `CSSCode.k` uses real GF(2) rank
- [x] Repetition-code constructor implemented
- [x] Steane-code constructor implemented
- [x] Phase 1 tests are active and passing
- [x] Notebook artifact added: `examples/01_gf2_stabilizer_basics.ipynb`

## What Was Implemented

| File | Purpose |
|------|---------|
| `qec_toolkit/verification/gf2.py` | Dense GF(2) rank, RREF, nullspace, rowspace membership, and symplectic inner product |
| `qec_toolkit/codes/base.py` | `CSSCode` validation and logical-qubit count using GF(2) rank |
| `qec_toolkit/codes/repetition.py` | Length-`n` bit-flip repetition CSS constructor |
| `qec_toolkit/codes/steane.py` | `[[7,1,3]]` Steane CSS constructor |
| `tests/test_gf2.py` | Active tests for all Phase 1 GF(2) routines |
| `tests/test_css_commutation.py` | Active CSS validation and `k` tests |
| `tests/test_small_codes.py` | Active repetition and Steane code tests |
| `examples/01_gf2_stabilizer_basics.ipynb` | Walkthrough notebook for GF(2), commutation, and reference codes |

## Verified Parameters

| Code | Verified |
|------|----------|
| 3-qubit repetition | `n=3`, `k=1`, `d=3`, valid CSS checks |
| 5-qubit repetition | `n=5`, `k=1`, `d=5`, adjacent Z-check shape |
| Steane | `n=7`, `k=1`, `d=3`, `r_x=3`, `r_z=3`, valid CSS checks |

## Test Baseline

```text
42 passed, 4 xfailed
```

The remaining expected failures are Phase 3 bivariate-bicycle code tests.

## Deferred Work

- Logical-operator extraction is still deferred to `qec_toolkit/verification/logicals.py`.
- BB/qLDPC construction remains Phase 3.
- Surface-code circuits, detector error models, and MWPM decoding remain Phase 2.

## Interview Readiness

Phase 1 now supports the core stabilizer algebra explanation:

- GF(2) row reduction gives check-matrix rank.
- Rank-nullity gives kernel dimensions.
- CSS validity is `H_X @ H_Z.T = 0 mod 2`.
- Logical count is `k = n - rank(H_X) - rank(H_Z)`.
- Binary Pauli commutation is the symplectic inner product of `(x | z)` vectors.
