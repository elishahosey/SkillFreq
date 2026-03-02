
#TODO: Add in Unscored (no role profile) since role isn't in yml, don't overtrust label for now
def classify(score: float) -> str:
    if score >= 0.75:
        return "Strong Apply"
    elif score >= 0.60:
        return "Strategic Apply"
    elif score >= 0.45:
        return "Stretch"
    else:
        return "Skip"