"""
conftest.py — pytest configuration and shared fixtures.
"""

import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests that take more than 5 seconds (MILP, large sims)"
    )
    config.addinivalue_line(
        "markers", "phase1: marks tests that become active in Phase 1"
    )
    config.addinivalue_line(
        "markers", "phase2: marks tests that become active in Phase 2"
    )
    config.addinivalue_line(
        "markers", "phase3: marks tests that become active in Phase 3"
    )
