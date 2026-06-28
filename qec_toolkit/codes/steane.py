"""
qec_toolkit.codes.steane
========================
Constructor for the [[7, 1, 3]] Steane CSS code.
"""

from __future__ import annotations

import numpy as np

from qec_toolkit.codes.base import CSSCode


def make_steane_code() -> CSSCode:
    """
    Return the [[7, 1, 3]] Steane code.

    The Steane code is built from the self-orthogonal classical [7, 4, 3]
    Hamming code. Its CSS check matrices are identical: ``H_X = H_Z = H``.

    Returns
    -------
    CSSCode
        The Steane CSS code with three X-checks, three Z-checks, one logical
        qubit, and distance 3.
    """
    hamming_check = np.array(
        [
            [1, 1, 1, 1, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 0],
            [1, 0, 1, 0, 1, 0, 1],
        ],
        dtype=np.uint8,
    )
    return CSSCode(
        hx=hamming_check.copy(),
        hz=hamming_check.copy(),
        name="[[7,1,3]] Steane",
        distance=3,
    )
