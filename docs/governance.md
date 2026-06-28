# Governance — Quantum_Study_001

> Protected paths, approval escalation, and file ownership.

---

## Project Owner

**Brandt Pileggi** — final approval authority on all architectural decisions, scope changes, and phase transitions.

---

## Protected Files

None designated at project start. Update this section when any file is designated protected.

Convention: a file is "protected" if modifying it without review could silently break the system
(e.g., a base class contract, a security utility, env var schema, CI config).

---

## Approval Escalation

| Action | Required approval |
|--------|------------------|
| Phase transition (e.g., Exploration → Discovery) | Brandt explicit confirmation |
| Adding a new dependency | Brandt confirmation + decision-log entry |
| Changing vector store or structured store | Brandt confirmation + ADR |
| Modifying CLAUDE.md | Brandt confirmation |
| Any action listed as **Block** in CLAUDE.md §3 | Stop and ask — do not proceed |

---

## File Ownership Convention

Every task should declare its file scope at the start. If a file is being modified,
it belongs to exactly one active task. Concurrent edits to the same file require
explicit coordination.

---

*Last updated: 2026-06-28*
