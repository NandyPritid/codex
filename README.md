# Payroll System Example

This repository contains a very small prototype of a payroll and attendance system. The code is intentionally simple and intended for newcomers.

## Running the Demo

1. **Install requirements** (only `cryptography`, `SQLAlchemy`, `pandas`, and `scikit-learn` are needed).
2. **Initialize and open the GUI**:
   ```bash
   python -m payroll_system.main --gui
   ```
   This launches a minimal window where you can add an employee by name and Aadhaar number.

3. **Command line usage**:
   Running `python -m payroll_system.main` without `--gui` simply prints a short message.

## Project Structure

- `payroll_system/db.py` – database models and helper functions
- `payroll_system/gui.py` – small Tkinter interface demo
- `payroll_system/export.py` – example Excel export
- `payroll_system/festival.py` – placeholder festival calendar logic
- `payroll_system/ml_utils.py` – machine learning helpers
- `tests/` – unit tests showing basic usage

This is not a full payroll solution but a starting point for experimentation.
