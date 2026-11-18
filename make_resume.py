#!/usr/bin/env python3
"""Make a one-page resume tailored to one job posting.

    python make_resume.py posting.txt --title "Firmware Intern" --employer "Acme"

The posting is a text file with the job description pasted in. The resume is
built only from the facts in your profile (profile/career_profile.json, or
--profile). Add --keywords to work the posting's own keywords in too; those
resumes come with a "CHECK BEFORE SENDING.txt" listing every keyword your
profile doesn't back.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import tailor


def main() -> int:
    parser = argparse.ArgumentParser(description="Make a one-page resume tailored to one job posting.")
    parser.add_argument("posting", help="text file holding the job posting")
    parser.add_argument("--title", required=True, help="the job title")
    parser.add_argument("--employer", required=True, help="the company")
    parser.add_argument("--profile", default=str(tailor.PROFILE_PATH), help="your profile JSON")
    parser.add_argument("--out", help="folder to put the resume folders in")
    parser.add_argument("--keywords", action="store_true", help="work the posting's keywords in (check before sending)")
    parser.add_argument("--no-ai", action="store_true", help="use the rules only, without Claude")
    parser.add_argument("--again", action="store_true", help="make it again even if one exists")
    args = parser.parse_args()

    profile = Path(args.profile)
    if not profile.exists():
        print(f"No profile at {profile}. Copy examples/sample_profile.json there and fill in your own facts.")
        return 1
    job_text = Path(args.posting).read_text(encoding="utf-8")
    job_id = re.sub(r"[^a-z0-9]+", "-", args.title.lower()).strip("-")[:40] or "job"
    result = tailor.tailor_resume(
        job_id, args.title, args.employer, job_text,
        use_ai=not args.no_ai, profile_path=profile, out_dir=args.out,
        reuse=not args.again, add_keywords=args.keywords,
    )
    print(f"Resume: {result.path}")
    print(f"Made with: {result.method}")
    for note in result.notes:
        print(f"  - {note}")
    if result.added:
        print("Check these before sending: " + ", ".join(result.added))
    return 0


if __name__ == "__main__":
    sys.exit(main())
