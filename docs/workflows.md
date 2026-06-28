# Workflows — Quantum_Study_001

> Dev lifecycle, branching, commit standards, PR process.

---

## Branching

| Branch | Purpose |
|--------|---------|
| `main` | Stable, phase-complete work only |
| `phase/<n>-<name>` | Active phase work (e.g., `phase/0-exploration`) |

Phase branches merge to `main` when the phase's Definition of Done is fully satisfied and Brandt signs off.

---

## Commit Standards

- Message explains *why*, not just *what*
- No secrets, credentials, or API keys in any commit
- No `print()` debugging left in `src/`
- All Definition of Done boxes checked before committing phase work

## Wiki Sync

Update `wiki/` in the repo first, then sync to GitHub wiki:
```bash
git clone https://github.com/BraPil/Quantum_study_001.wiki.git /tmp/wiki_sync
cp wiki/*.md /tmp/wiki_sync/
cd /tmp/wiki_sync && git add . && git commit -m "Sync wiki from repo" && git push
```

---

*Last updated: 2026-06-28*
