import argparse
import csv
from datetime import datetime
from pathlib import Path
from .pipeline import run_links,fetch_links,create_file,extract_links
from .skills.jds.extract import process_all_jobs
from .skills.extract import extract_jd_skills
from collections import Counter
from .resume_router import route_resumes_for_csv
try:
    import truststore
    truststore.inject_into_ssl()  # optional SSL fix for some platforms
except ImportError:
    truststore = None

import sys
print("DEBUG python:", sys.executable)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
skills_filename = f"extracted_skills_{timestamp}.txt"

def count_titles(csv_path: Path, title_col: str = "title") -> None:
    counts: Counter[str] = Counter()

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"{csv_path} does not appear to have a header row")
        if title_col not in reader.fieldnames:
            available = ", ".join(reader.fieldnames)
            raise ValueError(f"Column '{title_col}' not found. Available columns: {available}")

        for row in reader:
            title = " ".join((row.get(title_col) or "").split())
            if title:
                counts[title] += 1

    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["title", "count"])
    for title, count in counts.most_common():
        writer.writerow([title, count])

def main() -> None:
    parser = argparse.ArgumentParser(prog="skillfreq")
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    resume_suggest = sub.add_parser("suggest", help="Used to compare skills from JD vs resume/profile yaml")
    resume_suggest.add_argument("--jds", required=True,help="Enter the folder of JDs")
    resume_suggest.add_argument("--out", default="data/outputs/suggestions.csv", help="CSV output path for suggestions")

    route = sub.add_parser("route", help="Recommend the best resume variant for each JD row in a CSV")
    route.add_argument("--input", required=True, help="Path to input CSV with title/JD columns")
    route.add_argument("--out", default="data/outputs/routed_jobs.csv", help="CSV output path with resume routing columns")
    route.add_argument("--roles", default="configs/roles.yml", help="Path to roles.yml")
    route.add_argument("--title-col", default="", help="Title column name in the CSV (optional)")
    route.add_argument("--jd-col", default="description", help="JD text column name in the CSV")

    titles = sub.add_parser("titles", aliases=["count-titles"], help="Count job titles in a CSV")
    titles.add_argument("filename", help="Path to the CSV file")
    titles.add_argument("--title-col", default="title", help="Title column name in the CSV")

    extract_skills = sub.add_parser("extract", help="Used to extract skills from resume and update your profile yaml")
    extract_skills.add_argument("--file", required=True,help="Enter the filename of the resume, including the file extension")

    fetch = sub.add_parser("fetch", help="Fetch and process job links and append to links.txt")
    fetch.add_argument("--input", required=True, help="Path to input CSV with job links (e.g. from joblist.py)")
    fetch.add_argument("--output", default="links.txt", help="Path to output links.txt")
    
    run = sub.add_parser("run", help="Run SkillFreq on a list of job links")
    run.add_argument("--input", required=True, help="Path to links.txt")
    run.add_argument("--skills", default="configs/skills.yml", help="Path to skills.yml")
    run.add_argument("--weights", default="configs/weights.yml", help="Path to weights.yml")
    run.add_argument("--out", default="data/outputs/results.csv", help="CSV output path")
    run.add_argument("--min-score", type=float, default=0.0, help="Filter out jobs below score (0..1)")
    run.add_argument("--no-scrape", action="store_true", help="Treat input lines as raw text instead of URLs")
    run.add_argument("--profile", default="configs/profile.yml", help="Path to profile.yml")
    args = parser.parse_args()

    extract_skills.set_defaults(command="extract")
    fetch.set_defaults(command="fetch")
    run.set_defaults(command="run")
    resume_suggest.set_defaults(command="suggest")
    route.set_defaults(command="route")
    titles.set_defaults(command="titles")
    
    if args.cmd == "fetch":
        fetch_links(
            input_path=Path(args.input),
            output_path=Path(args.output)
        )

    elif args.cmd == "run":
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        jdParsedObject = run_links(
                        input_path=Path(args.input),
                        skills_path=Path(args.skills),
                        weight_path=Path(args.weights),
                        out_csv_path=out_path,
                        min_score=args.min_score,
                        no_scrape=args.no_scrape,
                        profile_path=Path(args.profile)
                    )
        
        #TODO:extract skills with NLP and add to yaml of skills; uncomment below when ready to extract skills from job descriptions and save to file for future analysis
        extracted_skills = extract_jd_skills(jdParsedObject)
        #flatten before creating file
        flatten_skills = [item for sublist in extracted_skills for item in sublist]
        
        counts_skills = Counter(flatten_skills)
        output = "\n".join(f"{skill},{count}" for skill, count in counts_skills.most_common())
        create_file(skills_filename, output)
    
    elif args.cmd == "extract":
        extract_links(
            file_path=args.file
        )
    elif args.cmd == "suggest":
        process_all_jobs(
            jd_folder= Path(args.jds), 
            skills_path= Path("configs/skills.yml")
         )
    elif args.cmd == "route":
        routed_df = route_resumes_for_csv(
            input_csv=Path(args.input),
            out_csv=Path(args.out),
            roles_path=Path(args.roles),
            title_col=args.title_col,
            jd_col=args.jd_col,
        )
        print(f"Wrote {len(routed_df)} routed rows to {args.out}")
    elif args.cmd in {"titles", "count-titles"}:
        count_titles(
            csv_path=Path(args.filename),
            title_col=args.title_col,
        )
        
        
if __name__ == "__main__":
    main()
