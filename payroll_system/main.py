"""Command line utilities for the payroll system.

Running this module provides a tiny command line interface.  Passing the
``--gui`` option launches the Tkinter front end; otherwise a short help
message is printed to standard output.
"""
import argparse
from .gui import run_gui
from .db import init_db


def main():
    """Entry point used by ``python -m payroll_system.main``.

    The function parses ``--gui`` and initializes the database.  If the
    flag is supplied the Tkinter window is started.  Without it the
    function simply prints a short informational message.
    """
    """Parse CLI arguments and launch the GUI if requested."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--gui', action='store_true', help='Run GUI')
    args = parser.parse_args()

    init_db()

    if args.gui:
        run_gui()
    else:
        print('Payroll System CLI. Use --gui for GUI.')

if __name__ == '__main__':
    main()
