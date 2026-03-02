from __future__ import annotations
import re
import json
import trafilatura
import requests
from skillfreq.parse.parsers import *

'''
Extractors depending on platform
'''


def detect_parser(url: str, html: str) -> BaseParser:
    u = url.lower()
    if "myworkdayjobs.com" in u:
        return WorkdayParser(url, html)
    if "greenhouse.io" in u:
        return GreenhouseParser(url, html)
    if "ashbyhq.com" in u:
        return AshbyParser(url, html)
    if "smartrecruiters.com" in u:
        return SmartRecruitersParser(url, html)
    if "icims.com" in u:
        return ICIMSParser(url, html)
    if "apexfintechsolutions.com" in u:
        return ApexParser(url, html)
    # if "taleo.net" in u:
    #     return TaleoParser(url, html)
    # if "brassring.com" in u:
    #     return BrassRingParser(url, html)
    # if "ultipro.com" in u:
    #     return UltiproParser(url, html)
    # if "acquiretm.com" in u:
    #     return AcquireTMParser(url, html)
    # if "paycor.com" in u:
    #     return PaycorParser(url, html)
    if "rippling.com" in u:
        return RipplingParser(url, html)

    # default fallback
    return GenericParser(url, html)



# def extract_ashby_description(html: str) -> str | None:
    """
    Extract job description from Ashby-hosted job pages.
    Returns plain text description if found.
    """

    # Detect Ashby
    if "window.__appData" not in html:
        return None

    '''
    Starting at window.__appdata, extract any whitespace,
    then anything followed immediately by a literal equals sign. 
    Then extract anything (0/more) up to the parenthesis 
    ( any character (0/more) up to the first closing parenthesis,followed by a semicolon. 
    Then extract anyhting (0/more) up to 'fetch(',which should be the next part of the script
    
    This should give us the JSON blob containing the job description.
    '''
    
    match = re.search(
        r"window\.__appData\s*=\s*({.*?});\s*fetch\(",
        html,
        flags=re.DOTALL
    )

    if not match:
        return None

    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None

    posting = data.get("posting", {})

    # Prefer plain text
    return posting.get("descriptionPlainText") \
        or posting.get("descriptionHtml")

def print_to_file(filename: str, content: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def test_url(url: str):
    print(f"Testing URL (before GET): {url}")

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    }

    try:
        s = requests.Session()
        s.trust_env = False  # ignores HTTP_PROXY/HTTPS_PROXY env vars that can cause hangs

        resp = s.get(
            url,
            headers=headers,
            timeout=(5, 15),        # (connect timeout, read timeout)
            allow_redirects=True,
        )

        print(f"Testing URL (after GET): {url} - Status: {resp.status_code} - Len: {len(resp.text)}")
        print("Final URL:", resp.url)
        print("Snippet:", resp.text[:300].replace("\n", " "))

        return resp

    except Exception as e:
        print(f"GET FAILED for {url}: {repr(e)}")
        return None

def extract_text_from_url(url: str) -> str | None:
    try:
        resp = test_url(url)        # MVP: use trafilatura for now, which is simple and robust
        final_url = resp.url if resp else url

       
       #TODO: parse the response based on platform (Ashby, Greenhouse, Lever, etc.) to extract the job description.
        parse_resp= detect_parser(final_url, html=resp.text if resp else None)
        if parse_resp:
            return parse_resp.parse()
        
        #branch depending on platform
        
        # print_to_file("extracted_text.txt", resp)
        # if resp:
        #     downloaded = trafilatura.fetch_url(url)
        #     if not downloaded:
        #         return None
        #     text = trafilatura.extract(downloaded)


        #     return text
    except Exception as e:
        print(f"Extraction failed for {url} due to {repr(e)}")
        return None