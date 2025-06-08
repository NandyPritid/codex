import pandas as pd
from datetime import datetime
from .db import SessionLocal, Attendance, Employee


def export_attendance(start_date, end_date, filename='attendance.xlsx'):
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
