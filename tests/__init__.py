"""
tests/__init__.py
Test suite for qec-ftqc-portfolio.

Test structure (by phase):
  test_gf2.py              – Phase 1: GF(2) linear algebra engine
  test_css_commutation.py  – Phase 1: CSS code validation
  test_small_codes.py      – Phase 1: Reference codes (repetition, Steane)
  test_bb_parameters.py    – Phase 3: Bivariate bicycle code parameters

Run all tests:
  pytest tests/ -v

Run only fast tests (skip MILP and large simulations):
  pytest tests/ -v -m "not slow"
"""
