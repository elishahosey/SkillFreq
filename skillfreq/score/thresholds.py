
#TODO: Add in Unscored (no role profile) since role isn't in yml, don't overtrust label for now
def classify(score: float, flags: dict) -> str:
    if flags.get("has_hard_requirement_blockers"):
        return "Skip"

    if flags.get("is_lead_like"):
        if score >= 12:
            return "Stretch"
        else:
            return "Skip"

    if score >= 25:
        return "Strong Apply"
    elif score >= 20:
        return "Strategic Apply"
    elif score >= 12:
        return "Stretch"
    else:
        return "Skip"