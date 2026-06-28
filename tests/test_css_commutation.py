"""
Tests for CSS code construction and commutation validation.
"""

import numpy as np
import pytest

from qec_toolkit.codes.base import CSSCode
from qec_toolkit.codes.steane import make_steane_code


class TestCSSCodeConstruction:
    """CSSCode can be instantiated and basic properties accessed."""

    def test_csscode_instantiation(self):
        hx = np.array([[1, 0, 1, 0]], dtype=np.uint8)
        hz = np.array([[0, 1, 0, 1]], dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz, name="test_code")
        assert code.name == "test_code"

    def test_csscode_n_property(self):
        hx = np.zeros((2, 7), dtype=np.uint8)
        hz = np.zeros((3, 7), dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz)
        assert code.n == 7

    def test_csscode_r_x_r_z(self):
        hx = np.zeros((2, 7), dtype=np.uint8)
        hz = np.zeros((3, 7), dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz)
        assert code.r_x == 2
        assert code.r_z == 3

    def test_csscode_dtype_coercion(self):
        hx = np.array([[1, 0, 1]], dtype=int)
        hz = np.array([[0, 1, 0]], dtype=float)
        code = CSSCode(hx=hx, hz=hz)
        assert code.hx.dtype == np.uint8
        assert code.hz.dtype == np.uint8

    def test_mismatched_width_raises(self):
        hx = np.zeros((1, 3), dtype=np.uint8)
        hz = np.zeros((1, 4), dtype=np.uint8)
        with pytest.raises(ValueError):
            CSSCode(hx=hx, hz=hz)


class TestCSSCommutationCondition:
    """``H_X @ H_Z.T = 0 mod 2`` must hold for valid CSS codes."""

    def test_valid_css_code_passes_validate(self):
        hx = np.array([[1, 1, 0, 0]], dtype=np.uint8)
        hz = np.array([[0, 0, 1, 1]], dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz, name="valid_example")
        code.validate()

    def test_invalid_css_code_fails_validate(self):
        hx = np.array([[1, 0]], dtype=np.uint8)
        hz = np.array([[1, 0]], dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz, name="invalid_example")
        with pytest.raises(AssertionError):
            code.validate()

    def test_is_valid_returns_bool(self):
        hx_good = np.array([[1, 1, 0, 0]], dtype=np.uint8)
        hz_good = np.array([[0, 0, 1, 1]], dtype=np.uint8)
        assert CSSCode(hx=hx_good, hz=hz_good).is_valid() is True

        hx_bad = np.array([[1, 0]], dtype=np.uint8)
        hz_bad = np.array([[1, 0]], dtype=np.uint8)
        assert CSSCode(hx=hx_bad, hz=hz_bad).is_valid() is False

    def test_zero_check_matrix_always_valid(self):
        hx = np.zeros((2, 5), dtype=np.uint8)
        hz = np.ones((3, 5), dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz)
        assert code.is_valid() is True


class TestCSSCodeK:
    """Tests for number of logical qubits ``k``."""

    def test_repetition_code_k_equals_1(self):
        hz = np.array([[1, 1, 0], [0, 1, 1]], dtype=np.uint8)
        hx = np.zeros((0, 3), dtype=np.uint8)
        code = CSSCode(hx=hx, hz=hz, name="3-qubit repetition")
        assert code.k == 1

    def test_steane_code_k_equals_1(self):
        code = make_steane_code()
        assert code.k == 1
