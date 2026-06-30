# Duplication Method

Transform any project folder into an LLM-friendly, workable folder — so an agent can scan it instantly and know what's missing, what to add, and how to build.

## Files

| File | Description |
|------|-------------|
| `DUPLICATION-METHOD.MD` | Full method spec — philosophy, folder skeleton, file conventions, scanning checklist |

## Quick Reference

A well-structured folder needs 4 file types:

1. **README.md** — Entry point, table of contents, one-liner per subfolder
2. **AGENTS.md** — Rules, constraints, anti-patterns, prerequisites
3. **template/** — [optional] Duplication seed (copy-paste base with runtime config)
4. **<variant>/README.md** — Full spec: stack, file tree, config, API endpoints, dummy data

If any of these files is missing, the folder is not LLM-ready.
