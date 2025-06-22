"""Database utilities for the payroll system.

This module defines SQLAlchemy models and helper functions to manage
employee records in a local SQLite database. Sensitive fields are
encrypted with Fernet for demonstration purposes.
"""

import os
import json
from zipfile import ZipFile
from datetime import datetime
from uuid import uuid4
from cryptography.fernet import Fernet
from sqlalchemy import (
    create_engine, Column, String, Integer, Float, Boolean,
    DateTime, JSON, ForeignKey, Index
)
from sqlalchemy.orm import declarative_base, sessionmaker

DB_NAME = os.environ.get('PAYROLL_DB', 'employee_db_2025.sqlite')
Base = declarative_base()
engine = create_engine(f'sqlite:///{DB_NAME}', echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

# Simple key management for demo purposes
# ``secret.key`` is created automatically on first run so that encrypted
# fields can be recovered on subsequent executions.
KEY_FILE = 'secret.key'
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, 'wb') as f:
        f.write(Fernet.generate_key())

def load_key():
    """Load the encryption key used for protecting sensitive fields."""
    return open(KEY_FILE, 'rb').read()

fernet = Fernet(load_key())

class Employee(Base):
    """Employee details stored in the database."""

    __tablename__ = 'employees'

    employee_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String)
    address = Column(String)
    contact_number = Column(String)
    family_contact_person = Column(String)
    family_contact_number = Column(String)
    blood_group = Column(String)
    medicines = Column(String)
    relationship = Column(String)
    reference = Column(String)
    aadhar_number = Column(String)
    pan_number = Column(String)
    address_proof = Column(String)
    photo = Column(String)
    hire_date = Column(DateTime)
    salary_history = Column(JSON, default={})
    consent_given = Column(Boolean, default=False)
    custom_fields = Column(JSON, default={})

class Attendance(Base):
    """Daily attendance records."""

    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    employee_id = Column(String, ForeignKey('employees.employee_id'), index=True)
    date = Column(DateTime, index=True)
    salary = Column(Float)
    role = Column(String)
    is_sunday = Column(Boolean)
    leave_type = Column(String)
    temporary_salary = Column(Float)
    anomaly_flag = Column(String)

class DeletedEmployee(Base):
    """Tracks deleted employees for audit purposes."""

    __tablename__ = 'deleted_employees'

    id = Column(Integer, primary_key=True)
    employee_id = Column(String)
    name = Column(String)
    deletion_date = Column(DateTime, default=datetime.utcnow)
    deletion_reason = Column(String)
    deletion_details = Column(String)
    deleted_by = Column(String)

class AuditLog(Base):
    """Record of all actions performed in the GUI or CLI."""

    __tablename__ = 'audit_log'

    action_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String)

class Metadata(Base):
    """Schema versioning information."""

    __tablename__ = 'metadata'

    version_id = Column(String, primary_key=True)
    last_updated = Column(DateTime)

# --- Helper functions ----------------------------------------------------

def encrypt(value: str) -> str:
    """Encrypt a string value for secure storage.

    Parameters
    ----------
    value : str
        Plain text to encrypt.

    Returns
    -------
    str
        Encrypted representation or ``None`` if ``value`` is ``None``.
    """
    if value is None:
        return None
    return fernet.encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    """Decrypt a previously encrypted string."""
    if value is None:
        return None
    return fernet.decrypt(value.encode()).decode()


def init_db():
    """Create database tables and insert initial metadata if missing."""
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        if not session.query(Metadata).first():
            session.add(
                Metadata(version_id='1.0', last_updated=datetime.utcnow())
            )
            session.commit()


def add_employee(session, **kwargs):
    """Insert a new employee record and return its UUID.

    Parameters
    ----------
    session : Session
        SQLAlchemy session in which the employee will be created.
    **kwargs : dict
        Fields matching :class:`Employee` columns.

    Returns
    -------
    str
        The generated ``employee_id``.
    """
    # Basic validation for government IDs
    aadhar = kwargs.get("aadhar_number")
    if aadhar:
        if not (aadhar.isdigit() and len(aadhar) == 12):
            raise ValueError("Aadhar number must be a 12-digit number")

    pan = kwargs.get("pan_number")
    if pan:
        if len(pan) != 10:
            raise ValueError("PAN number must be a 10-character code")

    sensitive_fields = ["aadhar_number", "pan_number"]
    for field in sensitive_fields:
        if field in kwargs and kwargs[field]:
            kwargs[field] = encrypt(kwargs[field])
    employee = Employee(**kwargs)
    session.add(employee)
    session.commit()
    return employee.employee_id


def get_session():
    """Create and return a new SQLAlchemy session."""
    return SessionLocal()


def get_employee(session, employee_id):
    """Fetch a single employee, decrypting sensitive fields."""
    emp = session.query(Employee).filter_by(employee_id=employee_id).first()
    if emp and emp.aadhar_number:
        emp.aadhar_number = decrypt(emp.aadhar_number)
    if emp and emp.pan_number:
        emp.pan_number = decrypt(emp.pan_number)
    return emp


def log_action(session, user_id: str, action: str, details: str = ''):
    """Record a user action in the audit log."""
    session.add(AuditLog(user_id=user_id, action=action, details=details))
    session.commit()

def restore_database(zip_path: str, work_dir: str = '.') -> str:
    """Restore the application database from a ZIP archive.

    WARNING: use this only with trusted ZIP files. Malicious archives can
    overwrite arbitrary files.

    Parameters
    ----------
    zip_path : str
        Path to the ZIP archive containing the database backup.
    work_dir : str, optional
        Directory into which the contents will be extracted. Defaults to the
        current working directory.

    Returns
    -------
    str
        The path to the restored database file.
    """
    extract_base = os.path.realpath(work_dir)
    with ZipFile(zip_path, 'r') as zf:
        for member in zf.namelist():
            dest = os.path.realpath(os.path.join(extract_base, member))
            if not dest.startswith(extract_base + os.sep):
                raise ValueError(f"Unsafe path detected in archive: {member}")
        zf.extractall(extract_base)
    return os.path.join(extract_base, DB_NAME)

#def record_attendance(
#    session,
#    employee_id: str,
#    date: datetime,
#    salary: float,
#    role: str,
#    is_sunday: bool = False,
#    leave_type: str | None = None,
#    temporary_salary: float | None = None,
#    anomaly_flag: str | None = None,
#):
#    """Insert a new attendance entry."""
#    record = Attendance(
#        employee_id=employee_id,
#        date=date,
#        salary=salary,
#        role=role,
#        is_sunday=is_sunday,
#        leave_type=leave_type,
#        temporary_salary=temporary_salary,
#        anomaly_flag=anomaly_flag,
#    )
#    session.add(record)
#    session.commit()

def backup_database(zip_path: str = 'backup.zip'):
    """Create a ZIP archive containing the database and employee files."""
    import zipfile

    with zipfile.ZipFile(zip_path, 'w') as zf:
        if os.path.exists(DB_NAME):
            zf.write(DB_NAME)
        if os.path.exists('employee_files'):
            for root_dir, _, files in os.walk('employee_files'):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    zf.write(file_path)
    return zip_path
