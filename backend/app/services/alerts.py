THRESHOLDS = {"advisory": 35, "watch": 50, "warning": 65, "severe_warning": 85}

def severity_for(probability: int) -> str | None:
    if probability >= THRESHOLDS["severe_warning"]: return "Severe Warning"
    if probability >= THRESHOLDS["warning"]: return "Warning"
    if probability >= THRESHOLDS["watch"]: return "Watch"
    if probability >= THRESHOLDS["advisory"]: return "Advisory"
    return None
