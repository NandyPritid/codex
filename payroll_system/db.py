import os
import json
from datetime import datetime
from uuid import uuid4
from cryptography.fernet import Fernet
from sqlalchemy import (create_engine, Column, String, Integer, Float, Boolean,
                        DateTime, JSON, ForeignKey)
from sqlalchemy.orm import declarative_base, sessionmaker

DB_NAME = os.environ.get('PAYROLL_DB', 'employee_db_2025.sqlite')
Base = declarative_base()
engine = create_engine(f'sqlite:///{DB_NAME}', echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

# Simple key management for demo purposes
KEY_FILE = 'secret.key'
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, 'wb') as f:
        f.write(Fernet.generate_key())

def load_key():
    return open(KEY_FILE, 'rb').read()

fernet = Fernet(load_key())

class Employee(Base):
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
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    employee_id = Column(String, ForeignKey('employees.employee_id'))
    date = Column(DateTime)
    salary = Column(Float)
    role = Column(String)
    is_sunday = Column(Boolean)
    leave_type = Column(String)
    temporary_salary = Column(Float)
    anomaly_flag = Column(String)

class DeletedEmployee(Base):
    __tablename__ = 'deleted_employees'
    id = Column(Integer, primary_key=True)
    employee_id = Column(String)
    name = Column(String)
    deletion_date = Column(DateTime, default=datetime.utcnow)
    deletion_reason = Column(String)
    deletion_details = Column(String)
    deleted_by = Column(String)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    action_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String)

class Metadata(Base):
    __tablename__ = 'metadata'
    version_id = Column(String, primary_key=True)
    last_updated = Column(DateTime)


def encrypt(value: str) -> str:
    if value is None:
        return None
    return fernet.encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    if value is None:
        return None
    return fernet.decrypt(value.encode()).decode()


def init_db():
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        if not session.query(Metadata).first():
            session.add(Metadata(version_id='1.0', last_updated=datetime.utcnow()))
            session.commit()


def add_employee(session, **kwargs):
    sensitive_fields = ['aadhar_number', 'pan_number']
    for field in sensitive_fields:
        if field in kwargs and kwargs[field]:
            kwargs[field] = encrypt(kwargs[field])
    employee = Employee(**kwargs)
    session.add(employee)
    session.commit()
    return employee.employee_id



def get_session():
    return SessionLocal()


def get_employee(session, employee_id):
    emp = session.query(Employee).filter_by(employee_id=employee_id).first()
    if emp and emp.aadhar_number:
        emp.aadhar_number = decrypt(emp.aadhar_number)
    if emp and emp.pan_number:
        emp.pan_number = decrypt(emp.pan_number)
    return emp


def log_action(session, user_id: str, action: str, details: str = ''):
    session.add(AuditLog(user_id=user_id, action=action, details=details))
    session.commit()

