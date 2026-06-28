"""
qec_toolkit.codes.repetition
============================
CSS constructor for the classical bit-flip repetition code.
"""

from __future__ import annotations

import numpy as np

from qec_toolkit.codes.base import CSSCode


def make_repetition_code(n: int = 3) -> CSSCode:
    """
    Return the length-``n`` bit-flip repetition code as a CSS code.

    Parameters
    ----------
    n : int
        Number of physical qubits. Must be at least 2.

    Returns
    -------
    CSSCode
        A CSS code with adjacent Z-checks ``Z_i Z_{i+1}``, no X-checks, and
        one protected classical bit-flip logical degree of freedom.
    """
    if n < 2:
        raise ValueError("repetition code length n must be at least 2")

    hz = np.zeros((n - 1, n), dtype=np.uint8)
    for row in range(n - 1):
        hz[row, row] = 1
        hz[row, row + 1] = 1

    hx = np.zeros((0, n), dtype=np.uint8)
    return CSSCode(hx=hx, hz=hz, name=f"{n}-qubit repetition", distance=n)
