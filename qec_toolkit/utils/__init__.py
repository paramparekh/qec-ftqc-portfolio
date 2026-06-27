"""qec_toolkit.utils — config loading, CSV I/O, seed management"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np


def load_config(path: str | Path) -> dict[str, Any]:
    """
    Load an experiment config from a YAML or JSON file.

    Parameters
    ----------
    path : str or Path
        Path to a .yaml or .json config file.

    Returns
    -------
    dict
        Parsed config dictionary.

    Status: SKELETON — implement in Phase 1.
    """
    raise NotImplementedError("load_config: implement in Phase 1")


def get_rng(seed: int) -> np.random.Generator:
    """
    Return a seeded numpy random generator.

    Parameters
    ----------
    seed : int
        Random seed for reproducibility (should come from config file).

    Returns
    -------
    np.random.Generator
        A seeded Generator instance.

    Notes
    -----
    Always use this instead of np.random.seed() for modern numpy RNG.
    Pass the generator to any function that needs randomness.
    """
    return np.random.default_rng(seed)
