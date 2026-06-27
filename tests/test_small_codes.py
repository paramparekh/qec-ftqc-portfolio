"""
tests/test_small_codes.py
==========================
Tests for reference code implementations: repetition code, Steane code.
Phase 1 target: qec_toolkit/codes/repetition.py, steane.py

Phase 0 status: All tests are xfail / skip — they define Phase 1's contract.

Known correct parameters to verify:
  3-qubit repetition: n=3, k=1, d=3 (corrects 1 bit flip)
  5-qubit perfect code: n=5, k=1, d=3
  [[7,1,3]] Steane code: n=7, k=1, d=3
"""

import numpy as np
import pytest


@pytest.mark.xfail(reason="repetition.py not implemented — Phase 1", strict=False)
class TestRepetitionCode:
    """Tests for 3-qubit repetition code."""

    def test_import(self):
        from qec_toolkit.codes.repetition import make_repetition_code  # noqa: F401

    def test_n_k_d_parameters(self):
        from qec_toolkit.codes.repetition import make_repetition_code
        code = make_repetition_code(n=3)
        assert code.n == 3
        assert code.k == 1
        # distance verified after Phase 1 implementation

    def test_css_condition_holds(self):
        from qec_toolkit.codes.repetition import make_repetition_code
        code = make_repetition_code(n=3)
        code.validate()  # H_X @ H_Z.T = 0 mod 2

    def test_hz_checks_adjacent_qubits(self):
        """Z-check matrix should check neighboring qubit pairs."""
        from qec_toolkit.codes.repetition import make_repetition_code
        code = make_repetition_code(n=3)
        # H_Z should be [[1,1,0],[0,1,1]]
        expected_hz = np.array([[1, 1, 0], [0, 1, 1]], dtype=np.uint8)
        np.testing.assert_array_equal(code.hz, expected_hz)


@pytest.mark.xfail(reason="steane.py not implemented — Phase 1", strict=False)
class TestSteaneCode:
    """Tests for [[7,1,3]] Steane code."""

    def test_import(self):
        from qec_toolkit.codes.steane import make_steane_code  # noqa: F401

    def test_n_k_parameters(self):
        from qec_toolkit.codes.steane import make_steane_code
        code = make_steane_code()
        assert code.n == 7
        assert code.k == 1
        assert code.r_x == 3
        assert code.r_z == 3

    def test_css_condition_holds(self):
        from qec_toolkit.codes.steane import make_steane_code
        code = make_steane_code()
        code.validate()

    def test_check_weight(self):
        """Each check in Steane code has weight 4."""
        from qec_toolkit.codes.steane import make_steane_code
        code = make_steane_code()
        for row in code.hx:
            assert row.sum() == 4
        for row in code.hz:
            assert row.sum() == 4
