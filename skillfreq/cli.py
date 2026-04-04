import argparse
from datetime import datetime
from pathlib import Path
from .pipeline import run_links,fetch_links,create_file,extract_links
from .skills.jds.extract import process_all_jobs
from .skills.extract import extract_jd_skills
import truststore
from collections import Counter

truststore.inject_into_ssl()  # fixes SSL issues on some platforms (e.g. Mac M1) without requiring users to manually install certs


import sys
print("DEBUG python:", sys.executable)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
skills_filename = f"extracted_skills_{timestamp}.txt"

def main() -> None:
    parser = argparse.ArgumentParser(prog="skillfreq")
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    resume_suggest = sub.add_parser("suggest", help="Used to compare skills from JD vs resume/profile yaml")
    resume_suggest.add_argument("--jds", required=True,help="Enter the folder of JDs")
    resume_suggest.add_argument("--out", default="data/outputs/suggestions.csv", help="CSV output path for suggestions")

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
        
        
if __name__ == "__main__":
    main()