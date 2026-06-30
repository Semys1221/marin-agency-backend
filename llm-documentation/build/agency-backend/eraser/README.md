# Eraser Models — 7 Diagrams

**Workspace :** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ

> Source de vérité unique pour toute l'architecture. Chaque composant, step et API call doit exister comme node/edge dans ces diagrammes. Si ce n'est pas dans le graphe, ne le construis pas.

---

## Les 7 Diagrammes

| # | Diagramme | Eraser ID | Fichier local | Contenu |
|---|-----------|-----------|---------------|---------|
| 1 | **Overview** | `QAvELXBDa9-F2Xrw3efw` | — | Full funnel : Phase 1 (Outreach) + Phase 2 (Frontend), tech stack, webhooks, ticket system, duplication |
| 2 | **Outreach** | Voir ci-dessous | — | 9 sous-diagrammes du pipeline scraping → clean → campaign → benchmarks |
| 3 | **Frontend** | Voir ci-dessous | — | 10 sous-diagrammes du funnel Phase 2 (landing → CRM) |
| 4 | **Dashboard** | `26Oz8D4Inf_qZb08DmOp` + `E-X9VSDsMQMxTsY5gOEL` | — | Client dashboard + Dashboard API |
| 5 | **Hermes** | `Ul74DEaDluJUrRerLLv8` | — | Agent d'orchestration Hermes |
| 6 | **Duplication** | `zbm5twzQ2PegJ6Q0ix5j` | `frontend-engine/12-duplication.md` | Instance duplication form → Vercel deploy → Hermes activation |
| 7 | **Sequence** | `SMNBspX1OngIi0aY6-vu` + `YdBJjXEQW9a9CIV7Jsj1` | — | Sequence Creator + Sequence Creator Sidecar |

---

## Détail des sous-diagrammes

### Phase 1 — Outreach Engine (9 diagrams)

| Diagramme | ID | Node dans le Full Funnel |
|-----------|----|--------------------------|
| User Config | `nN0c_LscKTt8USVzd0cm` | User Account |
| Brain Gemini | `ad4Hnjehs8ahgoUtt5rR` | Generate Niches (Gemini) |
| Outscraper Scrape | `jlkUFWt6qk4_xLbffz-N` | Outscraper Scrape |
| Email Cleaning | `pJP9cb61sDXIxOHswPul` | Quick Clean, Handshake API, DB Bounce |
| Email Generator | `rr9ShOtTvKAgONN4y5LF` | Email Generator |
| Sequence Creator | `SMNBspX1OngIi0aY6-vu` | Sequence Creator |
| Instantly Campaign | `oY278MfOy8Z2ouhW14lY` | Campaign Setup, Push Leads |
| Benchmarks | `phlJMCbmAfsVzVIkgknK` | Analyze Performance, Kill & Replace, Scale |
| Sequence Creator Sidecar | `YdBJjXEQW9a9CIV7Jsj1` | Sequence Creator Server |

### Phase 2 — Frontend Engine (10 diagrams)

| Diagramme | ID | Node dans le Full Funnel |
|-----------|----|--------------------------|
| Landing Questionnaire | `PyoRd4vxu9VEKCf0V2XB` | Landing Page Questionnaire |
| SIRET Qualification | `hzN1XFgzPeuiuOWRsW2E` | SIRET Qualification |
| Calendly Booking | `lILdJ84u3oZNfkbKFquW` | Calendly Booked |
| Detective Agent | `RDJuOVOzmiHpWpPisVN4` | Scrape JSON Website, Lead Intelligence |
| Resend Emails | `PHEXZcauLV-1kcnFY5DR` | Transactional Emails (Resend) |
| Call Page / Live Form | `DbCzoKhJrHmMF4joGckm` | Call Page, Live Form Questionnaire |
| Post-Call Decision | `0XtaoappxmYqQ5naJfVJ` | Decision, Closed Won, Indecis, Not Interested |
| Stripe Payment | `7Udp0ZPwkqX6VbTMmSy4` | Stripe Payment |
| Dropbox Sign Contract | `MC4Q49k19ArM9fjDEDg6` | Dropbox Sign Contract |
| CRM Onboarding | `GU_uf1DbbhrXFG4xY5O7` | CRM Update, Onboarding in App |

### Dashboards (2 diagrams)

| Diagramme | ID | Node dans le Full Funnel |
|-----------|----|--------------------------|
| Client Dashboard | `26Oz8D4Inf_qZb08DmOp` | Client Dashboard HTML |
| Dashboard API | `E-X9VSDsMQMxTsY5gOEL` | Backend API → Dashboard |

### Cross-cutting (3 diagrams)

| Diagramme | ID | Node dans le Full Funnel |
|-----------|----|--------------------------|
| Hermes Agent | `Ul74DEaDluJUrRerLLv8` | Hermes Agent |
| Duplication | `zbm5twzQ2PegJ6Q0ix5j` | Duplication group |
| Ticket System | `HZaOZXAU0HuC0wL_PY33` | Ticket System group |
| Webhooks | `Lsn2Z2RN6-aC7kj-b0I3` | Webhooks group |
| Slack Notifications | `Kz--lAPp181lxLSJz8io` | Slack Notifications |
| Operations Dashboard | `OwPrSqrZ8EHvwcDbSvex` | Backend Dashboard |

---

## Convention

- Ces diagrammes sont la **source de vérité**. Avant d'écrire du code, toujours ouvrir le diagramme Eraser et vérifier que le composant existe comme node/edge.
- Les IDs Eraser sont volatiles (peuvent changer). Si un lien direct ne fonctionne plus, chercher dans le workspace principal.
- Pour mettre à jour un diagramme, utiliser l'éditeur Eraser ou demander à un LLM.
