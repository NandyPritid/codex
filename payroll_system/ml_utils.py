from sklearn.ensemble import IsolationForest


def detect_anomalies(data):
    if len(data) < 5:
        return []
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit([[x] for x in data])
    return model.predict([[x] for x in data])


def predict_bonus_eligibility(days_worked, excess_leaves, festival_absences):
    if days_worked >= 300 and excess_leaves <= 0 and festival_absences <= 2:
        return True
    return False
