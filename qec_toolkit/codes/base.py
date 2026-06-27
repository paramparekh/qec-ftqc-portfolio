"""
qec_toolkit.codes.base
=======================
Core data structures for quantum error-correcting codes.

Status: Phase 0 skeleton — full implementation in Phase 1.

Key concepts
------------
CSS code:
    A [[n, k, d]] quantum error-correcting code defined by two binary matrices:
      H_X  (r_x × n)  — X-type parity checks (detect Z errors)
      H_Z  (r_z × n)  — Z-type parity checks (detect X errors)

    CSS commutation condition (MUST hold):
      H_X @ H_Z.T ≡ 0  (mod 2)

    Number of logical qubits:
      k = n - rank_GF2(H_X) - rank_GF2(H_Z)

    Code distance d:
      Minimum Hamming weight of a logical operator not in the stabilizer group.

Interview note:
    Q: How do you verify a CSS code is valid?
    A: Check H_X @ H_Z.T = 0 mod 2. This ensures X and Z stabilizers commute,
       which is required for all stabilizer codes to have well-defined syndromes.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


# ── Placeholder: gf2_rank will be implemented in Phase 1 ───────────────────
def _gf2_rank_placeholder(a: np.ndarray) -> int:
    """
    Placeholder for GF(2) rank. Returns numpy matrix rank over reals as a
    rough proxy. Replace with proper GF(2) row-reduction in Phase 1.

    .. warning::
        This is NOT correct over GF(2) for general matrices.
        Phase 1 will implement the real version in qec_toolkit/verification/gf2.py.
    """
    return int(np.linalg.matrix_rank(a))


@dataclass
class CSSCode:
    """
    Represents a CSS (Calderbank-Shor-Steane) quantum error-correcting code.

    Parameters
    ----------
    hx : np.ndarray
        X-check parity-check matrix, shape (r_x, n), dtype uint8.
        Row i of hx gives the support of the i-th X-type stabilizer.
    hz : np.ndarray
        Z-check parity-check matrix, shape (r_z, n), dtype uint8.
        Row j of hz gives the support of the j-th Z-type stabilizer.
    name : str, optional
        Human-readable name for the code (e.g. "[[7,1,3]] Steane").
    distance : int or None
        Known/estimated code distance d. Set after verification.

    Examples
    --------
    >>> # 3-qubit repetition code (only Z checks, trivial X check)
    >>> hz = np.array([[1,1,0],[0,1,1]], dtype=np.uint8)
    >>> hx = np.zeros((1, 3), dtype=np.uint8)  # no X errors detected
    >>> code = CSSCode(hx=hx, hz=hz, name="3-qubit repetition")
    >>> code.n
    3
    """

    hx: np.ndarray  # X-check matrix, shape (r_x, n)
    hz: np.ndarray  # Z-check matrix, shape (r_z, n)
    name: str = ""
    distance: int | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Coerce to uint8 on construction."""
        self.hx = np.asarray(self.hx, dtype=np.uint8)
        self.hz = np.asarray(self.hz, dtype=np.uint8)

    # ── Dimensions ─────────────────────────────────────────────────────────

    @property
    def n(self) -> int:
        """Number of physical qubits."""
        return int(self.hx.shape[1])

    @property
    def r_x(self) -> int:
        """Number of X-type stabilizer generators (rows of H_X)."""
        return int(self.hx.shape[0])

    @property
    def r_z(self) -> int:
        """Number of Z-type stabilizer generators (rows of H_Z)."""
        return int(self.hz.shape[0])

    @property
    def k(self) -> int:
        """
        Number of logical qubits.

        k = n - rank_GF2(H_X) - rank_GF2(H_Z)

        .. note::
            Uses placeholder rank until Phase 1 is implemented.
        """
        # TODO (Phase 1): replace with gf2_rank from qec_toolkit.verification.gf2
        return self.n - _gf2_rank_placeholder(self.hx) - _gf2_rank_placeholder(self.hz)

    # ── Validation ─────────────────────────────────────────────────────────

    def validate(self) -> None:
        """
        Verify the CSS commutation condition: H_X @ H_Z.T ≡ 0 (mod 2).

        Raises
        ------
        AssertionError
            If the commutation condition fails. This means the matrices do NOT
            define a valid CSS code.

        Interview note:
            This check ensures every X-stabilizer commutes with every Z-stabilizer.
            If it fails, the syndrome measurements would be contradictory.
        """
        commutator = (self.hx @ self.hz.T) % 2
        assert np.all(commutator == 0), (
            f"CSS commutation condition FAILED for code '{self.name}'.\n"
            f"H_X @ H_Z.T mod 2 has {commutator.sum()} nonzero entries.\n"
            "This means H_X and H_Z do not define a valid CSS code."
        )

    def is_valid(self) -> bool:
        """Return True if H_X @ H_Z.T = 0 mod 2, False otherwise."""
        return bool(np.all((self.hx @ self.hz.T) % 2 == 0))

    # ── Display ────────────────────────────────────────────────────────────

    def summary(self) -> str:
        """Return a one-line parameter summary: [[n, k, d]] and check weights."""
        d_str = str(self.distance) if self.distance is not None else "?"
        x_weight = self.hx.sum(axis=1).mean() if self.r_x > 0 else 0
        z_weight = self.hz.sum(axis=1).mean() if self.r_z > 0 else 0
        valid = "OK" if self.is_valid() else "INVALID!"
        return (
            f"{self.name or 'CSSCode'}: "
            f"[[{self.n}, {self.k}, {d_str}]] | "
            f"r_x={self.r_x}, r_z={self.r_z} | "
            f"avg_wX={x_weight:.1f}, avg_wZ={z_weight:.1f} | CSS={valid}"
        )

    def __repr__(self) -> str:
        return self.summary()

    # ── Logical operators (Phase 1 placeholder) ─────────────────────────────

    def logicals(self):
        """
        Return independent logical X and Z operators.

        .. note::
            NOT IMPLEMENTED YET. Will be implemented in Phase 1 after
            GF(2) nullspace and rowspace routines are tested.
        """
        raise NotImplementedError(
            "Logical operator extraction not yet implemented. "
            "See Phase 1: qec_toolkit/verification/logicals.py"
        )
