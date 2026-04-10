import csv
import pandas as pd
from datetime import datetime
from jobspy import scrape_jobs

now = datetime.now()
date = f"{now.month}-{now.day}-{now.strftime('%y')}"
filename= "jobs-"+date+".csv"
'''
Too broad for the pipeline I'm applying
Previous search list was too broad for the current job-search funnel.
It pulled in too many SWE/platform/backend roles that lowered alignment.
DE / integration should remain the primary focus for now.


search_terms = [
    "analytics platform engineer",
    "data reliability engineer",
    "data platform developer",
    "data infrastructure developer",
    "data engineer",
    "backend engineer",
    "backend software engineer",
    "software engineer backend",
    "data platform engineer",
    "data infrastructure engineer",
    "data systems engineer",
    "data pipeline engineer",
    "etl engineer",
    "etl developer",
    "integration engineer",
    "data integration engineer",
    "data ingestion engineer",
    "data developer",
    "sql developer",
    "database developer",
    "database engineer",
    "analytics engineer",
    "reporting engineer",
    "data operations engineer",
    "platform engineer",
    "software engineer platform",
    "systems engineer",
    "distributed systems engineer",
    "api engineer",
    "api developer",
    "application engineer",
    "services engineer"
]
'''

# Apply selectively from this list (~25% or less of total applications).
# Use only when the JD is still clearly SQL / pipeline / integration heavy.
secondary_terms = [
    "data platform engineer",
    "data systems engineer",
    "data infrastructure engineer",
    "software engineer data",
    "backend engineer data",
    "api engineer",
    "api developer",
    "backend data engineer",
    "data platform developer",
    "pipeline engineer",
    "data reliability engineer",
    "application engineer integration",
    "integration engineer",
    "integration developer"
]

# Primary search lane.
# Resume signal is strongest here, so these should make up most applications.
core_terms = [
    "data engineer",
    "junior data engineer",
    "associate data engineer",
    "etl engineer",
    "etl developer",
    "data integration engineer",
    "etl integration engineer",
    "api integration engineer",
    "systems integration engineer data",
    "data pipeline engineer",
    "data ingestion engineer",
    "sql developer",
    "database developer",
    "data operations engineer",
    "data quality engineer",
    "application developer data",
    "software engineer data engineering"
]

bridge_roles= [
"backend engineer",
"backend developer",
"systems analyst",
"automation engineer",
"database engineer",
"application engineer"
]

FALLBACK=False # whether to pull in bridge roles if core/secondary don't yield enough results

all_jobs = []

if FALLBACK:
    for term in bridge_roles:
        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter", "google"],
            search_term=term,
            google_search_term=f"{term} jobs since the past 1 days",
            location="Texas",
            results_wanted=20,
            hours_old=24,
            country_indeed='USA',
            linkedin_fetch_description=True
        )
        jobs["search_lane"] = "bridge"
        jobs["search_term_used"] = term
        all_jobs.extend(jobs.to_dict(orient="records"))

        print(f"Found BRIDGE jobs for term '{term}': {len(jobs)}")
else:
        for term in core_terms:
            jobs = scrape_jobs(
                site_name=["indeed", "linkedin", "zip_recruiter", "google"], # "glassdoor", "bayt", "naukri", "bdjobs"
                search_term=term,
                google_search_term=f"{term} jobs since the past 1 days",
                #google_search_term=f"{term} contract jobs in Texas since the past 1 days",
                location="Texas",
                results_wanted=100,
                hours_old=24 * 1, # 1 day
                country_indeed='USA',
                linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
                # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
            )
            jobs["search_lane"] = "core"
            jobs["search_term_used"] = term
            print(f"Found CORE jobs for term '{term}': {len(jobs)}")
            all_jobs.extend(jobs.to_dict(orient="records"))
            
        for term in secondary_terms:
            jobs = scrape_jobs(
                site_name=["indeed", "linkedin", "zip_recruiter", "google"],
                search_term=term,
                google_search_term=f"{term} jobs since the past 1 days",
                location="Texas",
                results_wanted=20,
                hours_old=24,
                country_indeed='USA',
                linkedin_fetch_description=True
            )
            jobs["search_lane"] = "secondary"
            jobs["search_term_used"] = term
            all_jobs.extend(jobs.to_dict(orient="records"))

            print(f"Found SECONDARY jobs for term '{term}': {len(jobs)}")
            
            
        jobs = pd.DataFrame(all_jobs)

        # Assign review priority based on search lane (core = 1, secondary = 2).
        jobs["review_priority"] = jobs["search_lane"].map({
            "core": 1,
            "secondary": 2
        })

        jobs = jobs.sort_values(by=["review_priority", "date_posted"], ascending=[True, False])

        # Remove duplicates based on job_url if available, otherwise use id or a combination of title/company/location.
        if "job_url" in jobs.columns:
            jobs = jobs.drop_duplicates(subset=["job_url"])
        elif "id" in jobs.columns:
            jobs = jobs.drop_duplicates(subset=["id"])
        else:
            jobs = jobs.drop_duplicates(subset=["title", "company", "location"])

        jobs.to_csv(f"{filename}", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel