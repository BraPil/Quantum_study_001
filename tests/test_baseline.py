"""Baseline sanity check — verifies the test suite is reachable and Python version is correct."""
import sys


def test_python_version():
    assert sys.version_info >= (3, 12), f"Expected Python 3.12+, got {sys.version}"
