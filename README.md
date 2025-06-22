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
   On first launch the application creates `employee_db_2025.sqlite` in the project directory. The window allows you to enter an employee name and Aadhaar number.  Clicking **Add** stores the employee and logs the action.

3. **Command line usage**

   You can also run the module without arguments:

   ```bash
   python -m payroll_system.main
   ```

   This prints a short help message and exits.

4. **Run the unit tests**

   Execute the tests with:

   ```bash
   pytest -q
   ```

   The tests require `scikit-learn`. If the package is missing, install it using the command in step 1.

## Running the Notebook

The repository includes `Payroll_Attendance_System.ipynb` demonstrating
basic operations. Launch it with Jupyter:

```bash
jupyter notebook Payroll_Attendance_System.ipynb
```

Make sure the dependencies from step&nbsp;1 are installed before opening the
notebook. The included CSV files in `test_data/` are loaded relative to the
repository root, so run the command above from this directory.

## Project Structure

- `payroll_system/db.py` – SQLAlchemy models and helper utilities
- `payroll_system/gui.py` – minimal Tkinter interface for adding employees
- `payroll_system/export.py` – very small example of exporting attendance data
- `payroll_system/festival.py` – placeholder Bengali festival calculation logic
- `payroll_system/ml_utils.py` – lightweight machine learning helpers
- `Payroll_Attendance_System.ipynb` – Jupyter notebook showing basic usage
- `tests/` – simple unit tests for the ML logic
- `test_data/` – tiny CSV samples used by the notebook

This is **not** a production-ready payroll system. It is a starting point that can be extended.

## Troubleshooting

- **Missing Tkinter** – If the GUI does not open and you see an error about `tkinter` or `Tk`, install the Tk libraries for your Python distribution (on Ubuntu: `sudo apt-get install python3-tk`).
- **Database reset** – To start over, delete `employee_db_2025.sqlite` and run the program again to recreate it.
- **Import errors** – Ensure you activated the correct Python environment and installed dependencies from `requirements.txt`.
- **Missing packages** – If a module such as `pandas` or `scikit-learn` cannot be
  found, rerun `pip install -r requirements.txt` to install all required
  libraries.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
The code is intentionally concise but provides a starting point for a
more complete system with role based access, encrypted data, and export
capabilities.  Feel free to experiment!  See the notebook for examples.
