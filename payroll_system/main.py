import argparse
from .gui import run_gui
from .db import init_db


def main():
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
