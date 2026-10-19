# saved-roles Specification

## Purpose

Lets a single user preserve job postings as identifiable local records, find them later, and resolve likely duplicates without implying that an application was submitted.

## Requirements

### Requirement: Save a role independently of applications
The system SHALL save a role with a nonempty company and title, optional URL and optional UTF-8 source text, and return a stable role ID only after the write succeeds. Saving a role SHALL NOT create an application.

#### Scenario: Save an unambiguous role
- **WHEN** the user saves a role with a company and title and no existing role is a likely match
- **THEN** a durable role is created, its stable ID is returned, and no application is created

#### Scenario: Preserve selected source text
- **WHEN** a role is saved with readable UTF-8 source text selected by the user
- **THEN** the stored role retains that text exactly for later retrieval

#### Scenario: Invalid role input
- **WHEN** company or title is blank, or selected source text cannot be read as UTF-8
- **THEN** the command reports failure and makes no role write

### Requirement: Prevent accidental duplicate roles
The system SHALL check for likely existing roles by URL and normalized company/title before creating a role. It SHALL return candidate IDs without silently merging different postings or creating another role when identity is uncertain.

#### Scenario: Repeat a save with the same URL
- **WHEN** the user repeats a save with the same URL and role details
- **THEN** the existing ID is returned without creating or replacing a role

#### Scenario: Repeat a save without a URL
- **WHEN** the user repeats the same company, title, and source text without a URL and exactly one existing role has those details
- **THEN** the existing ID is returned without creating another role

#### Scenario: Similar title and company
- **WHEN** a new save has a normalized company/title match whose identity is not certain
- **THEN** the matching role IDs are returned for resolution and no role is created

#### Scenario: Confirm a separate posting
- **WHEN** the user explicitly identifies a candidate as a distinct posting and no saved role has the same URL
- **THEN** the system permits creating a new role with a different stable ID

#### Scenario: Repeated URL with conflicting details
- **WHEN** a save uses an existing role's URL but supplies different role details
- **THEN** the system returns the existing candidate for resolution without replacing it or creating a duplicate

### Requirement: Retrieve and find saved roles
The system SHALL retrieve a role by stable ID and SHALL find candidate roles by URL or company/title. It SHALL expose enough stored details to let the user distinguish multiple matches.

#### Scenario: Retrieve by ID
- **WHEN** an existing role ID is requested
- **THEN** the stored company, title, URL, and source text are returned for that ID

#### Scenario: Find by role details
- **WHEN** a URL or company/title is searched
- **THEN** all matching candidates and their stable IDs are returned without selecting one arbitrarily

#### Scenario: Unknown role
- **WHEN** an unknown role ID is requested
- **THEN** the system reports that no such role exists

### Requirement: Support ordinary-language role requests
The JobTracker skill SHALL direct Codex to use the configured local role commands for save and lookup requests, seek user resolution for uncertain matches, and report writes only after successful command results.

#### Scenario: Save a role in conversation
- **WHEN** the user asks in ordinary language to save a role
- **THEN** Codex invokes the role command and reports the confirmed role ID or candidate IDs

#### Scenario: Ambiguous role in conversation
- **WHEN** a command returns multiple plausible roles or requires a separate-posting decision
- **THEN** Codex presents the candidates and obtains the user's choice before any distinct-role write

#### Scenario: Command failure in conversation
- **WHEN** a role command fails
- **THEN** Codex reports the failure without claiming that a role was saved
