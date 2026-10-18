# Proposal

## Why

The blueprint requires proof that a local Codex conversation can invoke a script and persist data across conversations before product features are built. That execution and permission path has not yet been demonstrated.

## What Changes

- Add a minimal local record flow: save a selected UTF-8 file under a stable key and retrieve its exact content from SQLite.
- Expose the flow through one discoverable JobTracker skill and one Python script, with JSON results and clear failures.
- Verify natural-language use, idempotence, fresh-conversation persistence, and the intended runtime permissions with synthetic data.

## Capabilities

### New Capabilities

- `local-record-access`: Save and retrieve a local text record reliably through Codex, with observable error handling and persistent storage.

### Modified Capabilities

None.

## Impact

Adds one skill, one Python script, one SQLite table in a dedicated data folder outside Git, and one synthetic text fixture. No job, application, CV, or matching behavior is included. No additional dependency or user interface is planned.
