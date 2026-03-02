import pandas as pd
import trafilatura

# I want to grab jobs from my tracker and then process them to get the skills and frequencies
#CSV (1),Notion(2),Excel(3),Google Sheets(4),Other(5)
path = 'C:\\Users\\ehose\\\Development\\SkillFreq\\CurrentExportFromNotion\\JobTracker2026.csv'
data = pd.read_csv(path)


def process_JD(link,job_record):
    request = trafilatura.fetch_url(link)
    if request is not None:
        extracted_text = trafilatura.extract(request)
        job_record['extracted_text'] = extracted_text
    return job_record
    
    
    

def preprocess(data):
    #only grab link column:
    job = data[['Company','Role','Link']]
  
    #i just care about links for now, so I will just loop through the links and process them
    for i, row in job.iterrows():
        link = row['Link']
        job_record=process_JD(link,i) #i used for quick indexing but will need to change this to be more robust later
        job_records.append(job_record)
        
    return

    
job_record = {
  "job_id": "",
  "url": "",
  "title": "",
  "company": "",
  "extracted_text": "",
  "extracted_at": "",
  "error": ""
}

job_records = []
preprocess(data)