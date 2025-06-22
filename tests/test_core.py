import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from payroll_system.ml_utils import predict_bonus_eligibility


def test_bonus_eligibility():
    assert predict_bonus_eligibility(300, 0, 2) is True
    assert predict_bonus_eligibility(250, 0, 2) is False
