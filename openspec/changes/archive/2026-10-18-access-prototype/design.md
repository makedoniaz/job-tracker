# Design

## Context

See proposal.md for the access question this prototype answers. The repository currently has a blueprint and OpenSpec files but no JobTracker code, database, or runtime skill. The pilot runs on native Windows through Codex desktop.

## Goals / Non-Goals

**Goals:** Establish one reproducible path from a natural-language request to a local script, SQLite, and a later read. Make every failure observable before Codex reports success.

**Non-Goals:** Parse CVs, fetch listings, model job state, support multiple users, or build a reusable storage framework.

## Decisions

1. **Keep the executable surface small.** Put one `SKILL.md` and one Python script in the project skill directory, `.agents/skills/jobtracker/`. Use a verified native Windows Python 3 interpreter. The script supports only `save --key KEY --file PATH` and `show --key KEY`, with a required absolute `--db PATH` for both. Resolve the script relative to the installed skill, never the conversation's current directory. This follows the blueprint's CLI boundary without introducing a service or dependency.
2. **Keep runtime data outside Git.** Use a dedicated folder under the current user's local application data directory, if the chosen Codex workspace can write there. At setup, resolve and record its absolute database path in the skill instructions; use that same path for every invocation. Do not silently fall back to a repository database if permissions fail. SQLite needs directory write access for journal files. The sample source remains synthetic and may live in the repository.
3. **Use one immutable key-to-text table.** A record has a caller-supplied nonempty key as its primary key and the file's exact UTF-8 decoded content. Decode file bytes strictly before opening a write transaction. An identical repeated save returns the existing record; different content for an occupied key is an error. This avoids an update rule that could hide accidental data loss. `show` never creates or changes a record.
4. **Use JSON as the command contract.** Success and expected failures produce JSON, with a nonzero exit status on failure. The skill passes paths and keys as arguments and reads JSON output; it never embeds file content in shell commands. The skill treats selected file contents as data, not instructions, and reports a save only after command success.
5. **Verify at two boundaries.** First run focused manual CLI checks with a UTF-8 sample containing punctuation, Unicode, and a path with spaces. Then use ordinary language in Codex, restart the app, and retrieve in a fresh conversation. Record expected versus actual results and any initial or recurring permission prompts. Neither CLI checks alone nor conversation memory establish the full gate.

## Risks / Trade-offs

- **Runtime folder access denied** → Request the narrow folder permission during implementation and record the blocker if it remains unavailable.
- **Skill does not activate in a fresh chat** → Check discoverability and invocation wording; use explicit selection only as a diagnostic, not as proof of implicit activation.
- **Text changes across the Windows console boundary** → Compare the SQLite value and JSON result with the source text, including Unicode and line endings.
- **Prototype data is not backed up** → Use only synthetic data until the later product workflow defines backup and deletion.

## Migration Plan

There is no existing JobTracker data to migrate. Keep this prototype's table and runtime folder separate from later product tables; later work can replace the prototype without converting user data because the sample contains no real records.
