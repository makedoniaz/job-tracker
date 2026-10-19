# Proposal

## Why

The access prototype proved local persistence, but its key-to-text records cannot represent or find job postings. The first product milestone needs saved roles with stable identities and duplicate checks, while keeping a saved role separate from an application.

## What Changes

- Add a JSON CLI to save a role with company, title, optional public URL, and optional UTF-8 source text, and to retrieve it by stable ID.
- Add role lookup by URL or company/title. Return likely matches before a write; repeated saves reuse the existing role, and ambiguous matches require an explicit choice before creating a distinct posting.
- Extend the JobTracker skill so ordinary-language requests use the role CLI and report only confirmed results.
- Implement in three review cycles: basic unambiguous save/show, lookup and ambiguity resolution, then conversational skill support. Stop after each cycle for review and focused manual checks.

## Capabilities

### New Capabilities

- `saved-roles`: Durable role records, stable-ID retrieval, duplicate-aware lookup and saving, and natural-language access.

### Modified Capabilities

None. The prototype's `local-record-access` behavior remains available.

## Impact

- A new role CLI and `jobs` table in the configured local SQLite database; the existing prototype table and commands remain usable.
- The existing `.agents/skills/jobtracker/SKILL.md` gains role commands and activation guidance.
- No new dependency, application record, URL fetching, listing extraction, or CV handling.
