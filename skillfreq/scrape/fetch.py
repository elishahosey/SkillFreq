import pandas as pd
from pathlib import Path
import logging
from .extract import MultiLineHandler, test_url,_extract_best_apply_href

# I want to grab jobs from my tracker and then process them to get the skills and frequencies
#CSV (1),Notion(2),Excel(3),Google Sheets(4),Other(5)
# notion_path = '**' # replace with the actual path to your Notion export CSV file
# notion_data = pd.read_csv(notion_path)
#Columns: id	site	job_url	job_url_direct	title	company	location	date_posted	job_type	salary_source	interval	min_amount	max_amount	currency	is_remote	job_level	job_function	listing_type	emails	description	company_industry	company_url	company_logo	company_url_direct	company_addresses	company_num_employees	company_revenue	company_description	skills	experience_range	company_rating	company_reviews_count	vacancy_count	work_from_home_type
# BASE_DIR = Path(__file__).resolve().parents[1]
# jobspy_path = BASE_DIR / "../JobSpy/output/jobspy_jobs.csv"
# jobspy_data = pd.read_csv(jobspy_path)

# jd_urls = pd.DataFrame(jobspy_data, columns=['id','job_url','job_url_direct','title'])
logger = logging.getLogger(__name__)
logger.addHandler(MultiLineHandler(line_length=80))

def process_empty_urls(jd_urls):
    for i, row in jd_urls.iterrows():
        #any row without a direct url, try to find one by testing the main url and seeing if it redirects or if we can find a better url from the page
        if pd.isna(row['job_url_direct']) or row['job_url_direct'].strip() == "":
            main_url = row['job_url']
            resp = test_url(main_url)
            if resp and resp.url != main_url:
                jd_urls.at[i, 'job_url_direct'] = resp.url
                logger.info(f"URL redirected: {main_url} -> {resp.url}")
            else:
                logger.info(f"No redirect for URL: {main_url}. Attempting to find better URL from page content.")
                #try to find a better url from the page content
                best_href = _extract_best_apply_href(resp.text, base_url=main_url) if resp else None
                if best_href:
                    jd_urls.at[i, 'job_url_direct'] = best_href
                    logger.info(f"Found better URL from page content: {main_url} -> {best_href}")
    return jd_urls
    