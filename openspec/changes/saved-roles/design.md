# Design

## Context

See proposal.md for motivation and specs/saved-roles/spec.md for behavior. The pilot has a small JSON `record.py` CLI, a JobTracker skill with a verified Windows interpreter and absolute database path, and a `records` table containing only synthetic prototype data. There is no role model or application table. The blueprint requires local SQLite storage, command-level validation, and one reviewable capability per cycle.

## Goals / Non-Goals

**Goals:** Make role identity and duplicate decisions explicit, preserve optional supplied source text, and keep the prototype commands working during this milestone.

**Non-Goals:** Fetch URLs, parse requirements, create applications, edit or delete saved roles, or migrate the prototype text record into a job.

## Decisions

1. **Add a sibling role CLI and `jobs` table in the configured database.** Use `roles.py` beside `record.py`, with `save`, `show`, and later `find` commands. Keep the prototype command and `records` table untouched. A row has an integer stable ID, company, title, optional URL, and source text. This is smaller and safer than converting the prototype's arbitrary key-to-text records or building a generic CLI framework.
2. **Treat role source text as selected input.** `save` accepts an optional absolute UTF-8 text-file path, reads it before the transaction, and stores its decoded content exactly. No URL fetch happens here. Passing text through a file follows the existing prototype pattern and avoids embedding listing content in shell arguments.
3. **Check identity and insert within one write transaction.** Require nonblank company/title and a syntactically valid HTTPS URL with a hostname when one is supplied. Compare URLs conservatively after trimming surrounding whitespace; compare company/title after case folding and collapsing whitespace. Identical URL and details, or a sole identical no-URL record, returns the existing ID unchanged. A conflicting URL match or uncertain company/title match returns candidate IDs without a write. A unique URL constraint backs up the URL check. This favors visible ambiguity over aggressive URL rewriting or silent merging.
4. **Resolve distinct postings explicitly.** The second cycle adds `find` by exact URL or normalized company/title and an explicit `--new-posting` save option. It bypasses company/title candidates only after the user chooses a separate posting; it never bypasses an existing URL. Choosing an existing candidate needs no write: use its ID. The skill must ask for the user's decision and never infer `--new-posting` from similar text alone. The CLI cannot prove conversational intent, so its output makes the decision observable.
5. **Keep a small JSON contract.** Return an outcome (`created`, `existing`, or `candidates`) and relevant IDs on successful save attempts; `candidates` means no write. `show` returns the full role; `find` returns matching candidate summaries. Invalid input, unreadable source, and missing IDs use nonzero exit and JSON error output. Read operations use SQLite read-only mode, and writes use the verified absolute database path and an atomic transaction.

## Risks / Trade-offs

- Similar postings at one company may share a title. Returning candidates and requiring `--new-posting` prevents accidental merging but adds a user decision.
- URL variants with different query strings can represent the same posting. Conservative URL comparison plus company/title candidates avoids false automatic merges; later URL retrieval can improve normalization if real examples justify it.
- The prototype database contains synthetic records. A new `jobs` table leaves them intact, while real role content introduces a backup obligation before routine use.
- Source text and search results may contain untrusted listing instructions. The skill treats them as data and passes structured arguments to the CLI.

## Migration Plan

Create `jobs` on the first role write in the configured SQLite database. Existing `record.py` reads and writes continue against `records`; no data conversion is needed. Rollback of the feature can leave the new table dormant without affecting prototype records. Do not drop user-created role rows as part of rollback.
