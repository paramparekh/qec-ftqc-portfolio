"""
Tests for the GF(2) linear algebra engine.
"""

import numpy as np
import pytest

from qec_toolkit.verification.gf2 import (
    gf2_in_rowspace,
    gf2_nullspace,
    gf2_rank,
    gf2_rref,
    symplectic_inner,
)


class TestGF2Rank:
    """Tests for ``gf2_rank()``."""

    def test_rank_identity_3x3(self):
        a = np.eye(3, dtype=np.uint8)
        assert gf2_rank(a) == 3

    def test_rank_identity_5x5(self):
        a = np.eye(5, dtype=np.uint8)
        assert gf2_rank(a) == 5

    def test_rank_zero_matrix(self):
        a = np.zeros((4, 4), dtype=np.uint8)
        assert gf2_rank(a) == 0

    def test_rank_full_row_rank_non_square(self):
        a = np.array(
            [
                [1, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 1],
            ],
            dtype=np.uint8,
        )
        assert gf2_rank(a) == 3

    def test_rank_repeated_row(self):
        a = np.array(
            [
                [1, 1, 0],
                [1, 1, 0],
                [0, 0, 1],
            ],
            dtype=np.uint8,
        )
        assert gf2_rank(a) == 2

    def test_rank_gf2_not_real_rank(self):
        a = np.array(
            [
                [1, 1, 0],
                [0, 1, 1],
                [1, 0, 1],
            ],
            dtype=np.uint8,
        )
        assert gf2_rank(a) == 2

    def test_rank_single_row(self):
        a = np.array([[1, 0, 1, 1]], dtype=np.uint8)
        assert gf2_rank(a) == 1

    def test_rank_accepts_int_values(self):
        a = np.array([[1, 0], [0, 1]])
        assert gf2_rank(a) == 2


class TestGF2RREF:
    """Tests for ``gf2_rref()``."""

    def test_rref_pivots_and_matrix(self):
        a = np.array(
            [
                [1, 1, 0],
                [0, 1, 1],
                [1, 0, 1],
            ],
            dtype=np.uint8,
        )
        rref, pivots = gf2_rref(a)
        expected = np.array(
            [
                [1, 0, 1],
                [0, 1, 1],
                [0, 0, 0],
            ],
            dtype=np.uint8,
        )
        assert pivots == [0, 1]
        np.testing.assert_array_equal(rref, expected)

    def test_rref_does_not_mutate_input(self):
        a = np.array([[1, 1], [1, 0]], dtype=np.uint8)
        original = a.copy()
        gf2_rref(a)
        np.testing.assert_array_equal(a, original)


class TestGF2Nullspace:
    """Tests for ``gf2_nullspace()``."""

    def test_nullspace_vectors_in_kernel(self):
        a = np.array(
            [
                [1, 0, 1, 0],
                [0, 1, 1, 0],
            ],
            dtype=np.uint8,
        )
        null_basis = gf2_nullspace(a)
        for v in null_basis:
            result = (a @ v) % 2
            assert np.all(result == 0), f"nullspace vector {v} is not in the kernel"

    def test_nullspace_dimension(self):
        a = np.array(
            [
                [1, 0, 1, 0],
                [0, 1, 1, 0],
            ],
            dtype=np.uint8,
        )
        n = a.shape[1]
        rank = gf2_rank(a)
        null_basis = gf2_nullspace(a)
        assert null_basis.shape[0] == n - rank

    def test_nullspace_identity_is_trivial(self):
        a = np.eye(3, dtype=np.uint8)
        null_basis = gf2_nullspace(a)
        assert null_basis.shape == (0, 3)


class TestGF2Rowspace:
    """Tests for ``gf2_in_rowspace()``."""

    def test_known_member(self):
        a = np.array([[1, 0, 1], [0, 1, 1]], dtype=np.uint8)
        v = np.array([1, 1, 0], dtype=np.uint8)
        assert gf2_in_rowspace(a, v) is True

    def test_known_non_member(self):
        a = np.array([[1, 0, 1], [0, 1, 1]], dtype=np.uint8)
        v = np.array([0, 0, 1], dtype=np.uint8)
        assert gf2_in_rowspace(a, v) is False

    def test_empty_rowspace_contains_zero_only(self):
        a = np.zeros((0, 3), dtype=np.uint8)
        assert gf2_in_rowspace(a, np.zeros(3, dtype=np.uint8)) is True
        assert gf2_in_rowspace(a, np.array([1, 0, 0], dtype=np.uint8)) is False

    def test_shape_mismatch_raises(self):
        a = np.zeros((2, 3), dtype=np.uint8)
        with pytest.raises(ValueError):
            gf2_in_rowspace(a, np.zeros(4, dtype=np.uint8))


class TestSymplecticInner:
    """Tests for ``symplectic_inner()``."""

    def test_x_and_z_same_qubit_anticommute(self):
        x0 = np.array([1, 0, 0, 0])
        z0 = np.array([0, 0, 1, 0])
        assert symplectic_inner(x0, z0) == 1

    def test_x_and_z_different_qubits_commute(self):
        x0 = np.array([1, 0, 0, 0])
        z1 = np.array([0, 0, 0, 1])
        assert symplectic_inner(x0, z1) == 0

    def test_x_and_x_commute(self):
        x0 = np.array([1, 0, 0, 0])
        x1 = np.array([0, 1, 0, 0])
        assert symplectic_inner(x0, x0) == 0
        assert symplectic_inner(x0, x1) == 0

    def test_z_and_z_commute(self):
        z0 = np.array([0, 0, 1, 0])
        z1 = np.array([0, 0, 0, 1])
        assert symplectic_inner(z0, z0) == 0
        assert symplectic_inner(z0, z1) == 0

    def test_odd_length_raises(self):
        with pytest.raises(ValueError):
            symplectic_inner(np.array([1, 0, 0]), np.array([0, 1, 0]))
