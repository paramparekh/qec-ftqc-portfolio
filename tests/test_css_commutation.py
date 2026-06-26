"""
tests/test_css_commutation.py
==============================
Tests for CSS code validation: the commutation condition H_X @ H_Z.T = 0 mod 2.

Phase 0 status: CSSCode.validate() is importable and structurally correct.
                Some tests run now; others are xfail pending Phase 1 GF(2) rank.

These tests verify:
  1. CSSCode object construction works (Phase 0 ✓)
  2. validate() correctly catches invalid CSS codes (Phase 0 ✓)
  3. k computation is correct (Phase 1 — xfail until gf2_rank is implemented)
"""

import numpy as np
import pytest

from qec_toolkit.codes.base import CSSCode


# ══════════════════════════════════════════════════════════════════════════════
# Phase 0 tests — run NOW (no NotImplementedError)
# ══════════════════════════════════════════════════════════════════════════════

class TestCSSCodeConstruction:
    """CSSCode can be instantiated and basic properties accessed."""

    def test_cssode_instantiation(self):
        """CSSCode can be constructed with numpy arrays."""
        hx = np.array([[1, 0, 1, 0]], dtype=np.uint8)
        hz = np.array([[0, 1, 0, 1]], dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz, name="test_code")
        assert code.name == "test_code"

    def test_cssode_n_property(self):
        """n = number of columns of H_X."""
        hx = np.zeros((2, 7), dtype=np.uint8)
        hz = np.zeros((3, 7), dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz)
        assert code.n == 7

    def test_cssode_r_x_r_z(self):
        """r_x and r_z count the rows of H_X and H_Z."""
        hx = np.zeros((2, 7), dtype=np.uint8)
        hz = np.zeros((3, 7), dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz)
        assert code.r_x == 2
        assert code.r_z == 3

    def test_cssode_dtype_coercion(self):
        """CSSCode should coerce inputs to uint8."""
        hx = np.array([[1, 0, 1]], dtype=int)
        hz = np.array([[0, 1, 0]], dtype=float)
        code = CSSCode(hx=hx, hz=hz)
        assert code.hx.dtype == np.uint8
        assert code.hz.dtype == np.uint8


class TestCSSCommutationCondition:
    """H_X @ H_Z.T = 0 mod 2 must hold for valid CSS codes."""

    def test_valid_css_code_passes_validate(self):
        """
        A valid CSS code: H_X @ H_Z.T = 0.
        Example: H_X = [[1,1,0,0]], H_Z = [[0,0,1,1]]
        Product = 0 (no overlap) → valid.
        """
        hx = np.array([[1, 1, 0, 0]], dtype=np.uint8)
        hz = np.array([[0, 0, 1, 1]], dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz, name="valid_example")
        code.validate()  # Should not raise

    def test_invalid_css_code_fails_validate(self):
        """
        An invalid CSS code: H_X @ H_Z.T ≠ 0.
        H_X = [[1,0]], H_Z = [[1,0]] → product = 1 mod 2 → INVALID.
        """
        hx = np.array([[1, 0]], dtype=np.uint8)
        hz = np.array([[1, 0]], dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz, name="invalid_example")
        with pytest.raises(AssertionError):
            code.validate()

    def test_is_valid_returns_bool(self):
        """is_valid() returns True for valid, False for invalid."""
        hx_good = np.array([[1, 1, 0, 0]], dtype=np.uint8)
        hz_good = np.array([[0, 0, 1, 1]], dtype=np.uint8)
        assert CSSCode(hx=hx_good, hz=hz_good).is_valid() is True

        hx_bad = np.array([[1, 0]], dtype=np.uint8)
        hz_bad = np.array([[1, 0]], dtype=np.uint8)
        assert CSSCode(hx=hx_bad, hz=hz_bad).is_valid() is False

    def test_zero_check_matrix_always_valid(self):
        """Zero H_X always satisfies H_X @ H_Z.T = 0 trivially."""
        hx = np.zeros((2, 5), dtype=np.uint8)
        hz = np.ones((3, 5), dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz)
        assert code.is_valid() is True


# ══════════════════════════════════════════════════════════════════════════════
# Phase 1 tests — xfail until gf2_rank is implemented
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.xfail(reason="k property uses gf2_rank — implement in Phase 1", strict=False)
class TestCSSCodeK:
    """Tests for number of logical qubits k. Requires Phase 1 gf2_rank."""

    def test_repetition_code_k_equals_1(self):
        """
        3-qubit repetition code (bit-flip): H_Z = [[1,1,0],[0,1,1]], H_X = zeros.
        n=3, rank(H_Z)=2, rank(H_X)=0 → k = 3 - 2 - 0 = 1.
        """
        hz = np.array([[1, 1, 0], [0, 1, 1]], dtype=np.uint8)
        hx = np.zeros((1, 3), dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz, name="3-qubit repetition")
        assert code.k == 1

    def test_steane_code_k_equals_1(self):
        """
        [[7,1,3]] Steane code. k should be 1.
        H_X and H_Z are each 3x7 matrices with rank 3.
        k = 7 - 3 - 3 = 1.
        (Values filled in Phase 1 when Steane code is constructed.)
        """
        pytest.skip("Steane code construction is Phase 1 work")
