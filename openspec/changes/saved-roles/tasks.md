# Tasks

Implement one numbered group per review cycle. Stop after each group, report focused manual-check results, and wait for user review before starting the next. Write no tests. If a group would add 300 or more lines of code or span dozens of files, split it before implementation.

## 1. Save and show unambiguous roles through the CLI

- [x] 1.1 Add sibling `roles.py` with a `jobs` table and JSON `save` command for company, title, optional HTTPS URL, and optional UTF-8 source file; verify a synthetic save returns a stable ID and exact source text is stored in the configured database.
- [x] 1.2 Add JSON `show --id` and atomic duplicate checks for URL and normalized company/title; verify direct show, identical resaves, conflicting URL, and a similar-role candidate response leave the expected row count and original content unchanged.
- [x] 1.3 Manually check blank fields, invalid URL, missing or invalid UTF-8 source, unknown ID, and prototype `record.py` save/show; verify failures are JSON with no partial role write, no application row is created, and prototype behavior still works. Stop for user review.

## 2. Find roles and resolve likely matches

- [x] 2.1 Add JSON `find` by URL or normalized company/title with candidate IDs and distinguishing details; verify zero, one, and multiple matches are returned without arbitrary selection.
- [x] 2.2 Add explicit distinct-posting save option that bypasses only company/title candidates; verify a confirmed distinct posting gets a new ID, an existing URL still cannot be duplicated, and ambiguous saves without the option do not write. Stop for user review.

## 3. Support ordinary-language role requests

- [x] 3.1 Extend `.agents/skills/jobtracker/SKILL.md` with role activation, documented `roles.py` commands, JSON outcomes, and candidate-resolution guidance while preserving prototype instructions; verify every documented command and path against the CLI.
- [x] 3.2 Manually ask Codex to save, repeat, find, and show a synthetic role in ordinary language, then trigger an ambiguous match and a failed save; verify it reports IDs and unchanged records accurately, seeks a decision before a distinct write, never claims a failed write, and creates no application. Stop for user review.
