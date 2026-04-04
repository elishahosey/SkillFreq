from __future__ import annotations
import logging
from textwrap import wrap
import re
import json
import trafilatura
import requests
from skillfreq.parse.parsers import *
from skillfreq.scrape.apply_buttons.glassdoor_apply import *  
from skillfreq.scrape.apply_buttons.base import *  
from skillfreq.scrape.apply_buttons.indeed_apply import *  
from skillfreq.scrape.apply_buttons.linkedin_apply import *  
from skillfreq.parse.parsers import _extract_best_apply_href

class MultiLineHandler(logging.StreamHandler):
    def __init__(self, line_length: int):
        logging.StreamHandler.__init__(self)
        self.line_length = line_length

    def emit(self, record):
        record.msg = "\n".join(wrap(record.msg, self.line_length))
        super().emit(record)

logger = logging.getLogger(__name__)
logger.addHandler(MultiLineHandler(line_length=80))

'''
Extractors depending on platform
'''
def extract_apply_link(url: str) -> str | None:
    result = None
    if "indeed" in url:
        result = detect_indeed_apply(url)
    elif "linkedin" in url:
        result = detect_linkedin_apply(url)
    elif "glassdoor" in url:
        result = detect_glassdoor_apply(url)
    
    if result and isinstance(result, dict):
        return result.get('external_url') or url
    return url

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
    if "rippling.com" in u:
        return RipplingParser(url, html)
    if "oraclecloud.com" in u:
        return OracleCloudParser(url,html)

    # default fallback
    return GenericParser(url, html)




def test_url(url: str):
    logger.info(f"Testing URL (before GET): {url}")

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

        logging.info(f"Received response for {url} - Status: {resp.status_code} - Len: {len(resp.text)}")
        logger.info(f"Testing URL (after GET): {url} - Status: {resp.status_code} - Len: {len(resp.text)}")
        logger.info(f"Final URL: {resp.url}")
        logger.info(f"Snippet: {resp.text[:300].replace('\n', ' ')}")

        return resp

    except Exception as e:
        logger.error(f"GET FAILED for {url}: {repr(e)}")
        return None

def extract_text_from_url(url: str) -> str | None:
    try:
       #TODO: if there are no direct urls, find it and then test those urls to 
       # find one that works, then extract from that one
       
        resp = test_url(url)
        final_url = resp.url if resp else url
        #find apply button
        if "indeed" in url or "linkedin" in url or "glassdoor" in url:
             final_url = extract_apply_link(url)
        
        # If final_url changed (e.g., external apply link), fetch HTML from the new URL
        original_url = resp.url if resp else url
        if final_url != original_url:
            resp = test_url(final_url)
        
        #check for new html after redirect
        if "indeed" in url or "linkedin" in url or "glassdoor" in url:
            redirected_html=fetch_rendered_html(final_url)
            parse_resp= detect_parser(final_url, html=redirected_html)
            logger.info(f"HTML length of REDIRECTED URL: {len(redirected_html) if redirected_html else 0}")
        else: 
            parse_resp= detect_parser(final_url, html=resp.text if resp else None)
        
        logger.info(f"Using parser {parse_resp.__class__.__name__} for URL: {final_url}")
        #logger.info(f"Parser Response Object: {parse_resp}")
        if parse_resp:
            parsed_text = parse_resp.parse()
            logger.info(f"Parsed object for {final_url}: {type(parsed_text)} - Length: {len(parsed_text) if parsed_text else 'N/A'}")
            for k, v in parsed_text.items():
                logger.info(f"Metadata - {k}: {v}")
            return parsed_text
           # return parse_resp.parse()
        
    except Exception as e:
        logger.error(f"Extraction failed for {url} due to {repr(e)}")
        # return None
        return None