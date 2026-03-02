import argparse
from pathlib import Path
import truststore
truststore.inject_into_ssl()  # fixes SSL issues on some platforms (e.g. Mac M1) without requiring users to manually install certs


from .pipeline import run_links

import sys
print("DEBUG python:", sys.executable)

def main() -> None:
    parser = argparse.ArgumentParser(prog="skillfreq")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Run SkillFreq on a list of job links")
    run.add_argument("--input", required=True, help="Path to links.txt")
    run.add_argument("--skills", default="configs/skills.yml", help="Path to skills.yml")
    run.add_argument("--out", default="data/outputs/results.csv", help="CSV output path")
    run.add_argument("--min-score", type=float, default=0.0, help="Filter out jobs below score (0..1)")
    run.add_argument("--no-scrape", action="store_true", help="Treat input lines as raw text instead of URLs")
    run.add_argument("--profile", default="configs/profile.yml", help="Path to profile.yml")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    run_links(
        input_path=Path(args.input),
        skills_path=Path(args.skills),
        out_csv_path=out_path,
        min_score=args.min_score,
        no_scrape=args.no_scrape,
        profile_path=Path(args.profile)
    )


if __name__ == "__main__":
    main()