#!/usr/bin/env pytest -vs
"""Tests for travis_wait_improved."""

import os
import sys
from unittest.mock import patch

import pytest

import travis_wait_improved
from travis_wait_improved import sherpa

# define sources of version strings
TRAVIS_TAG = os.getenv("TRAVIS_TAG")
PROJECT_VERSION = travis_wait_improved.__version__


def test_stdout_version(capsys):
    """Verify that version string sent to stdout agrees with the module version."""
    with pytest.raises(SystemExit):
        with patch.object(sys, "argv", ["bogus", "--version"]):
            sherpa.main()
    captured = capsys.readouterr()
    assert (
        captured.out == f"{PROJECT_VERSION}\n"
    ), "standard output by '--version' should agree with module.__version__"


@pytest.mark.skipif(
    TRAVIS_TAG in [None, ""], reason="this is not a release (TRAVIS_TAG not set)"
)
def test_release_version():
    """Verify that release tag version agrees with the module version."""
    assert (
        TRAVIS_TAG == f"v{PROJECT_VERSION}"
    ), "TRAVIS_TAG does not match the project version"
