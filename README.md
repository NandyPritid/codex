# Lightweight Payroll and Attendance System

This repository demonstrates a **minimal** yet modular payroll system
implemented in pure Python.  It is designed for factories with fewer
than 50 employees and is intentionally simple so that even newcomers can
experiment with the code.

## Quick Start

1. **Install requirements**.  The only external packages are
   [SQLAlchemy](https://www.sqlalchemy.org/),
   [pandas](https://pandas.pydata.org/),
   [cryptography](https://cryptography.io/), and
   [scikit‑learn](https://scikit-learn.org/).  Install them with:
   ```bash
   pip install sqlalchemy pandas cryptography scikit-learn
   ```
2. **Launch the GUI** to add employees or attendance records:
   ```bash
   python -m payroll_system.main --gui
   ```
   Default credentials are:
   * `master` / `master`
   * `viewer` / `viewer`
   * `att` / `att`
3. **Command line tools**.  Run `python -m payroll_system.main --help` to
   see options such as creating a ZIP backup or exporting attendance to
   Excel/CSV/JSON files.

## Project Layout

- `payroll_system/db.py` – database models and helper utilities.
- `payroll_system/gui.py` – tiny Tkinter interface with role based login.
- `payroll_system/export.py` – export helpers for Excel/CSV/JSON.
- `payroll_system/festival.py` – Bengali festival calendar helpers.
- `payroll_system/ml_utils.py` – lightweight machine learning helpers.
- `tests/` – small unit tests to show expected behaviour.
- `Payroll_Attendance_System.ipynb` – Jupyter notebook walkthrough.

## Troubleshooting

- **Missing packages** – install the requirements shown above.  If you
  see an error like `ModuleNotFoundError: No module named 'sklearn'`,
  make sure scikit-learn was installed successfully.
- **Database locked** – close other programs using `employee_db_2025.sqlite`
  before launching the GUI or running exports.
- **Corrupt database** – you can restore from a ZIP backup created with
  `python -m payroll_system.main --backup backup.zip`.

The code is intentionally concise but provides a starting point for a
more complete system with role based access, encrypted data, and export
capabilities.

### Using the GUI

After logging in you will see three tabs:

1. **Employee** – enter name, Aadhar, PAN, contact number and hire date.
2. **Attendance** – record daily salary and role with optional leave type.
3. **Festivals** – view important Bengali holidays loaded from
   `test_data/festivals.csv`.

These examples are deliberately minimal so that even beginners can
follow the flow. Feel free to inspect the Jupyter notebook for a step by
step explanation.
