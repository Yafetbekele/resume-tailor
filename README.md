# resume-tailor

Makes a one-page resume tailored to a job posting, built only from a profile of your own true facts.

- **With Claude:** Claude Code, running on your existing Claude plan with no API key, picks and rewords your bullets for the job. Every bullet it writes is checked against your profile. A bullet that adds a number, employer, title, date, award or technical term your profile doesn't have is thrown out and replaced.
- **Without Claude:** your pre-written bullets, coursework and skills are ranked by how well their tags match the posting. It's free and instant, and it's used whenever Claude can't be reached.
- **Layout:** a classic Times layout (bold headings, dash bullets) on exactly one page. Empty space is filled with more of your profile, the most relevant first. Long content is trimmed.

## Setup

```
pip install -r requirements.txt
```

1. Copy `examples/sample_profile.json` to `profile/career_profile.json`.
2. Fill it in with your own facts. The `profile/` folder is never uploaded.
3. To use Claude, install [Claude Code](https://claude.com/claude-code) and sign in. Otherwise pass `--no-ai`.

## Use

Paste the job posting into a text file, then run:

```
python make_resume.py posting.txt --title "Firmware Intern" --employer "Acme"
```

The resume goes to `tailored_resumes/<job>-<employer>/`, with the `plan.json` it was drawn from.

Options:
- `--keywords`: also work the posting's keywords into the skills line and bullets, even ones your profile doesn't back. These resumes go to `tailored_resumes_with_job_keywords/`, each with a `CHECK BEFORE SENDING.txt` listing every added keyword. Read it before you send.
- `--no-ai`: use the rules only, without Claude.
- `--again`: make it again even if one already exists for that job.
- `--profile`: use a profile somewhere else.
- `--out`: put the resume folders somewhere else.

From Python:

```python
import tailor
result = tailor.tailor_resume("job-1", "Firmware Intern", "Acme", posting_text, add_keywords=True)
print(result.path, result.method, result.added)
```

## The profile

See `examples/sample_profile.json` for the shape. Its main parts:
- `contact` and `education`, with coursework and honors.
- `sections`: entries with bullets and topic tags, used for ranking.
  - Mark an entry `trim_first` to cut it first when the page is full.
  - Use `never_claim` to list phrases Claude must never write about it.
- `skills`, with tags.

Settings by environment variable:
- `HSBOT_PROFILE`, `HSBOT_TAILORED_DIR`, `HSBOT_KEYWORD_DIR`: the profile path and the output folders.
- `HSBOT_CLAUDE`: the Claude Code program to run.

## Tests

The tests use a made-up student and a fake Claude, so they spend no usage:

```
python tests/tailor_test.py
```

This code comes from [handshake_intern_bot](https://github.com/Yafetbekele/handshake_intern_bot), where it tailors a resume for each internship application.
