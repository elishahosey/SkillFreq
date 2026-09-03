import tempfile
import unittest
from pathlib import Path

from skillfreq.skills.job_market import (
    extract_job_rows,
    extract_market_skills,
    load_market_taxonomy,
)


class JobMarketSkillsTest(unittest.TestCase):
    def test_aliases_normalize_to_one_canonical_skill(self):
        taxonomy = {"PostgreSQL": ["postgresql", "postgres"]}

        matches = extract_market_skills(
            "Built PostgreSQL pipelines; migrated an older Postgres service.", taxonomy
        )

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].canonical_skill, "PostgreSQL")
        self.assertEqual(matches[0].mention_count, 2)
        self.assertEqual(matches[0].matched_terms, ("postgresql", "postgres"))

    def test_boundaries_avoid_substring_false_positives(self):
        matches = extract_market_skills("Used MySQL, not NoSQL.", {"SQL": ["sql"]})
        self.assertEqual(matches, [])

    def test_job_rows_have_one_row_per_job_and_skill(self):
        jobs = [{
            "source_site": "indeed",
            "source_job_id": "123",
            "job_url": "https://example.test/123",
            "description": "SQL and SQL plus Python",
        }]

        rows = extract_job_rows(jobs, {"SQL": ["sql"], "Python": ["python"]})

        self.assertEqual(len(rows), 2)
        self.assertEqual({row[4] for row in rows}, {"SQL", "Python"})
        self.assertEqual(next(row[6] for row in rows if row[4] == "SQL"), 2)

    def test_taxonomy_rejects_alias_assigned_to_two_skills(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "skills.yml"
            path.write_text("One:\n  - shared\nTwo:\n  - shared\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "assigned to both"):
                load_market_taxonomy(path)


if __name__ == "__main__":
    unittest.main()
