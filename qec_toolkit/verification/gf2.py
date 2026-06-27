"""
qec_toolkit.verification.gf2
==============================
GF(2) linear algebra engine — the mathematical foundation of the entire project.

Status: Phase 0 skeleton — full implementation is the Day 2–4 task in Phase 1.

Why this matters
----------------
All quantum error correction code families (surface, BB, HGP, CSS) reduce to
binary (GF(2)) linear algebra. If this engine is wrong, every downstream
result is unreliable. This is also the fastest way to build interview confidence.

Key concepts
------------
GF(2) = the field with two elements {0, 1} where:
  - Addition  =  XOR  (0+0=0, 0+1=1, 1+1=0)
  - Multiplication = AND

Row reduction over GF(2):
  - Same idea as Gaussian elimination, but subtraction = addition (XOR).
  - Use uint8 arrays and ^ (XOR) operator.
  - Result: row-reduced echelon form (RREF over GF(2)).

Rank: number of nonzero rows in RREF.

Nullspace: vectors v s.t. A @ v ≡ 0 (mod 2).

Interview note:
    Q: How do you compute k for a CSS code?
    A: k = n - rank_GF2(H_X) - rank_GF2(H_Z). This counts the degrees of
       freedom not fixed by either the X or Z stabilizers — these become the
       logical qubit degrees of freedom.

TODO (Phase 1 - Days 2-4):
    [ ] Implement gf2_rank() with pivot column tracking
    [ ] Implement gf2_rref() — row-reduced echelon form
    [ ] Implement gf2_nullspace() — basis for kernel of A
    [ ] Implement gf2_rowspace_membership() — check if vector is in row span
    [ ] Add all unit tests in tests/test_gf2.py
    [ ] Optimize with packed uint64 representation (stretch goal)
"""

from __future__ import annotations

import numpy as np

# ══════════════════════════════════════════════════════════════════════════════
# Phase 0 SKELETON — replace each function body in Phase 1
# ══════════════════════════════════════════════════════════════════════════════


def gf2_rank(a: np.ndarray) -> int:
    """
    Return the rank of matrix ``a`` over GF(2).

    Parameters
    ----------
    a : np.ndarray
        Binary matrix, shape (m, n). Values should be 0 or 1 (uint8 preferred).

    Returns
    -------
    int
        The rank of ``a`` over GF(2), i.e., the number of linearly independent
        rows over the field with two elements.

    Notes
    -----
    Algorithm: Gaussian elimination over GF(2).
    For each column, find a pivot row, swap it up, then XOR it into all other
    rows that have a 1 in that column.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.eye(3, dtype=np.uint8)
    >>> gf2_rank(a)
    3
    >>> z = np.zeros((3, 3), dtype=np.uint8)
    >>> gf2_rank(z)
    0

    Status: SKELETON — implement in Phase 1, Day 2.
    """
    a = (a.copy() % 2).astype(np.uint8)
    m, n = a.shape
    rank = 0
    for col in range(n):
        pivot = None
        for r in range(rank, m):
            if a[r, col]:
                pivot = r
                break
        if pivot is None:
            continue
        if pivot != rank:
            # Swap rows to bring the pivot row to the current rank index
            a[[rank, pivot]] = a[[pivot, rank]]
        for r in range(m):
            if r != rank and a[r, col]:
                # XOR subtraction equivalent in GF(2)
                a[r] ^= a[rank]
        rank += 1
    return rank


def gf2_rref(a: np.ndarray) -> tuple[np.ndarray, list[int]]:
    """
    Return the row-reduced echelon form (RREF) of ``a`` over GF(2).

    Parameters
    ----------
    a : np.ndarray
        Binary matrix, shape (m, n).

    Returns
    -------
    rref : np.ndarray
        The RREF of ``a`` over GF(2).
    pivot_cols : list[int]
        Column indices of the pivot columns (length = rank).

    Status: SKELETON — implement in Phase 1, Day 3.
    """
    raise NotImplementedError("gf2_rref: implement in Phase 1, Day 3")


def gf2_nullspace(a: np.ndarray) -> np.ndarray:
    """
    Return a basis for the nullspace (kernel) of ``a`` over GF(2).

    The nullspace consists of all binary vectors v such that:
      A @ v ≡ 0  (mod 2)

    Parameters
    ----------
    a : np.ndarray
        Binary matrix, shape (m, n).

    Returns
    -------
    np.ndarray
        Matrix of shape (dim_null, n), where each row is a basis vector of
        the nullspace. dim_null = n - rank_GF2(a).

    Notes
    -----
    Algorithm: compute RREF, identify free columns, back-substitute.

    Interview note:
        Logical operators live in the nullspace of the opposite check matrix.
        X-logicals: H_Z @ lx.T ≡ 0 (mod 2)
        Z-logicals: H_X @ lz.T ≡ 0 (mod 2)

    Status: SKELETON — implement in Phase 1, Day 4.
    """
    raise NotImplementedError("gf2_nullspace: implement in Phase 1, Day 4")


def gf2_in_rowspace(a: np.ndarray, v: np.ndarray) -> bool:
    """
    Check whether vector ``v`` lies in the row space of ``a`` over GF(2).

    Parameters
    ----------
    a : np.ndarray
        Binary matrix, shape (m, n).
    v : np.ndarray
        Binary vector, shape (n,).

    Returns
    -------
    bool
        True if v can be written as a GF(2) linear combination of rows of a.

    Status: SKELETON — implement in Phase 1, Day 4.
    """
    raise NotImplementedError("gf2_in_rowspace: implement in Phase 1, Day 4")


def symplectic_inner(p: np.ndarray, q: np.ndarray) -> int:
    """
    Compute the symplectic inner product of two Pauli operators.

    A Pauli on n qubits is represented as a binary vector of length 2n:
      p = (p_x | p_z)  where p_x, p_z are length-n binary vectors.

    The symplectic inner product is:
      <p, q>_s = p_x · q_z + p_z · q_x  (mod 2)

    Two Paulis commute iff their symplectic inner product is 0.

    Parameters
    ----------
    p : np.ndarray
        Binary vector of length 2n, encoding a Pauli as (x_part | z_part).
    q : np.ndarray
        Binary vector of length 2n.

    Returns
    -------
    int
        0 if p and q commute, 1 if they anticommute.

    Examples
    --------
    >>> import numpy as np
    >>> # X on qubit 0:  x=[1,0], z=[0,0]  →  [1,0,0,0]
    >>> X0 = np.array([1,0,0,0])
    >>> # Z on qubit 0:  x=[0,0], z=[1,0]  →  [0,0,1,0]
    >>> Z0 = np.array([0,0,1,0])
    >>> symplectic_inner(X0, Z0)
    1   # anticommute — correct!
    >>> # X on qubit 0 vs Z on qubit 1:
    >>> Z1 = np.array([0,0,0,1])
    >>> symplectic_inner(X0, Z1)
    0   # commute — correct!

    Status: SKELETON — implement in Phase 1, Day 5.
    """
    raise NotImplementedError("symplectic_inner: implement in Phase 1, Day 5")
