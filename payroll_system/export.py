"""Utility functions for exporting payroll data.

These helpers demonstrate how the database contents can be exported to
Excel, CSV, or JSON files so that non-technical users can back up or
analyze the information in common tools like LibreOffice or Excel.
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from .db import SessionLocal, Attendance, Employee


def export_attendance(start_date, end_date, filename='attendance.xlsx') -> str:
    """Export attendance records to an Excel file.

    Parameters
    ----------
    start_date, end_date : datetime
        Boundaries for the export.
    filename : str, optional
        Destination path. The suffix determines the output format.

    Returns
    -------
    str
        Path to the written file.
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
    path = Path(filename)
    if path.suffix == '.csv':
        df.to_csv(path, index=False)
    elif path.suffix == '.json':
        df.to_json(path, orient='records')
    else:
        df.to_excel(path, index=False)
    return str(path)
