"""Minimal Tkinter interface for the payroll system.
The GUI is deliberately lightweight so that newcomers can run it
without extensive setup. It demonstrates how to log in with a role and
add a very small amount of employee data.
"""

import tkinter as tk
from tkinter import messagebox
from .db import (
    get_session,
    add_employee,
    init_db,
    log_action,
)

def run_gui():
    """Launch a simple GUI for adding employees with login."""
    init_db()

    creds = {
        'master': {'password': 'master', 'role': 'Master'},
        'viewer': {'password': 'viewer', 'role': 'View-Only'},
        'att': {'password': 'att', 'role': 'Attendance-Only'},
    }

    login = tk.Tk()
    login.title('Login')

    tk.Label(login, text='Username').grid(row=0, column=0)
    user_var = tk.Entry(login)
    user_var.grid(row=0, column=1)
    tk.Label(login, text='Password').grid(row=1, column=0)
    pass_var = tk.Entry(login, show='*')
    pass_var.grid(row=1, column=1)

    def attempt_login():
        u = user_var.get()
        p = pass_var.get()
        if u in creds and creds[u]['password'] == p:
            role = creds[u]['role']
            login.destroy()
            open_main(role)
        else:
            messagebox.showerror('Login Failed', 'Invalid credentials')

    tk.Button(login, text='Login', command=attempt_login).grid(row=2, column=0, columnspan=2)
    login.mainloop()


def open_main(role: str):
    """Open the main window after successful login."""
    root = tk.Tk()
    root.title(f'Payroll System ({role})')
    tk.Label(root, text='Name').grid(row=0, column=0)
    name_var = tk.Entry(root)
    name_var.grid(row=0, column=1)

    tk.Label(root, text='Aadhar').grid(row=1, column=0)
    aadhar_var = tk.Entry(root)
    aadhar_var.grid(row=1, column=1)

    def submit():
        if role == 'View-Only':
            messagebox.showwarning('Read only', 'You do not have permission to add employees.')
            return
        """Callback for the Add button."""
        with get_session() as session:
            emp_id = add_employee(session, name=name_var.get(), aadhar_number=aadhar_var.get())
            log_action(session, role, f'Add Employee {emp_id}')
            messagebox.showinfo('Added', f'Employee {emp_id} added')

    tk.Button(root, text='Add', command=submit).grid(row=2, column=0, columnspan=2)

    root.mainloop()

if __name__ == '__main__':
    run_gui()
