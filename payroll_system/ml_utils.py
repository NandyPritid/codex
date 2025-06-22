"""Machine learning helpers for anomaly detection and bonus prediction.

These functions are intentionally lightweight and avoid heavy
dependencies so that the entire system can run on modest hardware.
"""

from sklearn.ensemble import IsolationForest


def detect_anomalies(data):
    """Identify outliers in a numeric sequence."""
    if len(data) < 5:
        return []
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit([[x] for x in data])
    return model.predict([[x] for x in data])


def predict_bonus_eligibility(days_worked, excess_leaves, festival_absences):
    """Return True if an employee meets basic bonus criteria."""
    if days_worked >= 300 and excess_leaves <= 0 and festival_absences <= 2:
        return True
    return False


def recommend_leave_month(history: list[int]) -> int:
    """Return an index of the month with minimal historic leave usage.

    Parameters
    ----------
    history : list[int]
        Twelve numbers representing number of employees on leave per month.

    Returns
    -------
    int
        Month number (1-12) suggested for scheduling new leave.
    """
    if len(history) != 12:
        raise ValueError('history must contain 12 monthly values')
    return history.index(min(history)) + 1
