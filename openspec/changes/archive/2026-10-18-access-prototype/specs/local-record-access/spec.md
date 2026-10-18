# Spec Delta

## Purpose

Lets a local Codex conversation save and retrieve a small text record reliably, proving the execution and persistence path needed for later JobTracker features.

## ADDED Requirements

### Requirement: Save selected text
The system SHALL save the exact UTF-8 content of a user-selected local text file under a stable record key and return a JSON result only after the content is durable.

#### Scenario: Save text with Unicode and spaces in its path
- **WHEN** the user selects a readable UTF-8 file whose path contains spaces and whose text contains punctuation and Unicode
- **THEN** the saved record contains that text exactly and the operation returns its key in JSON

#### Scenario: Repeat the same save
- **WHEN** the same key and identical file content are saved again
- **THEN** the existing record is returned and no second record is created

#### Scenario: Existing key has different content
- **WHEN** a save uses an existing key with different file content
- **THEN** the operation fails without replacing the existing content

### Requirement: Retrieve durable records
The system SHALL retrieve a saved record by key from local persistent storage and return its exact content in JSON.

#### Scenario: Retrieve from a fresh conversation
- **WHEN** the app has restarted and a new Codex conversation requests a previously saved key
- **THEN** the returned content matches the saved file without relying on prior conversation context

#### Scenario: Unknown key
- **WHEN** retrieval requests a key that has not been saved
- **THEN** the operation returns a clear failure rather than invented content

### Requirement: Reject invalid saves safely
The system SHALL report invalid or unreadable input as a failed operation and SHALL leave persistent records unchanged.

#### Scenario: Missing source file
- **WHEN** a save names a missing source file
- **THEN** the operation reports failure and creates no record

#### Scenario: Invalid text encoding
- **WHEN** a save selects a file that is not valid UTF-8
- **THEN** the operation reports failure and creates no record

### Requirement: Use the configured local data folder
The system SHALL keep its database in the selected dedicated data folder outside Git and SHALL use that same location for save and retrieve operations.

#### Scenario: Separate working directories
- **WHEN** save and retrieve are invoked from different working directories
- **THEN** both access the same database at the configured absolute path

### Requirement: Support natural-language operation
The JobTracker skill SHALL let Codex interpret ordinary save and retrieve requests, invoke the local commands, and report a write as successful only after a successful command result.

#### Scenario: Save without user commands
- **WHEN** the user asks in natural language to save the selected text file
- **THEN** Codex invokes the local save operation without requiring the user to type a command

#### Scenario: Command failure in chat
- **WHEN** the local command returns a failure
- **THEN** Codex reports that failure and does not claim the record was saved
