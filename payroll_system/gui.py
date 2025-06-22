"""Minimal Tkinter interface for the payroll system.

This module exposes :func:`run_gui`, a very small window that allows a
user to enter an employee's name and Aadhaar number.  Pressing the *Add*
button inserts the employee into the local SQLite database and records
the action in the audit log.
"""
import tkinter as tk
from tkinter import messagebox
from .db import get_session, add_employee, init_db, log_action


def attempt_login(username: str, password: str) -> bool:
    """Validate user credentials.

    This placeholder implementation simply returns ``True`` for any input.
    In a real application it would verify the provided username and
    password against a user database.

    Parameters
    ----------
    username:
        Name of the user attempting to authenticate.
    password:
        Password provided by the user.

    Returns
    -------
    bool
        ``True`` if the credentials are accepted, ``False`` otherwise.
    """

    return True

def run_gui():
    """Launch a simple GUI for adding employees.

    The window contains two entry fields (name and Aadhaar). When the
    user clicks **Add** the employee is saved and a confirmation dialog
    appears.
    """
    init_db()
    root = tk.Tk()
    root.title('Payroll System')

    tk.Label(root, text='Name').grid(row=0, column=0)
    name_var = tk.Entry(root)
    name_var.grid(row=0, column=1)

    tk.Label(root, text='Aadhar').grid(row=1, column=0)
    aadhar_var = tk.Entry(root)
    aadhar_var.grid(row=1, column=1)

    def submit():
        """Save a new employee record and display confirmation.

        This callback is invoked when the **Add** button is pressed. It
        writes the entered name and Aadhar number to the database and
        logs the action, then pops up a small confirmation window.
        """
        with get_session() as session:
            emp_id = add_employee(session, name=name_var.get(), aadhar_number=aadhar_var.get())
            log_action(session, 'admin', f'Add Employee {emp_id}')
            messagebox.showinfo('Added', f'Employee {emp_id} added')

    tk.Button(root, text='Add', command=submit).grid(row=2, column=0, columnspan=2)

    root.mainloop()

if __name__ == '__main__':
    run_gui()
