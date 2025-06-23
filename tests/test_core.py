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
