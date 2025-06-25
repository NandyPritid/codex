import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from payroll_system.ml_utils import predict_bonus_eligibility, recommend_leave_month

def test_bonus_eligibility():
    assert predict_bonus_eligibility(300, 0, 2) is True
    assert predict_bonus_eligibility(250, 0, 2) is False


def test_recommend_leave_month():
    hist = [5] * 12
    hist[2] = 1  # March least busy
    assert recommend_leave_month(hist) == 3
def test_add_employee_validation():
    init_db()
    session = get_session()

    emp_id = add_employee(
        session,
        name="John",
        aadhar_number="123456789012",
        pan_number="ABCDE1234F",
    )
    assert emp_id

    with pytest.raises(ValueError):
        add_employee(
            session,
            name="Jane",
            aadhar_number="12345",
            pan_number="ABCDE1234F",
        )

    with pytest.raises(ValueError):
        add_employee(
            session,
            name="Jim",
            aadhar_number="123456789012",
            pan_number="ABCDE123",
        )
