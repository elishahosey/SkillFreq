
#TODO: Add in Unscored (no role profile) since role isn't in yml, don't overtrust label for now
def classify(score: float, flags: dict) -> str:
    if flags.get("has_hard_requirement_blockers"):
        return "Skip"

    if flags.get("has_modern_stack_blockers"):
        if score >= 22:
            return "Low Match"
        return "Minimal Match Present"

    if flags.get("is_lead_like"):
        if score >= 18:
            return "Low Match"
        return "Minimal Match Present"

    years_required = flags.get("years_required")
    if isinstance(years_required, tuple):
        max_years = years_required[1]
    elif isinstance(years_required, int):
        max_years = years_required
    else:
        max_years = None

    # Light seniority dampening
    if max_years is not None and max_years >= 7:
        if score >= 22:
            return "Low Match"
        return "Minimal Match Present"

    if score >= 35:
            return "High Match"
    elif score >= 28:
        return "Moderate Match"
    elif score >= 22:
        return "Low Match"
    else:
        return "Minimal Match Present"