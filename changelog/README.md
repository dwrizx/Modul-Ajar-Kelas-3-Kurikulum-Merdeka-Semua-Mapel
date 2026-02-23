# Changelog Guide

## Purpose
Changelog documents user/dev-impacting changes so future work has clear context.

## When Changelog Is Required
Create a changelog entry for:
- feature additions
- behavior/alur changes
- API/CLI output/flag changes
- config/env changes impacting usage
- permission/auth/security changes
- UX/UI flow changes
- performance changes visible to users

If change is non-functional only (pure refactor/chore), note the reason if no changelog is created.

## File Naming
Use:

`changelog/YYYY-MM-DD-<short-topic>.md`

Example:

`changelog/2026-02-23-kelas-1-batch-download.md`

## Minimum Content
Each entry must include:
- what changed
- why it changed
- impact/risk
- testing evidence (automated or manual steps)

## Template
Copy from:

`changelog/_template.md`
