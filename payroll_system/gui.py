import tkinter as tk
from tkinter import messagebox
from .db import get_session, add_employee, init_db, log_action


def run_gui():
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
        with get_session() as session:
            emp_id = add_employee(session, name=name_var.get(), aadhar_number=aadhar_var.get())
            log_action(session, 'admin', f'Add Employee {emp_id}')
            messagebox.showinfo('Added', f'Employee {emp_id} added')

    tk.Button(root, text='Add', command=submit).grid(row=2, column=0, columnspan=2)

    root.mainloop()

if __name__ == '__main__':
    run_gui()
