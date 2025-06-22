"""Utility functions for exporting payroll data.

Only a single helper ``export_attendance`` is provided for demonstration.
It writes queried attendance records to an Excel file using ``pandas``.
"""

import pandas as pd
from datetime import datetime
from .db import SessionLocal, Attendance, Employee


def export_attendance(start_date, end_date, filename='attendance.xlsx'):
    """Export attendance records to an Excel file.

    Parameters
    ----------
    start_date, end_date : datetime
        Boundaries for the exported records.
    filename : str, optional
        Path of the resulting Excel file.

    Returns
    -------
    str
        The filename that was written.
    """
    with SessionLocal() as session:
        records = session.query(Attendance).filter(
            Attendance.date >= start_date,
            Attendance.date <= end_date
        ).all()
        data = [
            {
                'employee_id': r.employee_id,
                'date': r.date,
                'salary': r.salary,
                'role': r.role,
                'is_sunday': r.is_sunday,
                'leave_type': r.leave_type,
                'temporary_salary': r.temporary_salary,
            }
            for r in records
        ]
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename
