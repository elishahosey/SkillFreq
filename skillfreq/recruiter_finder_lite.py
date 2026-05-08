# recruiter_finder_lite.py
# Adds recruiter/contact search fields to your Job Tracker CSV.

import pandas as pd
from urllib.parse import quote_plus
from pathlib import Path

#currently hardcoded to my Job Tracker from Notion export - update as needed
INPUT_FILE = "Job Tracker 2026- v3 8dcc866429df82fe86770149001ecd0f_all.csv"
OUTPUT_FILE = "job_tracker_with_recruiter_finder.csv"


def get_col(row, possible_names):
    for name in possible_names:
        if name in row and pd.notna(row[name]):
            return str(row[name]).strip()
    return ""


def google_search_url(query):
    return f"https://www.google.com/search?q={quote_plus(query)}"


def linkedin_people_search_url(query):
    return f"https://www.linkedin.com/search/results/people/?keywords={quote_plus(query)}"


def build_queries(company, role):
    recruiter_query = f'site:linkedin.com/in "{company}" recruiter'
    talent_query = f'site:linkedin.com/in "{company}" "talent acquisition"'
    role_recruiter_query = f'site:linkedin.com/in "{company}" "{role}" recruiter'
    data_manager_query = f'site:linkedin.com/in "{company}" "data engineering manager"'
    backend_manager_query = f'site:linkedin.com/in "{company}" "software engineering manager" data'
    engineering_manager_query = f'site:linkedin.com/in "{company}" "engineering manager" "{role}"'

    return {
        "Recruiter Search Query": recruiter_query,
        "Talent Acquisition Search Query": talent_query,
        "Role Recruiter Search Query": role_recruiter_query,
        "Data Manager Search Query": data_manager_query,
        "Backend Manager Search Query": backend_manager_query,
        "Engineering Manager Search Query": engineering_manager_query,

        "Recruiter Google URL": google_search_url(recruiter_query),
        "Talent Acquisition Google URL": google_search_url(talent_query),
        "Role Recruiter Google URL": google_search_url(role_recruiter_query),
        "Data Manager Google URL": google_search_url(data_manager_query),
        "Backend Manager Google URL": google_search_url(backend_manager_query),
        "Engineering Manager Google URL": google_search_url(engineering_manager_query),

        "LinkedIn Recruiter People URL": linkedin_people_search_url(f"{company} recruiter"),
        "LinkedIn Talent People URL": linkedin_people_search_url(f"{company} talent acquisition"),
        "LinkedIn Data Manager People URL": linkedin_people_search_url(f"{company} data engineering manager"),
        "LinkedIn Engineering Manager People URL": linkedin_people_search_url(f"{company} engineering manager"),
    }


def should_check_contact(row):
    fit = get_col(row, ["Manual FIT (1-5)"]).lower()
    status = get_col(row, ["Status"]).lower()
    pivot = get_col(row, ["Pivotable?"]).lower()

    weak_signals = [
        "weak" in fit,
        "skip" in status,
        "rejected" in status,
        "denied" in status,
        "risky" in pivot,
        "not" in pivot,
    ]

    strong_signals = [
        "good" in fit,
        "submitted" in status,
        "applied" in status,
        "pivotable" in pivot,
        "pivot-safe" in pivot,
        "safe" in pivot,
    ]

    if any(weak_signals):
        return "skip"

    if any(strong_signals):
        return "check"

    return "optional"


def main():
    input_path = Path(INPUT_FILE)

    if not input_path.exists():
        raise FileNotFoundError(f"Could not find input file: {INPUT_FILE}")

    df = pd.read_csv(input_path)

    results = []

    for _, row in df.iterrows():
        company = get_col(row, ["Company", "company", "company_name", "employer"])
        role = get_col(row, ["Role", "title", "role_title", "job_title", "Job Title"])
        job_url = get_col(row, ["Link", "job_url", "Job URL"])

        if not company:
            queries = {}
            contact_priority = "missing_company"
        else:
            queries = build_queries(company, role)
            contact_priority = should_check_contact(row)

        results.append({
            "Contact Priority": contact_priority,
            "Contact Status": "not_checked",
            "Contact Name": "",
            "Contact Title": "",
            "Contact Profile URL": "",
            "Contacted Date": "",
            "Follow Up Date": "",
            "Contact Notes": "",
            "Original Job URL": job_url,
            **queries,
        })

    recruiter_df = pd.DataFrame(results)
    final_df = pd.concat([df, recruiter_df], axis=1)

    final_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Done. Created: {OUTPUT_FILE}")
    print("Recommended workflow: only check rows where Contact Priority == 'check'")


if __name__ == "__main__":
    main()