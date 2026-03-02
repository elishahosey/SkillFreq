import pandas as pd
import nltk
import requests
from pydparser import  JdParser
import os

os.environ["NLTK_DATA"] = r"C:\\Users\\ehose\\Development\\SkillFreq\\.nltk_data"

def checkNLTKData():
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")


path = '.\CurrentExportFromNotion\JobTracker2026.csv'
data = pd.read_csv(path)


def process_JD(link):
    #scrape the job description from the link and then use the JdParser to extract the skills and frequencies
    request=requests.get(link)
    if request.status_code == 200:
        parser = JdParser(request.text)
        skills = parser.extract_skills()
        print(skills)
    
    return
    
    
    
    
def preprocess(data):
    job_descriptions = [] # sections are usually : what you'll do, what you'll need, nice to have, who you are.
    for d in data:
        process_JD(d['Link'])
        
    
        
    
    return

    
checkNLTKData()
