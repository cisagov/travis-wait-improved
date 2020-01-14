#!/usr/bin/env pytest -vs
"""Tests for travis_wait_improved."""

# Standard Python Libraries
import os
import sys
from unittest.mock import patch

# Third-Party Libraries
import pytest

# cisagov Libraries
import travis_wait_improved
from travis_wait_improved import sherpa

# define sources of version strings
RELEASE_TAG = os.getenv("RELEASE_TAG")
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
    RELEASE_TAG in [None, ""], reason="this is not a release (RELEASE_TAG not set)"
)
def test_release_version():
    """Verify that release tag version agrees with the module version."""
    assert (
        RELEASE_TAG == f"v{PROJECT_VERSION}"
    ), "RELEASE_TAG does not match the project version"


def test_child_timeout_kill(capsys):
    """Determine if the sherpa killed the child, and it exited with non-zero."""
    with patch.object(sys, "argv", ["bogus", "--timeout=1s", "sleep", "10"]):
        return_code = sherpa.main()
        captured = capsys.readouterr()
        assert (
            "killing child" in captured.out
        ), "didn't see expected 'killing child' message in output"
        assert return_code != 0, "main() should not retun 0 when the child is killed"


def test_child_success(capsys):
    """Determine if the sherpa killed the child, and it exited with non-zero."""
    with patch.object(sys, "argv", ["bogus", "--timeout=5s", "sleep", "3"]):
        return_code = sherpa.main()
        captured = capsys.readouterr()
        assert (
            "exited with: 0" in captured.out
        ), "didn't see expected 'exited with: 0' message in output"
        assert return_code == 0, "main() should return 0 when the child returns 0"


@pytest.mark.slow
def test_child_slow_success(capsys):
    """Determine if the sherpa killed the child, and it exited with non-zero."""
    with patch.object(sys, "argv", ["bogus", "--timeout=2m", "sleep", "90"]):
        return_code = sherpa.main()
        captured = capsys.readouterr()
        assert (
            "exited with: 0" in captured.out
        ), "didn't see expected 'exited with: 0' message in output"
        assert return_code == 0, "main() should return 0 when the child returns 0"


def test_child_fast_success(capsys):
    """Determine if the sherpa killed the child, and it exited with non-zero."""
    with patch.object(sys, "argv", ["bogus", "--timeout=1", "exit", "0"]):
        return_code = sherpa.main()
        captured = capsys.readouterr()
        assert (
            "exited with: 0" in captured.out
        ), "didn't see expected 'exited with: 0' message in output"
        assert return_code == 0, "main() should return 0 when the child returns 0"


def test_child_fast_fail(capsys):
    """Determine if the sherpa killed the child, and it exited with non-zero."""
    with patch.object(sys, "argv", ["bogus", "--timeout=1", "exit", "1"]):
        return_code = sherpa.main()
        captured = capsys.readouterr()
        assert (
            "exited with: 1" in captured.out
        ), "didn't see expected 'exited with: 1' message in output"
        assert return_code == 1, "main() should return 1 when the child returns 1"


def test_bad_timeout(capsys):
    """Test passing in a bad timeout value."""
    with pytest.raises(SystemExit):
        with patch.object(sys, "argv", ["bogus", "--timeout=yourmom", "exit", "1"]):
            return_code = sherpa.main()
            assert return_code == 1, "main() should return 1 when timeout is invalid"


def test_child_with_flags(capsys):
    """Test a child command that has flags and arguments.

    This tests to make sure options_first=True is on for docopt.
    """
    with patch.object(
        sys,
        "argv",
        ["bogus", "--timeout=2", "echo", "--something", "more", "complicated"],
    ):
        return_code = sherpa.main()
        captured = capsys.readouterr()
        assert (
            "exited with: 0" in captured.out
        ), "didn't see expected 'exited with: 0' message in output"
        assert return_code == 0, "main() should return 0 when the child returns 0"
