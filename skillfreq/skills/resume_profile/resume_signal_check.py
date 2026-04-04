
def suggest_stretch_tweaks(jd_matches: dict, profile_skills: dict, light_map: dict | None = None) -> list[dict]:
    light_map = light_map or {}
    suggestions = []

    for skill, count in jd_matches.items():
        if profile_skills.get(skill, 0):
            continue

        if skill in light_map:
            suggestions.append({
                "skill": skill,
                "type": "stretch",
                "note": f"Safe to mention lightly: {light_map[skill]}"
            })

    return suggestions

def suggest_profile_from_resume(resume_signals: dict, current_profile: dict) -> dict:
    resume_present = {k for k, v in resume_signals.items() if v > 0}
    profile_present = {k for k, v in current_profile.items() if v > 0}

    return {
        "missing_in_profile": sorted(resume_present - profile_present),
        "not_in_resume": sorted(profile_present - resume_present),
        "aligned": sorted(resume_present & profile_present),
    }

def print_profile_suggestions(result):
    print("\n=== PROFILE ALIGNMENT CHECK ===\n")

    if result["missing_in_profile"]:
        print("[+] In Resume but NOT in profile:")
        for s in result["missing_in_profile"]:
            print(f"- {s}")

    if result["not_in_resume"]:
        print("\n[!] In Profile but NOT visible in resume:")
        for s in result["not_in_resume"]:
            print(f"- {s}")

    print("\n================================\n")
