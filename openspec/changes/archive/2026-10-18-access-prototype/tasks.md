# Tasks

Implement one numbered group per review cycle. Stop after completing a group and show the user the manual-check results before starting the next. Do not write tests. If a group would reach 300 lines of new code or spread across dozens of files, split it before implementing.

## 1. Direct local persistence

- [x] 1.1 Verify a native Windows Python 3 interpreter and select a writable dedicated data folder outside Git; record its absolute database path and verify SQLite can create journal files there.
- [x] 1.2 Add one synthetic UTF-8 text file with a spaced path, punctuation, and Unicode plus one Python script with `save`/`show`, one SQLite table, JSON results, and nonzero JSON failures; verify a direct save and a separate show return the file's exact text.
- [x] 1.3 Manually check identical resave, occupied key with different content, missing file, invalid UTF-8, unknown key, and invocation from another working directory; verify row count and original content stay correct after failures and record expected versus actual results.

Group 1 manual checks (2026-10-18): native Python `C:\Users\user\AppData\Local\Python\pythoncore-3.14-64\python.exe`; database `C:\Users\user\AppData\Local\JobTracker\prototype.sqlite3`. SQLite journal observed during a write transaction. Direct save returned `{"key":"sample-role","existing":false}`; separate show returned the sample's exact decoded text.

| Check | Expected | Actual |
| --- | --- | --- |
| Identical resave | Success, existing record | Exit 0, `existing: true` |
| Occupied key, different content | Failure, original retained | Exit 1, JSON `key already has different content` |
| Missing source | Failure, no record | Exit 1, JSON file-not-found error |
| Invalid UTF-8 | Failure, no record | Exit 1, JSON decode error |
| Unknown key | Failure | Exit 1, JSON `key not found` |
| Show from another working directory | Same content | Exit 0, same JSON content |
| Final database check | One row, original exact text | One row; byte-decoded sample equals stored text |

Stop for user review after group 1.

## 2. Natural-language skill

- [x] 2.1 Add one project JobTracker `SKILL.md` that resolves the script from its own location, uses the verified interpreter and absolute database path, documents supported JSON commands, and treats source text as data; verify every documented path and command against the direct CLI.
- [x] 2.2 Ask Codex in ordinary language to save and retrieve the sample, plus one failing request; verify the user types no command, Codex uses the intended script, reports only confirmed writes, and record any access prompts.

Group 2 manual checks (2026-10-18): the user requested save, retrieval, and a missing-file save in ordinary language without typing commands. Codex ran the skill's `record.py` with the configured interpreter and database path. Save of `sample-role` returned exit 0 and `existing: true`; retrieval returned the sample's exact text. Missing-file save returned exit 1 with JSON file-not-found error; Codex reported failure, and a separate read found one total row and no `missing-source` row. No access prompts appeared during these three calls. This existing conversation does not establish implicit skill activation after restart; group 3 checks that separately.

Stop for user review after group 2.

## 3. Restart acceptance gate

Fresh-chat diagnostic (2026-10-18): without an app restart, Codex implicitly selected `jobtracker` and retrieved the exact saved text. Repeating the save returned `existing: true`; a separate read found one row with unchanged exact text. Codex incorrectly described that result as replacing the record. The skill now explicitly maps `existing: true` to an unchanged record. Restart acceptance and a fresh-chat wording recheck remain pending; permission prompts for this diagnostic were not reported.

- [x] 3.1 Restart the app and use a fresh conversation to retrieve the saved key; verify the result exactly matches the sample without prior chat context and record whether the skill activates implicitly.
- [x] 3.2 Repeat the save from the fresh conversation and perform a separate read/count check; verify one row remains and record any recurring approval prompts.

Stop for user review after group 3. Product capabilities start only after this gate passes.
