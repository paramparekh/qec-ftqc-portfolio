"""
qec_toolkit.codes.base
======================
Core data structures for CSS quantum error-correcting codes.

A CSS code is defined by two binary parity-check matrices:

- ``hx``: X-type stabilizer checks, shape ``(r_x, n)``.
- ``hz``: Z-type stabilizer checks, shape ``(r_z, n)``.

The CSS commutation condition is ``hx @ hz.T == 0 mod 2``. The number of
logical qubits is ``k = n - rank_GF2(hx) - rank_GF2(hz)``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from qec_toolkit.verification.gf2 import gf2_rank


@dataclass
class CSSCode:
    """
    Represents a CSS (Calderbank-Shor-Steane) quantum error-correcting code.

    Parameters
    ----------
    hx : np.ndarray
        X-check parity-check matrix, shape ``(r_x, n)``.
    hz : np.ndarray
        Z-check parity-check matrix, shape ``(r_z, n)``.
    name : str
        Human-readable code name.
    distance : int | None
        Known or verified code distance, when available.
    """

    hx: np.ndarray
    hz: np.ndarray
    name: str = ""
    distance: int | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Coerce check matrices to binary ``np.uint8`` arrays."""
        self.hx = (np.asarray(self.hx, dtype=np.uint8) % 2).astype(np.uint8)
        self.hz = (np.asarray(self.hz, dtype=np.uint8) % 2).astype(np.uint8)
        if self.hx.ndim != 2 or self.hz.ndim != 2:
            raise ValueError("hx and hz must both be 2D matrices")
        if self.hx.shape[1] != self.hz.shape[1]:
            raise ValueError(
                f"hx and hz must have the same number of columns, got "
                f"{self.hx.shape[1]} and {self.hz.shape[1]}"
            )

    @property
    def n(self) -> int:
        """Number of physical qubits."""
        return int(self.hx.shape[1])

    @property
    def r_x(self) -> int:
        """Number of X-type stabilizer generators."""
        return int(self.hx.shape[0])

    @property
    def r_z(self) -> int:
        """Number of Z-type stabilizer generators."""
        return int(self.hz.shape[0])

    @property
    def k(self) -> int:
        """Number of logical qubits computed with GF(2) ranks."""
        return self.n - gf2_rank(self.hx) - gf2_rank(self.hz)

    def validate(self) -> None:
        """
        Verify the CSS commutation condition ``hx @ hz.T == 0 mod 2``.

        Raises
        ------
        AssertionError
            If any X-check anticommutes with any Z-check.
        """
        commutator = (self.hx @ self.hz.T) % 2
        assert np.all(commutator == 0), (
            f"CSS commutation condition failed for code '{self.name}'. "
            f"hx @ hz.T mod 2 has {int(commutator.sum())} nonzero entries."
        )

    def is_valid(self) -> bool:
        """Return ``True`` iff all X and Z checks commute."""
        return bool(np.all((self.hx @ self.hz.T) % 2 == 0))

    def summary(self) -> str:
        """Return a one-line summary of code parameters and check weights."""
        d_str = str(self.distance) if self.distance is not None else "?"
        x_weight = float(self.hx.sum(axis=1).mean()) if self.r_x > 0 else 0.0
        z_weight = float(self.hz.sum(axis=1).mean()) if self.r_z > 0 else 0.0
        valid = "OK" if self.is_valid() else "INVALID"
        return (
            f"{self.name or 'CSSCode'}: "
            f"[[{self.n}, {self.k}, {d_str}]] | "
            f"r_x={self.r_x}, r_z={self.r_z} | "
            f"avg_wX={x_weight:.1f}, avg_wZ={z_weight:.1f} | CSS={valid}"
        )

    def __repr__(self) -> str:
        return self.summary()

    def logicals(self):
        """
        Return independent logical X and Z operators.

        Logical extraction is intentionally deferred until after Phase 1's
        GF(2) rowspace/nullspace routines are established.
        """
        raise NotImplementedError(
            "Logical operator extraction not yet implemented. "
            "See qec_toolkit/verification/logicals.py in a later phase."
        )
