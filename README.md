# Payroll System Example

This repository provides a tiny demonstration of a payroll and attendance system written in Python.  The goal is educational: each module is small and easy to read so that newcomers can see how a larger project might be structured.

## Getting Started

1. **Install Python dependencies**

   Install the packages listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

   If you encounter `ModuleNotFoundError: No module named 'sklearn'` during the tests or while running the code, ensure that `scikit-learn` is installed using the command above.

2. **Launch the GUI**

   The simplest way to try the demo is to start the Tkinter interface:

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

