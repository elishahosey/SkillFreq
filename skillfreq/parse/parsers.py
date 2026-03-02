from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
import re
from typing import Any, Dict, Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import html as html_lib

import requests


'''
Generic structured extractors
'''

def _find_jobposting_jsonld(soup: BeautifulSoup) -> Optional[dict]:
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text(strip=True)
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except Exception:
            continue

        candidates = data if isinstance(data, list) else [data]
        for item in candidates:
            if not isinstance(item, dict):
                continue
            if item.get("@type") == "JobPosting":
                return item
            if isinstance(item.get("@graph"), list):
                for g in item["@graph"]:
                    if isinstance(g, dict) and g.get("@type") == "JobPosting":
                        return g
    return None


def _jsonld_to_fields(jp: dict) -> Dict[str, str]:
    title = (jp.get("title") or "").strip()
    org = jp.get("hiringOrganization") or {}
    company = (org.get("name") or "").strip() if isinstance(org, dict) else ""
    description = _clean_text(jp.get("description") or "")

    # Location can be list/dict
    loc = jp.get("jobLocation")
    if isinstance(loc, list) and loc:
        loc = loc[0]
    location = ""
    if isinstance(loc, dict):
        addr = loc.get("address")
        if isinstance(addr, dict):
            parts = [addr.get("addressLocality"), addr.get("addressRegion"), addr.get("addressCountry")]
            parts = [p for p in parts if p]
            location = ", ".join(parts)

    return {
        "title": title,
        "company": company,
        "location": location,
        "description": description,
    }


def _extract_nextjs_data(soup: BeautifulSoup) -> Optional[dict]:
    tag = soup.find("script", id="__NEXT_DATA__")
    if not tag:
        return None
    raw = tag.string or tag.get_text(strip=True)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None


def _extract_json_from_assignment(html: str, var_names: list[str]) -> Optional[dict]:
    """
    Tries to extract big JSON blobs from:
      window.__INITIAL_STATE__ = {...};
      window.__APOLLO_STATE__ = {...};
      __NUXT__=...
    """
    for name in var_names:
        # non-greedy, but allow large blobs
        m = re.search(rf"{re.escape(name)}\s*=\s*({{.*?}})\s*;?", html, flags=re.S)
        if m:
            blob = m.group(1)
            try:
                return json.loads(blob)
            except Exception:
                pass
    return None

def _meta_fallback(soup: BeautifulSoup, url: str) -> Dict[str, str]:
    canon = _get_meta(soup, prop="og:url") or url
    title = _get_meta(soup, prop="og:title") or (soup.title.string.strip() if soup.title and soup.title.string else "")
    desc = _get_meta(soup, name="description") or _get_meta(soup, prop="og:description")
    return {
        "url": canon,
        "title": title.strip(),
        "company": "",
        "location": "",
        "description": _clean_text(desc),
    }


'''
UA
'''
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
       "AppleWebKit/537.36 (KHTML, like Gecko) "
       "Chrome/122.0.0.0 Safari/537.36")


'''
Block measures
'''
def looks_like_indeed_block_page(html: str) -> bool:
        h = (html or "").lower()
        return "color-scheme:light dark" in h and "<style>:root" in h
    

def _resolve_final_url(url: str, timeout: int = 20) -> str:
    """Resolve tracking/redirect links to their final destination URL."""
    s = requests.Session()
    s.headers.update({"User-Agent": _UA})
    # HEAD sometimes blocked; GET is more reliable.
    r = s.get(url, timeout=timeout, allow_redirects=True)
    if r.status_code in (403, 429):
        raise FetchBlocked(f"{r.status_code} blocked resolving {url}")
    r.raise_for_status()
    return r.url

'''
Helper functions
'''



def _first_text(el) -> Optional[str]:
    if not el:
        return None
    txt = el.get_text(" ", strip=True)
    return txt.strip() if txt else None


