#!/usr/bin/env python

"""Helper tool to work around stdout timout of Travis-CI.

If a long-running process does not output anything for 10 minutes
Travis will assume it has stalled, and kill it.  Some tools (like Packer)
can easily go beyond this 10 minute mark without writing to stdout.

Usage:
  travis_wait_improved [--timeout=<time>] <command>...
  travis_wait_improved (-h | --help)

Options:
  -h --help             Show this message.
  -t --timeout=<mins>   Maximum time process will be allowed to run
                        in minutes (m) or seconds (s) [default: 20m].
"""

from datetime import datetime, timedelta
from enum import Enum, auto
import subprocess  # nosec
import sys

import docopt
from termcolor import colored

from ._version import __version__

HEADER = colored("Travis-wait ❱", "magenta", attrs=["bold"])
OUTPUT_INTERVAL = 60
COUNTDOWN_AT = 10


class Severity(Enum):
    """Used to select the formatting of messages."""

    GOOD = auto()
    WARNING = auto()
    FAIL = auto()


def cprint(message, severity=None):
    """Print a formatted message and flush."""
    if severity == Severity.GOOD:
        message = colored(f"{message}", "green", attrs=["bold"])
    elif severity == Severity.WARNING:
        message = colored(f"{message}", "yellow")
    elif severity == Severity.FAIL:
        message = colored(f"{message}", "red", attrs=["bold"])
    print(HEADER, message, flush=True)


def parse_time(time_str):
    """Parse the time string and return a timedelta."""
    try:
        if time_str[-1] in ["s", "S"]:
            # explict seconds
            return timedelta(seconds=int(time_str[:-1]))
        elif time_str[-1] in ["m", "M"]:
            # explicit minutes
            return timedelta(minutes=int(time_str[:-1]))
        else:
            # assuming minutes
            return timedelta(minutes=int(time_str))
    except ValueError:
        cprint("--timeout must be an integer, with optional unit 'm', or 's'")
        sys.exit(-1)


def now_no_us():
    """Return utcnow without microseconds."""
    now = datetime.utcnow()
    return now - timedelta(microseconds=now.microsecond)


def calculate_sleep_time(remaining_delta):
    """Calculate how long we should sleep."""
    seconds_to_kill = remaining_delta.total_seconds()
    if seconds_to_kill > COUNTDOWN_AT and seconds_to_kill <= OUTPUT_INTERVAL:
        # If we are getting close to the countdown, only sleep until that time
        max_sleep_time = seconds_to_kill - COUNTDOWN_AT
    elif seconds_to_kill <= COUNTDOWN_AT:
        # We are counting down
        max_sleep_time = 1
    else:
        # Not near countdown, do regular interval
        max_sleep_time = OUTPUT_INTERVAL
    return min(max_sleep_time, seconds_to_kill)


def main():
    """Start a child process, output status, and monitor exit."""
    args = docopt.docopt(__doc__, version=__version__)
    command = " ".join(args["<command>"])
    timeout = parse_time(args["--timeout"])

    # Calculate the time at which we will kill the child process.
    now = now_no_us()
    killtime = now + timeout

    # Log some startup information for the user.
    cprint(f"Running: {command}")
    cprint(f"Max runtime {timeout}")
    cprint(f"Will kill at {killtime} UTC")

    # Start the child process.
    child = subprocess.Popen(command, shell=True)  # nosec

    # Loop until it is time to kill the child process.
    while now < killtime:
        # Log how much time is remaining.
        remaining_delta = killtime - now
        cprint(f"{remaining_delta} remaining", severity=Severity.WARNING)
        try:
            sleep_time = calculate_sleep_time(remaining_delta)
            # Sleep while waiting for the child to exit.
            return_code = child.wait(sleep_time)
            # The child has exited before the timeout
            break
        except subprocess.TimeoutExpired:
            # The child did not exit.  Not a problem.
            pass
        now = now_no_us()
    else:
        # We've reached the killtime.
        cprint("Timeout reached... killing child.", severity=Severity.FAIL)
        child.kill()

    # Wait for the child to exit if it hasn't already.
    return_code = child.wait()
    # Log the return code of the child.
    if return_code == 0:
        cprint(f"Child has exited with: {return_code}", severity=Severity.GOOD)
    else:
        cprint(f"Child has exited with: {return_code}", severity=Severity.FAIL)

    # Return the child's return code as our own so that it can be acted upon.
    return return_code


if __name__ == "__main__":
    sys.exit(main())
