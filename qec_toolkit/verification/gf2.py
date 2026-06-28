"""
qec_toolkit.verification.gf2
============================
GF(2) linear algebra engine for stabilizer and CSS-code calculations.

GF(2) is the binary field {0, 1}, where addition is XOR. All routines in this
module reduce inputs modulo 2 and return ``np.uint8`` arrays where appropriate.

Key uses in this project
------------------------
- ``gf2_rank(H)`` computes stabilizer-check rank.
- ``gf2_nullspace(H)`` finds vectors that commute with a CSS check matrix.
- ``gf2_in_rowspace(H, v)`` tests whether a candidate operator is a stabilizer.
- ``symplectic_inner(p, q)`` tests binary Pauli commutation.
"""

from __future__ import annotations

import numpy as np


def _as_binary_matrix(a: np.ndarray) -> np.ndarray:
    """Return a copy of ``a`` reduced modulo 2 with dtype ``np.uint8``."""
    matrix = np.asarray(a)
    if matrix.ndim != 2:
        raise ValueError(f"expected a 2D matrix, got shape {matrix.shape}")
    return (matrix.copy() % 2).astype(np.uint8)


def _as_binary_vector(v: np.ndarray) -> np.ndarray:
    """Return a copy of ``v`` reduced modulo 2 with dtype ``np.uint8``."""
    vector = np.asarray(v)
    if vector.ndim != 1:
        raise ValueError(f"expected a 1D vector, got shape {vector.shape}")
    return (vector.copy() % 2).astype(np.uint8)


def gf2_rref(a: np.ndarray) -> tuple[np.ndarray, list[int]]:
    """
    Return the row-reduced echelon form of ``a`` over GF(2).

    Parameters
    ----------
    a : np.ndarray
        Binary matrix, shape ``(m, n)``.

    Returns
    -------
    rref : np.ndarray
        Row-reduced echelon form of ``a`` over GF(2), shape ``(m, n)``.
    pivot_cols : list[int]
        Pivot-column indices. The length of this list is the GF(2) rank.

    Notes
    -----
    This is Gaussian elimination over GF(2): row addition is XOR, and every
    pivot column is cleared above and below the pivot row.
    """
    rref = _as_binary_matrix(a)
    m, n = rref.shape
    pivot_cols: list[int] = []
    pivot_row = 0

    for col in range(n):
        pivot_candidates = np.flatnonzero(rref[pivot_row:, col])
        if pivot_candidates.size == 0:
            continue

        pivot = pivot_row + int(pivot_candidates[0])
        if pivot != pivot_row:
            rref[[pivot_row, pivot]] = rref[[pivot, pivot_row]]

        rows_to_eliminate = np.flatnonzero(rref[:, col])
        for row in rows_to_eliminate:
            if row != pivot_row:
                rref[row] ^= rref[pivot_row]

        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == m:
            break

    return rref, pivot_cols


def gf2_rank(a: np.ndarray) -> int:
    """
    Return the rank of matrix ``a`` over GF(2).

    Parameters
    ----------
    a : np.ndarray
        Binary matrix, shape ``(m, n)``. Values are reduced modulo 2.

    Returns
    -------
    int
        Number of linearly independent rows over GF(2).
    """
    _, pivot_cols = gf2_rref(a)
    return len(pivot_cols)


def gf2_nullspace(a: np.ndarray) -> np.ndarray:
    """
    Return a row-basis for the nullspace of ``a`` over GF(2).

    Parameters
    ----------
    a : np.ndarray
        Binary matrix, shape ``(m, n)``.

    Returns
    -------
    np.ndarray
        Matrix of shape ``(dim_null, n)``. Each row is a basis vector ``v`` with
        ``a @ v % 2 == 0``. If the nullspace is trivial, the shape is ``(0, n)``.

    Notes
    -----
    For each free column in the RREF, set that free variable to 1 and all other
    free variables to 0, then read pivot variables from the RREF equations.
    """
    matrix = _as_binary_matrix(a)
    _, n = matrix.shape
    rref, pivot_cols = gf2_rref(matrix)
    pivot_set = set(pivot_cols)
    free_cols = [col for col in range(n) if col not in pivot_set]

    if not free_cols:
        return np.zeros((0, n), dtype=np.uint8)

    basis = np.zeros((len(free_cols), n), dtype=np.uint8)
    for basis_row, free_col in enumerate(free_cols):
        vector = basis[basis_row]
        vector[free_col] = 1
        for row, pivot_col in enumerate(pivot_cols):
            vector[pivot_col] = rref[row, free_col]

    return basis


def gf2_in_rowspace(a: np.ndarray, v: np.ndarray) -> bool:
    """
    Return whether ``v`` lies in the row span of ``a`` over GF(2).

    Parameters
    ----------
    a : np.ndarray
        Binary matrix, shape ``(m, n)``.
    v : np.ndarray
        Binary vector, shape ``(n,)``.

    Returns
    -------
    bool
        ``True`` if ``v`` is a GF(2) linear combination of rows of ``a``.

    Notes
    -----
    Appending ``v`` as one extra row cannot increase rank exactly when ``v`` is
    already in the row span.
    """
    matrix = _as_binary_matrix(a)
    vector = _as_binary_vector(v)
    if matrix.shape[1] != vector.shape[0]:
        raise ValueError(
            f"matrix has {matrix.shape[1]} columns, but vector has length {vector.shape[0]}"
        )

    if matrix.shape[0] == 0:
        return bool(np.all(vector == 0))

    augmented = np.vstack([matrix, vector])
    return gf2_rank(augmented) == gf2_rank(matrix)


def symplectic_inner(p: np.ndarray, q: np.ndarray) -> int:
    """
    Compute the binary symplectic inner product of two Pauli vectors.

    A Pauli on ``n`` qubits is represented as ``(x | z)`` with length ``2n``.
    The symplectic inner product is ``x_p.dot(z_q) + z_p.dot(x_q) mod 2``.
    Two Paulis commute iff this value is 0.

    Parameters
    ----------
    p, q : np.ndarray
        Binary Pauli vectors, both shape ``(2n,)``.

    Returns
    -------
    int
        0 for commuting Paulis, 1 for anticommuting Paulis.
    """
    p_vec = _as_binary_vector(p)
    q_vec = _as_binary_vector(q)
    if p_vec.shape != q_vec.shape:
        raise ValueError(
            f"Pauli vectors must have the same shape, got {p_vec.shape} and {q_vec.shape}"
        )
    if p_vec.shape[0] % 2 != 0:
        raise ValueError("Pauli vectors must have even length 2n")

    n = p_vec.shape[0] // 2
    p_x, p_z = p_vec[:n], p_vec[n:]
    q_x, q_z = q_vec[:n], q_vec[n:]
    return int((np.dot(p_x, q_z) + np.dot(p_z, q_x)) % 2)
