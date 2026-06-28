"""
Tests for Phase 1 reference code implementations.
"""

import numpy as np
import pytest

from qec_toolkit.codes.repetition import make_repetition_code
from qec_toolkit.codes.steane import make_steane_code


class TestRepetitionCode:
    """Tests for the bit-flip repetition code."""

    def test_n_k_d_parameters(self):
        code = make_repetition_code(n=3)
        assert code.n == 3
        assert code.k == 1
        assert code.distance == 3

    def test_css_condition_holds(self):
        code = make_repetition_code(n=3)
        code.validate()

    def test_hz_checks_adjacent_qubits(self):
        code = make_repetition_code(n=3)
        expected_hz = np.array([[1, 1, 0], [0, 1, 1]], dtype=np.uint8)
        np.testing.assert_array_equal(code.hz, expected_hz)

    def test_general_odd_length(self):
        code = make_repetition_code(n=5)
        assert code.n == 5
        assert code.k == 1
        assert code.distance == 5
        assert code.hz.shape == (4, 5)

    def test_invalid_length_raises(self):
        with pytest.raises(ValueError):
            make_repetition_code(n=1)


class TestSteaneCode:
    """Tests for the [[7,1,3]] Steane code."""

    def test_n_k_d_parameters(self):
        code = make_steane_code()
        assert code.n == 7
        assert code.k == 1
        assert code.distance == 3
        assert code.r_x == 3
        assert code.r_z == 3

    def test_css_condition_holds(self):
        code = make_steane_code()
        code.validate()

    def test_check_weight(self):
        code = make_steane_code()
        for row in code.hx:
            assert row.sum() == 4
        for row in code.hz:
            assert row.sum() == 4

    def test_hx_equals_hz(self):
        code = make_steane_code()
        np.testing.assert_array_equal(code.hx, code.hz)
