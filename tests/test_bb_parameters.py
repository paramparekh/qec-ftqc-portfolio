"""
tests/test_bb_parameters.py
============================
Tests for bivariate bicycle (BB) code construction and parameter verification.
Phase 3 target: qec_toolkit/codes/bb.py

Phase 0 status: All tests are xfail — they define Phase 3's contract.

Key facts about BB codes:
  - Defined by two polynomials A(x,y) and B(x,y) over Z_l × Z_m cyclic groups.
  - H_X = [A, B],  H_Z = [B^T, A^T]
  - By construction: H_X @ H_Z.T = A B^T + B A^T = 0 mod 2 (if AB^T = BA^T)
  - n = 2lm, k computed from ranks.
  - FOM (figure of merit) = k * d^2 / n (higher is better).

Famous example from the IBM paper:
  l=6, m=6, A=1+x+x^2, B=1+y+y^2 → [[72, 12, 6]] code.
"""

import pytest


@pytest.mark.xfail(reason="bb.py not implemented — Phase 3", strict=False)
class TestBBCodeConstruction:
    """Tests for BB code parity-check matrix construction."""

    def test_import(self):
        from qec_toolkit.codes.bb import bb_css_code  # noqa: F401

    def test_css_condition_holds(self):
        """BB codes must always satisfy H_X @ H_Z.T = 0 mod 2 by construction."""
        from qec_toolkit.codes.bb import bb_css_code

        # Simple example: l=3, m=3
        A_terms = [(0, 0), (1, 0)]  # A = 1 + x
        B_terms = [(0, 0), (0, 1)]  # B = 1 + y
        code = bb_css_code(l=3, m=3, A_terms=A_terms, B_terms=B_terms)
        code.validate()

    def test_n_formula(self):
        """n = 2 * l * m."""
        from qec_toolkit.codes.bb import bb_css_code

        ell, m = 4, 5
        A_terms = [(0, 0), (1, 0)]
        B_terms = [(0, 0), (0, 1)]
        code = bb_css_code(l=ell, m=m, A_terms=A_terms, B_terms=B_terms)
        assert code.n == 2 * ell * m

    def test_known_bb_72_12_6_parameters(self):
        """
        Reproduce the [[72, 12, 6]] BB code from the IBM paper.
        l=6, m=6, A=1+x+x^2, B=1+y+y^2.

        This is the key validation for Phase 3.
        n=72, k=12, d=6, FOM = 12*36/72 = 6.0
        """
        from qec_toolkit.codes.bb import bb_css_code

        A_terms = [(0, 0), (1, 0), (2, 0)]  # 1 + x + x^2
        B_terms = [(0, 0), (0, 1), (0, 2)]  # 1 + y + y^2
        code = bb_css_code(l=6, m=6, A_terms=A_terms, B_terms=B_terms)
        assert code.n == 72
        assert code.k == 12
        # Distance d=6 verified via MILP in Phase 3
