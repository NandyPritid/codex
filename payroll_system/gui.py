"""Minimal Tkinter interface for the payroll system.

This GUI is intentionally tiny but demonstrates how multiple screens can
be used to manage employees, record attendance and view festival dates.
It is suitable for experiments and learning purposes.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from .db import (
    get_session,
    add_employee,
    init_db,
    log_action,
    record_attendance,
)
from .festival import get_festivals


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


def open_main(role: str) -> None:
    """Open the main window with tabs for employees, attendance and festivals."""
    root = tk.Tk()
    root.title(f"Payroll System ({role})")

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    # --- Employee tab -------------------------------------------------
    emp_tab = ttk.Frame(nb)
    nb.add(emp_tab, text="Employee")

    ttk.Label(emp_tab, text="Name").grid(row=0, column=0)
    name_var = ttk.Entry(emp_tab)
    name_var.grid(row=0, column=1)

    ttk.Label(emp_tab, text="Aadhar").grid(row=1, column=0)
    aadhar_var = ttk.Entry(emp_tab)
    aadhar_var.grid(row=1, column=1)

    ttk.Label(emp_tab, text="PAN").grid(row=2, column=0)
    pan_var = ttk.Entry(emp_tab)
    pan_var.grid(row=2, column=1)

    ttk.Label(emp_tab, text="Contact").grid(row=3, column=0)
    contact_var = ttk.Entry(emp_tab)
    contact_var.grid(row=3, column=1)

    ttk.Label(emp_tab, text="Hire Date (YYYY-MM-DD)").grid(row=4, column=0)
    hire_var = ttk.Entry(emp_tab)
    hire_var.grid(row=4, column=1)

    def submit_emp():
        if role == "View-Only":
            messagebox.showwarning("Read only", "You do not have permission to add employees.")
            return
        try:
            hire_date = datetime.fromisoformat(hire_var.get()) if hire_var.get() else None
        except ValueError:
            messagebox.showerror("Invalid", "Hire date must be YYYY-MM-DD")
            return
        with get_session() as session:
            emp_id = add_employee(
                session,
                name=name_var.get(),
                aadhar_number=aadhar_var.get(),
                pan_number=pan_var.get(),
                contact_number=contact_var.get(),
                hire_date=hire_date,
            )
            log_action(session, role, f"Add Employee {emp_id}")
            messagebox.showinfo("Added", f"Employee {emp_id} added")

    ttk.Button(emp_tab, text="Add", command=submit_emp).grid(row=5, column=0, columnspan=2)

    # --- Attendance tab ----------------------------------------------
    att_tab = ttk.Frame(nb)
    nb.add(att_tab, text="Attendance")

    ttk.Label(att_tab, text="Employee ID").grid(row=0, column=0)
    emp_id_var = ttk.Entry(att_tab)
    emp_id_var.grid(row=0, column=1)

    ttk.Label(att_tab, text="Date (YYYY-MM-DD)").grid(row=1, column=0)
    att_date_var = ttk.Entry(att_tab)
    att_date_var.grid(row=1, column=1)

    ttk.Label(att_tab, text="Salary").grid(row=2, column=0)
    salary_var = ttk.Entry(att_tab)
    salary_var.grid(row=2, column=1)

    ttk.Label(att_tab, text="Role").grid(row=3, column=0)
    role_var = ttk.Entry(att_tab)
    role_var.grid(row=3, column=1)

    sunday_var = tk.BooleanVar()
    ttk.Checkbutton(att_tab, text="Sunday", variable=sunday_var).grid(row=4, column=0, columnspan=2)

    ttk.Label(att_tab, text="Leave Type").grid(row=5, column=0)
    leave_var = ttk.Entry(att_tab)
    leave_var.grid(row=5, column=1)

    ttk.Label(att_tab, text="Temporary Salary").grid(row=6, column=0)
    tmp_sal_var = ttk.Entry(att_tab)
    tmp_sal_var.grid(row=6, column=1)

    def submit_att():
        if role not in {"Master", "Attendance-Only"}:
            messagebox.showwarning("No permission", "You cannot record attendance.")
            return
        try:
            date = datetime.fromisoformat(att_date_var.get())
        except ValueError:
            messagebox.showerror("Invalid", "Date must be YYYY-MM-DD")
            return
        with get_session() as session:
            record_attendance(
                session,
                employee_id=emp_id_var.get(),
                date=date,
                salary=float(salary_var.get() or 0),
                role=role_var.get(),
                is_sunday=sunday_var.get(),
                leave_type=leave_var.get() or None,
                temporary_salary=float(tmp_sal_var.get() or 0) or None,
            )
            log_action(session, role, f"Add attendance {emp_id_var.get()}")
            messagebox.showinfo("Recorded", "Attendance saved")

    ttk.Button(att_tab, text="Record", command=submit_att).grid(row=7, column=0, columnspan=2)

    # --- Festivals tab -----------------------------------------------
    fest_tab = ttk.Frame(nb)
    nb.add(fest_tab, text="Festivals")

    fest_list = tk.Listbox(fest_tab, width=40)
    fest_list.grid(row=0, column=0, columnspan=2)

    def refresh_festivals():
        fest_list.delete(0, tk.END)
        for name, date in get_festivals().items():
            fest_list.insert(tk.END, f"{name} - {date.strftime('%Y-%m-%d')}")

    ttk.Button(fest_tab, text="Load Festivals", command=refresh_festivals).grid(row=1, column=0, columnspan=2)
    refresh_festivals()

    root.mainloop()

if __name__ == '__main__':
    run_gui()