def _fetch_html(url: str, timeout: int = 20) -> str:
    headers = {
        "User-Agent": _UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    s = requests.Session()
    s.headers.update(headers)
    # warm cookies (often helps with Indeed)
    s.get("https://www.indeed.com/", timeout=timeout)
    r = s.get(url, headers={"Referer": "https://www.indeed.com/"}, timeout=timeout)
    # If blocked, raise a specific exception
    if r.status_code == 403:
        raise FetchBlocked(f"403 blocked for {url}")
    
    r.raise_for_status()
    return r.text

def _strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", " ", s or "")

def _clean_text(s: str) -> str:
    s = html_lib.unescape(s or "")
    s = _strip_tags(s)
    return re.sub(r"\s+", " ", s).strip()

def _get_meta(soup: BeautifulSoup, *, name: str | None = None, prop: str | None = None) -> str:
    if name:
        tag = soup.find("meta", attrs={"name": name})
        return (tag.get("content") or "").strip() if tag else ""
    if prop:
        tag = soup.find("meta", attrs={"property": prop})
        return (tag.get("content") or "").strip() if tag else ""
    return ""

def _find_jobposting_jsonld(soup: BeautifulSoup) -> dict | None:
    blocks = soup.find_all("script", attrs={"type": "application/ld+json"})
    for b in blocks:
        raw = (b.string or "").strip()
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue

        # Could be dict or list
        if isinstance(data, dict) and data.get("@type") == "JobPosting":
            return data

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("@type") == "JobPosting":
                    return item

    return None

class FetchBlocked(Exception):
    pass


class BaseParser(ABC):
    def __init__(self, url: str, html: str | None = None):
        self.url = url
        self.html = html  #TODO: Read the architecture book=> injection for testing

    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        """
        Returns structured job data.
        Must include at minimum:
        {
            "title": str,
            "company": str,
            "location": str,
            "description": str,
        }
        """
        pass
    
class GenericParser(BaseParser):
    def parse(self) -> dict:
        if not self.html:
            raise ValueError("GenericParser requires injected HTML.")

        soup = BeautifulSoup(self.html, "html.parser")

        # 1) JSON-LD JobPosting
        jp = _find_jobposting_jsonld(soup)
        if jp:
            title = jp.get("title", "")
            company = (jp.get("hiringOrganization", {}) or {}).get("name", "")
            location = ((jp.get("jobLocation", {}) or {}).get("address", {}) or {}).get("addressLocality", "")
            description = _clean_text(jp.get("description", ""))

            return {
                "source": "generic",
                "url": _get_meta(soup, prop="og:url") or self.url,
                "title": title,
                "company": company,
                "location": location,
                "description": description,
            }

        # 2) Meta tags
        url = _get_meta(soup, prop="og:url") or self.url
        title = (_get_meta(soup, prop="og:title") or "").strip()
        if not title:
            title = (soup.title.string or "").strip() if soup.title else ""

        description = _get_meta(soup, name="description") or _get_meta(soup, prop="og:description")
        description = _clean_text(description)

        # 3) Last resort: pull visible page text
        if len(description) < 200:
            container = soup.find("main") or soup.find("article") or soup.body
            if container:
                body_text = container.get_text("\n", strip=True)
                # avoid returning a whole navigation dump
                description = _clean_text(body_text)[:12000] or description

        return {
            "source": "generic",
            "url": url,
            "title": title,
            "company": "",
            "location": "",
            "description": description,
        }
        
        







class ApexParser(BaseParser):
    """
    careers.apexfintechsolutions.com job pages.

    Returns (minimum):
      {
        "title": str,
        "company": str,
        "location": str,
        "description": str,
      }

    Extras:
      "job_id": str | "",
      "workplace_type": str | "",
      "source": str,
      "url": str
    """
    
    def _company_from_jsonld(self, jp: dict) -> str:
        ho = jp.get("hiringOrganization")
        if isinstance(ho, dict):
            return _clean_text(str(ho.get("name", "")))
        return ""

    def _location_from_jsonld(self, jp: dict) -> str:
        jl = jp.get("jobLocation")
        # dict or list
        if isinstance(jl, list) and jl:
            jl = jl[0]
        if not isinstance(jl, dict):
            return ""

        addr = jl.get("address")
        if not isinstance(addr, dict):
            return ""

        city = _clean_text(str(addr.get("addressLocality", "")))
        region = _clean_text(str(addr.get("addressRegion", "")))
        country = _clean_text(str(addr.get("addressCountry", "")))

        parts = [p for p in [city, region, country] if p]
        return ", ".join(parts)
    
    def _fetch(self, url: str) -> str:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        return r.text

    # ---------------- Inference ----------------
    def _infer_job_id(self, url: str, jp: Optional[dict]) -> str:
        # Prefer JSON-LD identifier when present
        if jp:
            ident = jp.get("identifier")
            if isinstance(ident, dict):
                val = ident.get("value") or ident.get("name")
                if val:
                    return _clean_text(str(val))
            elif isinstance(ident, str):
                return _clean_text(ident)

        m = re.search(r"(JR\d+)", url, flags=re.IGNORECASE)
        return (m.group(1).upper() if m else "")

    def _infer_location(self, text: str) -> str:
        # Basic "Austin, TX" match
        m = re.search(r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*),\s*([A-Z]{2})\b", text)
        return f"{m.group(1)}, {m.group(2)}" if m else ""

    def _infer_workplace_type(self, text: str) -> str:
        # Keep it simple and consistent for SkillFreq tagging
        if re.search(r"\bhybrid\b", text, flags=re.IGNORECASE):
            return "Hybrid"
        if re.search(r"\bremote\b", text, flags=re.IGNORECASE):
            return "Remote"
        if re.search(r"\bon[-\s]?site\b", text, flags=re.IGNORECASE):
            return "On-site"
        return ""

    SOURCE = "apexfintechsolutions_careers"

    def parse(self) -> Dict[str, Any]:
        html = self.html or self._fetch(self.url)
        soup = BeautifulSoup(html, "html.parser")

        # ---- 1) Schema.org JSON-LD JobPosting (best)
        jp = _find_jobposting_jsonld(soup)
        if jp:
            title = _clean_text(str(jp.get("title", "")))
            company = self._company_from_jsonld(jp) or "Apex Fintech Solutions"
            location = self._location_from_jsonld(jp)
            description = _clean_text(str(jp.get("description", "")))
            workplace_type = self._infer_workplace_type(description or soup.get_text(" ", strip=True))
            job_id = self._infer_job_id(self.url, jp)

            return {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "job_id": job_id,
                "workplace_type": workplace_type,
                "source": self.SOURCE,
                "url": self.url,
            }

        # ---- 2) HTML fallback
        title = _clean_text(_get_meta(soup, prop="og:title")) or _clean_text(_get_meta(soup, name="title"))
        if not title:
            h1 = soup.find("h1")
            title = _clean_text(h1.get_text(" ", strip=True) if h1 else "")

        # description: try common containers, then main, then meta description
        desc_node = (
            soup.select_one('[data-qa="job-description"]')
            or soup.select_one('[data-testid="job-description"]')
            or soup.select_one(".job-description")
            or soup.select_one(".jobDescription")
            or soup.select_one("article")
            or soup.select_one("main")
        )
        description = _clean_text(str(desc_node)) if desc_node else ""
        if len(description) < 200:
            description = _clean_text(_get_meta(soup, prop="og:description")) or _clean_text(_get_meta(soup, name="description"))

        # location: heuristic from page text
        page_text = soup.get_text(" ", strip=True)
        location = self._infer_location(page_text)

        workplace_type = self._infer_workplace_type(page_text)
        job_id = self._infer_job_id(self.url, None)

        return {
            "title": title,
            "company": "Apex Fintech Solutions",
            "location": location,
            "description": description,
            "job_id": job_id,
            "workplace_type": workplace_type,
            "source": self.SOURCE,
            "url": self.url,
        }



class InterfolioParser(GenericParser):
    source = "interfolio"


class RecruiterflowParser(GenericParser):
    source = "recruiterflow"

    def parse(self) -> Dict[str, Any]:
        html = self.html or _fetch_html(self.url)
        soup = BeautifulSoup(html, "html.parser")

        # JSON-LD first
        jp = _find_jobposting_jsonld(soup)
        if jp:
            out = {"source": self.source, "url": self.url, **_jsonld_to_fields(jp)}
            return out

        # Try common SPA state blobs
        state = _extract_json_from_assignment(html, [
            "window.__INITIAL_STATE__",
            "window.__PRELOADED_STATE__",
            "window.__APOLLO_STATE__",
        ])
        if isinstance(state, dict):
            # Best-effort: scan for something that looks like a job
            text = json.dumps(state)
            title = ""
            company = ""
            location = ""
            desc = ""
            # Heuristics
            tm = re.search(r'"title"\s*:\s*"([^"]{3,120})"', text)
            dm = re.search(r'"description"\s*:\s*"(.{200,}?)"', text)
            if tm:
                title = html_lib.unescape(tm.group(1))
            if dm:
                desc = _clean_text(dm.group(1))
            return {
                "source": self.source,
                "url": self.url,
                "title": title,
                "company": company,
                "location": location,
                "description": desc,
            }

        # Fallback to meta/text
        out = _meta_fallback(soup, self.url)
        out["source"] = self.source
        if len(out["description"]) < 200:
            main = soup.find("main") or soup.body
            out["description"] = _clean_text(main.get_text("\n", strip=True))[:12000] if main else out["description"]
        return out


class SchoolJobsParser(BaseParser):
    source = "schooljobs"

    def parse(self) -> Dict[str, Any]:
        html = self.html or _fetch_html(self.url)
        soup = BeautifulSoup(html, "html.parser")

        # JSON-LD first
        jp = _find_jobposting_jsonld(soup)
        if jp:
            return {"source": self.source, "url": self.url, **_jsonld_to_fields(jp)}

        # SchoolJobs/NEOGOV-style pages often have a clear job description container.
        title = _first_text(soup.select_one("h1")) or _get_meta(soup, prop="og:title")
        company = _first_text(soup.select_one(".company")) or ""
        location = _first_text(soup.select_one(".job-location")) or ""

        # Heuristic containers
        desc_container = (
            soup.select_one("#job-details")
            or soup.select_one("#jobDescriptionText")
            or soup.select_one(".job-description")
            or soup.find("main")
            or soup.body
        )
        description = ""
        if desc_container:
            description = _clean_text(desc_container.get_text("\n", strip=True))[:20000]

        out = {
            "source": self.source,
            "url": _get_meta(soup, prop="og:url") or self.url,
            "title": (title or "").strip(),
            "company": company.strip(),
            "location": location.strip(),
            "description": description,
        }
        if len(out["description"]) < 200:
            out["description"] = _meta_fallback(soup, self.url)["description"]
        return out


class LensaParser(GenericParser):
    source = "lensa"


class ApplyToJobParser(GenericParser):
    source = "applytojob"

    def parse(self) -> Dict[str, Any]:
        html = self.html or _fetch_html(self.url)
        soup = BeautifulSoup(html, "html.parser")

        # JSON-LD first
        jp = _find_jobposting_jsonld(soup)
        if jp:
            return {"source": self.source, "url": self.url, **_jsonld_to_fields(jp)}

        # Many applytojob pages are Next.js
        nd = _extract_nextjs_data(soup)
        if isinstance(nd, dict):
            # Best-effort crawl for fields inside the JSON
            blob = json.dumps(nd)
            title = ""
            company = ""
            location = ""
            desc = ""

            tm = re.search(r'"title"\s*:\s*"([^"]{3,150})"', blob)
            cm = re.search(r'"company(Name)?"\s*:\s*"([^"]{2,150})"', blob)
            lm = re.search(r'"location"\s*:\s*"([^"]{2,150})"', blob)
            dm = re.search(r'"description"\s*:\s*"(.{200,}?)"', blob)

            if tm: title = html_lib.unescape(tm.group(1))
            if cm: company = html_lib.unescape(cm.group(2))
            if lm: location = html_lib.unescape(lm.group(1))
            if dm: desc = _clean_text(dm.group(1))

            return {
                "source": self.source,
                "url": _get_meta(soup, prop="og:url") or self.url,
                "title": title,
                "company": company,
                "location": location,
                "description": desc or _meta_fallback(soup, self.url)["description"],
            }

        # fallback
        out = _meta_fallback(soup, self.url)
        out["source"] = self.source
        return out


class AdzunaParser(GenericParser):
    source = "adzuna"


class HireologyParser(GenericParser):
    source = "hireology"

    def parse(self) -> Dict[str, Any]:
        # Hireology often has JSON-LD; if not, it’s usually very parseable HTML.
        html = self.html or _fetch_html(self.url)
        soup = BeautifulSoup(html, "html.parser")

        jp = _find_jobposting_jsonld(soup)
        if jp:
            return {"source": self.source, "url": self.url, **_jsonld_to_fields(jp)}

        title = _first_text(soup.select_one("h1")) or _get_meta(soup, prop="og:title")
        # Company/location sometimes in header blocks
        company = _first_text(soup.select_one('[data-testid="company-name"]')) or ""
        location = _first_text(soup.select_one('[data-testid="job-location"]')) or ""

        desc_container = soup.find("main") or soup.select_one(".job-description") or soup.body
        description = _clean_text(desc_container.get_text("\n", strip=True))[:20000] if desc_container else ""

        out = {
            "source": self.source,
            "url": _get_meta(soup, prop="og:url") or self.url,
            "title": (title or "").strip(),
            "company": company.strip(),
            "location": location.strip(),
            "description": description or _meta_fallback(soup, self.url)["description"],
        }
        return out

class ADPWorkforceNowParser(GenericParser):
    source = "adp_workforcenow"

    def parse(self) -> Dict[str, Any]:
        html = self.html or _fetch_html(self.url)
        soup = BeautifulSoup(html, "html.parser")

        # JSON-LD first
        jp = _find_jobposting_jsonld(soup)
        if jp:
            return {"source": self.source, "url": self.url, **_jsonld_to_fields(jp)}

        # Many ADP career pages are SPA/Next-ish. Try __NEXT_DATA__.
        nd = _extract_nextjs_data(soup)
        if isinstance(nd, dict):
            blob = json.dumps(nd)
            title = ""
            location = ""
            description = ""

            tm = re.search(r'"jobTitle"\s*:\s*"([^"]{3,180})"', blob) or re.search(r'"title"\s*:\s*"([^"]{3,180})"', blob)
            lm = re.search(r'"location"\s*:\s*"([^"]{2,180})"', blob)
            dm = re.search(r'"jobDescription"\s*:\s*"(.{200,}?)"', blob) or re.search(r'"description"\s*:\s*"(.{200,}?)"', blob)

            if tm: title = html_lib.unescape(tm.group(1))
            if lm: location = html_lib.unescape(lm.group(1))
            if dm: description = _clean_text(dm.group(1))

            return {
                "source": self.source,
                "url": _get_meta(soup, prop="og:url") or self.url,
                "title": title,
                "company": _get_meta(soup, prop="og:site_name") or "",
                "location": location,
                "description": description or _meta_fallback(soup, self.url)["description"],
            }

        # fallback
        out = _meta_fallback(soup, self.url)
        out["source"] = self.source
        if len(out["description"]) < 200 and soup.body:
            out["description"] = _clean_text(soup.body.get_text("\n", strip=True))[:12000]
        return out


class HCSHiringParser(GenericParser):
    source = "hcshiring"

class GuardianJobsParser(GenericParser):
    source = "guardian_jobs"

class RecruitRookieParser(GenericParser):
    source = "recruitrookie"
    
class AshbyParser(BaseParser):
    def parse(self) -> Dict[str, Any]:
        if not self.html:
            raise ValueError("AshbyParser requires HTML to be provided (inject html).")

        soup = BeautifulSoup(self.html, "html.parser")

        # 1) Title (often: "<role> @ <company>")
        raw_title = (soup.title.string or "").strip() if soup.title else ""
        role, company = self._split_title(raw_title)

        # 2) Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = (meta_desc.get("content") or "").strip() if meta_desc else ""
        # Decode HTML entities like &#39;
        description = html_lib.unescape(description)

        # 3) Canonical/OG URL (helps dedupe)
        og_url = soup.find("meta", attrs={"property": "og:url"})
        canonical_url = (og_url.get("content") or "").strip() if og_url else self.url

        # Optional: pull location out of description if present
        location = self._extract_location_from_description(description)

        return {
            "source": "ashby",
            "url": canonical_url,
            "title": role or raw_title,
            "company": company,
            "location": location,
            "description": description,
        }

    @staticmethod
    def _split_title(raw_title: str) -> tuple[str, str]:
        # Expected: "Junior Data Engineer @ Teza Technologies"
        if " @ " in raw_title:
            role, company = raw_title.split(" @ ", 1)
            return role.strip(), company.strip()
        return raw_title.strip(), ""

    @staticmethod
    def _extract_location_from_description(description: str) -> str:
        # Very light heuristic for MVP:
        # looks for "Location\n<line>"
        marker = "Location\n"
        idx = description.find(marker)
        if idx == -1:
            return ""
        after = description[idx + len(marker):]
        # first non-empty line
        for line in after.splitlines():
            line = line.strip()
            if line:
                return line
        return ""
    
class WorkdayParser(BaseParser):
    def parse(self) -> Dict[str, Any]:
        if not self.html:
            raise ValueError("WorkdayParser requires injected HTML.")

        soup = BeautifulSoup(self.html, "html.parser")

        # Find ALL ld+json blocks (sometimes there are multiple)
        blocks = soup.find_all("script", attrs={"type": "application/ld+json"})
        if not blocks:
            raise ValueError("No JSON-LD (application/ld+json) found on page.")

        jobposting = None
        for b in blocks:
            raw = (b.string or "").strip()
            if not raw:
                continue

            # Sometimes JSON-LD can be an array; sometimes whitespace/newlines
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                # Some sites include multiple JSON objects; try a light cleanup
                raw2 = raw.replace("\n", " ").strip()
                data = json.loads(raw2)

            # Normalize if list
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") == "JobPosting":
                        jobposting = item
                        break
            elif isinstance(data, dict) and data.get("@type") == "JobPosting":
                jobposting = data

            if jobposting:
                break

        if not jobposting:
            raise ValueError("JSON-LD found, but no JobPosting object detected.")

        title = jobposting.get("title", "") or ""
        company = (jobposting.get("hiringOrganization", {}) or {}).get("name", "") or ""
        date_posted = jobposting.get("datePosted", "") or ""
        employment_type = jobposting.get("employmentType", "") or ""

        # Location (best-effort)
        job_loc = jobposting.get("jobLocation", {}) or {}
        addr = (job_loc.get("address", {}) or {})
        location = addr.get("addressLocality", "") or ""

        # Description is often HTML-escaped or contains tags
        desc = jobposting.get("description", "") or ""
        desc = html_lib.unescape(desc)
        desc = self._strip_tags(desc).strip()

        # Requisition / identifier
        identifier = jobposting.get("identifier", {}) or {}
        req_id = identifier.get("value", "") or ""

        return {
            "source": "workday",
            "url": self.url,
            "title": title,
            "company": company,
            "location": location,
            "description": desc,
            "date_posted": date_posted,
            "employment_type": employment_type,
            "req_id": req_id,
            "raw": jobposting,  # optional: keep for debugging
        }

    @staticmethod
    def _strip_tags(s: str) -> str:
        return re.sub(r"<[^>]+>", " ", s)
    
    
class GreenhouseParser(BaseParser):
    def parse(self) -> dict:
        if not self.html:
            raise ValueError("GreenhouseParser requires injected HTML.")
        soup = BeautifulSoup(self.html, "html.parser")

        # Canonical URL (better for dedupe)
        canonical = soup.find("link", attrs={"rel": "canonical"})
        url = (canonical.get("href") or "").strip() if canonical else self.url

        # Title
        h1 = soup.select_one("h1.section-header")
        title = h1.get_text(" ", strip=True) if h1 else ((soup.title.string or "").strip() if soup.title else "")

        # Location (your example: <div class="job__location"><div>Austin, TX</div></div>)
        loc_node = soup.select_one(".job__location div")
        location = loc_node.get_text(" ", strip=True) if loc_node else ""

        # Description
        desc_node = soup.select_one(".job__description")
        # keep as text for SkillFreq (you can also store raw_html if you want)
        description = _clean_text(str(desc_node)) if desc_node else _clean_text(_get_meta(soup, name="description"))

        # Company (best-effort)
        # 1) try logo alt e.g., "Apptronik Logo"
        logo = soup.select_one("img.logo")
        company = ""
        if logo and logo.get("alt"):
            company = logo["alt"].replace(" Logo", "").strip()

        # 2) fallback: slug from URL /<company>/jobs/...
        if not company:
            m = re.search(r"greenhouse\.io/([^/]+)/jobs", url)
            company = m.group(1) if m else ""

        return {
            "source": "greenhouse",
            "url": url,
            "title": title,
            "company": company,
            "location": location,
            "description": description,
        }
        
        
class SmartRecruitersParser(BaseParser):
    def parse(self) -> dict:
        if not self.html:
            raise ValueError("SmartRecruitersParser requires injected HTML.")
        soup = BeautifulSoup(self.html, "html.parser")

        # Canonical URL
        canonical = soup.find("link", attrs={"rel": "canonical"})
        url = (canonical.get("href") or "").strip() if canonical else self.url

        # Company often appears in the canonical path: /<Company>/<postingId>-...
        company = ""
        m = re.search(r"smartrecruiters\.com/([^/]+)/", url)
        if m:
            company = m.group(1).strip()

        # Title
        raw_title = (soup.title.string or "").strip() if soup.title else ""
        # Often: "Visa Staff Data Engineer | SmartRecruiters"
        title = raw_title.replace("| SmartRecruiters", "").strip()

        # Meta description (often truncated but still useful)
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = _clean_text(meta_desc.get("content") if meta_desc else "")

        # IDs (optional but great for dedupe)
        sr_job_ad_id = soup.find("meta", attrs={"name": "sr:job-ad-id"})
        job_ad_uuid = (sr_job_ad_id.get("content") or "").strip() if sr_job_ad_id else ""

        return {
            "source": "smartrecruiters",
            "url": url,
            "title": title,
            "company": company,
            "location": self._extract_location_from_head(title, soup),
            "description": description,
            "job_ad_uuid": job_ad_uuid,
        }

    @staticmethod
    def _extract_location_from_head(title: str, soup: BeautifulSoup) -> str:
        # sometimes keywords contain location: "Visa Staff Data Engineer Austin, TX, USA jobs careers"
        kw = soup.find("meta", attrs={"name": "keywords"})
        if kw and kw.get("content"):
            s = kw["content"]
            # crude but effective for MVP: look for "Austin, TX" pattern
            m = re.search(r"([A-Za-z .'-]+,\s*[A-Z]{2})(?:,|\s)", s)
            if m:
                return m.group(1).strip()
        return ""
    
class RipplingParser(BaseParser):
    def parse(self) -> dict:
        if not self.html:
            raise ValueError("RipplingParser requires injected HTML.")
        soup = BeautifulSoup(self.html, "html.parser")

        # 1) JSON-LD if present
        jp = _find_jobposting_jsonld(soup)
        if jp:
            title = jp.get("title", "")
            company = (jp.get("hiringOrganization", {}) or {}).get("name", "")
            location = ((jp.get("jobLocation", {}) or {}).get("address", {}) or {}).get("addressLocality", "")
            description = _clean_text(jp.get("description", ""))
            return {
                "source": "rippling",
                "url": _get_meta(soup, prop="og:url") or self.url,
                "title": title,
                "company": company,
                "location": location,
                "description": description,
            }

        # 2) Meta fallback
        url = _get_meta(soup, prop="og:url") or self.url
        title = _get_meta(soup, prop="og:title") or ((soup.title.string or "").strip() if soup.title else "")
        description = _clean_text(_get_meta(soup, name="description") or _get_meta(soup, prop="og:description"))

        # 3) Very light DOM fallback (some rippling pages have visible headings)
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(" ", strip=True) or title

        return {
            "source": "rippling",
            "url": url,
            "title": title,
            "company": "",
            "location": "",
            "description": description,
        }
        
class ICIMSParser(BaseParser):
    def parse(self) -> dict:
        if not self.html:
            raise ValueError("ICIMSParser requires injected HTML.")
        soup = BeautifulSoup(self.html, "html.parser")

        # 1) JSON-LD
        jp = _find_jobposting_jsonld(soup)
        if jp:
            title = jp.get("title", "")
            company = (jp.get("hiringOrganization", {}) or {}).get("name", "")
            location = ((jp.get("jobLocation", {}) or {}).get("address", {}) or {}).get("addressLocality", "")
            description = _clean_text(jp.get("description", ""))
            return {
                "source": "icims",
                "url": _get_meta(soup, prop="og:url") or self.url,
                "title": title,
                "company": company,
                "location": location,
                "description": description,
            }

        # 2) Meta fallback
        url = _get_meta(soup, prop="og:url") or self.url
        title = _get_meta(soup, prop="og:title") or ((soup.title.string or "").strip() if soup.title else "")
        description = _clean_text(_get_meta(soup, name="description") or _get_meta(soup, prop="og:description"))

        # 3) Light DOM fallback (iCIMS often has obvious content blocks)
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(" ", strip=True) or title

        # Try a couple common containers (won't hurt)
        main = soup.find("main") or soup.find(id="content") or soup.find(class_="iCIMS_JobContent")
        if main and len(main.get_text(strip=True)) > 200:
            description = _clean_text(main.get_text("\n", strip=True)) or description

        return {
            "source": "icims",
            "url": url,
            "title": title,
            "company": "",
            "location": "",
            "description": description,
        }
        
        