# DUPLICATION-METHOD.MD

Turn any project folder into an LLM-friendly, workable folder — so an agent can scan it instantly and know what's missing, what to add, and how to build.

**This is NOT a standalone method.** It describes a pattern. Use it as a reference when you need to structure or audit any folder for AI-assisted development.

---

## 1. Philosophy

The goal is **discoverability in under 5 reads**. An agent should be able to open a folder and understand:

- What is this? (README.md)
- What are the rules? (AGENTS.md)
- What variants exist? (subfolder specs)
- How is it duplicated for each client? (template/)
- What exact files to generate? (variant README specs)

A well-structured folder needs exactly **4 file types** — no more, no less.

---

## 2. The Folder Skeleton

```
<module>/
├── README.md          # Entry point — table of contents, one-liner per subfolder
├── AGENTS.md          # Rules, constraints, anti-patterns, prerequisites
├── template/          # [optional] Duplication seed (copy-paste base)
│   ├── index.html
│   ├── config/client.js
│   └── vercel.json
└── <variant>/
│   └── README.md      # Full spec: stack, file tree, config, API, dummy data, rules
```

---

## 3. README.md — Entry Point

The root README must answer **"what's here?"** in under 10 seconds.

Format: a table with 3 columns: | Chemin | Description | Contient |

```
| Chemin | Description |
|--------|-------------|
| AGENTS.md | Design rules & constraints |
| backend-dashboard/README.md | Backend dashboard spec |
| template/ | Base template for duplication |
```

**Rule:** Each subfolder gets exactly one row. No essays. The detail lives in the subfolder's own README.

---

## 4. AGENTS.md — Rules of the Game

This is the **first file an agent should read**. It must cover:

1. **Prerequisites** — What must already exist before building (backend endpoints, env vars, auth model)
2. **Core Rules** — Design constraints (e.g. "no React, static HTML only", "no routing, single page")
3. **Anti-patterns** — What NOT to do (e.g. "this is not the funnel", "do not add business logic")
4. **Duplication Model** — How instances are created (copy template vs. separate deploy)

**Tone:** Direct, prescriptive. No explanations, just rules.

---

## 5. template/ — Duplication Seed

Only needed when the module follows a **multi-instance** model (one per client).

Structure:

```
template/
├── index.html           # Self-contained page, loads config at runtime
├── config/client.js     # Global `var ClientConfig` — edited per client
└── vercel.json          # Cache-override for config files
```

**Rules:**
- Config is loaded at **runtime** via `<script>`, not built in. No build step per instance.
- `vercel.json` must prevent caching of `/config/(.*)`.
- The template is copied: `cp -r template clients/nouveau-client`, then `config/client.js` is edited.

---

## 6. Variant Spec Convention (subfolder/README.md)

Each variant gets its own `README.md` with **all the information an agent needs to generate it from scratch**.

```
# <Variant Name>

## Stack
Framework, libraries, CDN links, build tool.

## File Tree to Generate
Exact tree listing every required file.

## Config Interface
Typed config object (TypeScript interface or JS shape), with all fields.

## API Endpoints Consumed
Full list: method, path, purpose, dummy data for each.

## Dummy Data
Every endpoint needs a mock response example. Agents cannot call real APIs.

## Deployment
How to deploy (vercel, render, etc.), env vars needed.

## Rules (Variant-Specific)
What makes this variant different from others.
```

**Critical:** If you omit `Dummy Data`, the agent will either hallucinate API responses or waste time asking you. Dummy data is **mandatory**.

---

## 7. Scanning Checklist

When an agent needs to assess a folder:

1. **Read `AGENTS.md`** — Know the rules first.
2. **Read `README.md`** — Map the folder layout.
3. **Read each variant's `README.md`** — Understand what needs to be built.
4. **If `template/` exists, read its `README.md`** — Understand the duplication mechanism.
5. **Check for dummy data** — If missing, flag it. The spec is incomplete.

If any of these files is missing, the folder is **not LLM-ready**. The first task is to create the missing file.

---

## 8. How to Apply This to Any Folder

When tasked with restructuring a folder or preparing it for AI work:

1. Create `AGENTS.md` with the rules of the domain.
2. Create `README.md` with a table of contents.
3. For each subfolder containing a distinct module/variant, give it a `README.md` with the full spec.
4. If the module is duplicated per client, add a `template/` directory.
5. Verify every variant spec includes dummy data.

**That's it.** Four file types, one pattern, instant clarity.
