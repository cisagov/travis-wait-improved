#!/usr/bin/env python

"""example is an example Python library and tool.

Usage:
  example [--log-level=LEVEL]
  example (-h | --help)

Options:
  -h --help              Show this message.
  --log-level=LEVEL      If specified, then the log level will be set to
                         the specified value.  Valid values are "debug", "info",
                         "warning", "error", and "critical". [default: warning]
"""

import logging
import sys

import docopt

from ._version import __version__


def main():
    """Set up logging and call the example function."""
    args = docopt.docopt(__doc__, version=__version__)
    # Set up logging
    log_level = args["--log-level"]
    try:
        logging.basicConfig(
            format="%(asctime)-15s %(levelname)s %(message)s", level=log_level.upper()
        )
    except ValueError:
        logging.critical(
            f'"{log_level}" is not a valid logging level.  Possible values '
            "are debug, info, warning, and error."
        )
        return 1

    # Stop logging and clean up
    logging.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
