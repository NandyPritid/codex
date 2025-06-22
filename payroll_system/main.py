"""Command line utilities for the payroll system.
The command line is intentionally simple so that users can quickly
perform common actions like launching the GUI or exporting data without
remembering many options.
"""

import argparse
from .gui import run_gui
from .db import init_db, backup_database
from .export import export_attendance


def main():
    """Parse CLI arguments and launch the GUI if requested."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--gui', action='store_true', help='Run GUI')
    parser.add_argument('--backup', help='Create a backup ZIP of the database')
    parser.add_argument('--export', nargs=2, metavar=('START', 'END'), help='Export attendance between two YYYY-MM-DD dates')
    args = parser.parse_args()

    init_db()

    if args.gui:
        run_gui()
    elif args.backup:
        path = backup_database(args.backup)
        print(f'Backup written to {path}')
    elif args.export:
        start, end = args.export
        file = export_attendance(start, end)
        print(f'Attendance exported to {file}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
