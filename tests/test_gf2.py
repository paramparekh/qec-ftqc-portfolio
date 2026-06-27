"""
tests/test_gf2.py
==================
Tests for the GF(2) linear algebra engine.
Phase 1 implementation target: qec_toolkit/verification/gf2.py

Phase 0 status: All tests are MARKED TO SKIP until Phase 1 is implemented.
                The tests exist so the test suite is runnable from Day 0.

These tests define the CONTRACT that gf2.py must satisfy.
Write the implementation to make every test pass.

Test coverage required (Phase 1):
  - gf2_rank:    identity, zero, full-rank random, rank-deficient, mod-2 check
  - gf2_nullspace: nullspace vectors actually in kernel, dimension check
  - gf2_rref:    correct pivot columns, correct echelon form
  - gf2_in_rowspace: membership and non-membership examples
  - symplectic_inner: X/Z anticommute, X/I commute, Z/Z commute
"""

import numpy as np
import pytest

# We import at module level; tests will be xfail until Phase 1 implements the functions.
from qec_toolkit.verification.gf2 import (
    gf2_nullspace,
    gf2_rank,
    symplectic_inner,
)

# ══════════════════════════════════════════════════════════════════════════════
# gf2_rank tests
# ══════════════════════════════════════════════════════════════════════════════

class TestGF2Rank:
    """Tests for gf2_rank(). All should pass after Phase 1, Day 2."""

    def test_rank_identity_3x3(self):
        """Identity matrix of size n has rank n over any field."""
        a = np.eye(3, dtype=np.uint8)
        assert gf2_rank(a) == 3

    def test_rank_identity_5x5(self):
        a = np.eye(5, dtype=np.uint8)
        assert gf2_rank(a) == 5

    def test_rank_zero_matrix(self):
        """Zero matrix has rank 0."""
        a = np.zeros((4, 4), dtype=np.uint8)
        assert gf2_rank(a) == 0

    def test_rank_full_row_rank_non_square(self):
        """Matrix with 3 independent rows has rank 3."""
        a = np.array([
            [1, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 1],
        ], dtype=np.uint8)
        assert gf2_rank(a) == 3

    def test_rank_repeated_row(self):
        """Duplicating a row does not increase rank over GF(2)."""
        a = np.array([
            [1, 1, 0],
            [1, 1, 0],  # duplicate
            [0, 0, 1],
        ], dtype=np.uint8)
        assert gf2_rank(a) == 2

    def test_rank_gf2_not_real_rank(self):
        """
        Over GF(2), rank differs from real-valued rank for some matrices.
        Example: [1,1; 1,1] has real rank 1 AND GF(2) rank 1.
        But [1,1,0; 0,1,1; 1,0,1] has real rank 3 but GF(2) rank 2
        because rows sum to 0 over GF(2).
        """
        a = np.array([
            [1, 1, 0],
            [0, 1, 1],
            [1, 0, 1],  # = row0 XOR row1 over GF(2)
        ], dtype=np.uint8)
        assert gf2_rank(a) == 2  # NOT 3 — this is the GF(2) case!

    def test_rank_single_row(self):
        a = np.array([[1, 0, 1, 1]], dtype=np.uint8)
        assert gf2_rank(a) == 1

    def test_rank_accepts_int_values(self):
        """Should handle inputs that are integers 0 and 1, not just uint8."""
        a = np.array([[1, 0], [0, 1]])
        assert gf2_rank(a) == 2


# ══════════════════════════════════════════════════════════════════════════════
# gf2_nullspace tests
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.xfail(reason="Phase 1 not implemented yet", strict=False)
class TestGF2Nullspace:
    """Tests for gf2_nullspace(). Phase 1, Day 4."""

    def test_nullspace_vectors_in_kernel(self):
        """Every basis vector of the nullspace must satisfy A @ v = 0 mod 2."""
        a = np.array([
            [1, 0, 1, 0],
            [0, 1, 1, 0],
        ], dtype=np.uint8)
        null_basis = gf2_nullspace(a)
        for v in null_basis:
            result = (a @ v) % 2
            assert np.all(result == 0), f"Nullspace vector {v} not in kernel!"

    def test_nullspace_dimension(self):
        """dim(null) = n - rank(A) by rank-nullity theorem."""
        a = np.array([
            [1, 0, 1, 0],
            [0, 1, 1, 0],
        ], dtype=np.uint8)
        n = a.shape[1]
        rank = gf2_rank(a)
        null_basis = gf2_nullspace(a)
        assert null_basis.shape[0] == n - rank

    def test_nullspace_identity_is_trivial(self):
        """Nullspace of full-rank square matrix is empty (no free variables)."""
        a = np.eye(3, dtype=np.uint8)
        null_basis = gf2_nullspace(a)
        assert null_basis.shape[0] == 0


# ══════════════════════════════════════════════════════════════════════════════
# symplectic_inner tests
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.xfail(reason="Phase 1 not implemented yet", strict=False)
class TestSymplecticInner:
    """Tests for symplectic_inner(). Phase 1, Day 5."""

    def test_x_and_z_same_qubit_anticommute(self):
        """X and Z on the same qubit anticommute: <X_0, Z_0>_s = 1."""
        # 2 qubits: p = (x|z) = [x0, x1, z0, z1]
        # X on qubit 0: x0=1, rest=0
        X0 = np.array([1, 0, 0, 0])
        # Z on qubit 0: z0=1, rest=0
        Z0 = np.array([0, 0, 1, 0])
        assert symplectic_inner(X0, Z0) == 1

    def test_x_and_z_different_qubits_commute(self):
        """X on qubit 0 and Z on qubit 1 commute: <X_0, Z_1>_s = 0."""
        X0 = np.array([1, 0, 0, 0])
        Z1 = np.array([0, 0, 0, 1])
        assert symplectic_inner(X0, Z1) == 0

    def test_x_and_x_commute(self):
        """X and X always commute."""
        X0 = np.array([1, 0, 0, 0])
        X1 = np.array([0, 1, 0, 0])
        assert symplectic_inner(X0, X0) == 0
        assert symplectic_inner(X0, X1) == 0

    def test_z_and_z_commute(self):
        """Z and Z always commute."""
        Z0 = np.array([0, 0, 1, 0])
        Z1 = np.array([0, 0, 0, 1])
        assert symplectic_inner(Z0, Z0) == 0
        assert symplectic_inner(Z0, Z1) == 0
