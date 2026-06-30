# Client Dashboard — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=26Oz8D4Inf_qZb08DmOp

## Purpose
Static HTML dashboard served as the client's CRM endpoint. No Shadcn, no React — simple HTML. Links to external services + fetches backend API data.

## Database Tables
Read-only on all tables: clients, call_sessions, clean_leads, campaign_settings, campaign_analytics, email_tracking, funnel_progress, onboarding_tasks.

## Env Vars
None (HTML fetches from API endpoints described below).

## External Links (Redirects)
| Service | URL |
|---------|-----|
| Microsoft | `https://office.com` |
| Quo | `https://quo.com` |
| Looker Studio | `https://lookerstudio.google.com` |
| Calendly | `https://calendly.com/{client}` |
| Stripe | `https://dashboard.stripe.com` |
| Shopify * | `https://{client}.myshopify.com/admin` |

\* E-commerce only.

## API Endpoint
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/dashboard?tenant_id=X` | Aggregated dashboard data (leads, campaigns, keys, renewals, sequences, scripts, prospects, funnel, reports, services) |
| POST | `/api/leads/status` | Update lead status (no-show, indecis, closed) |
| POST | `/api/campaigns/stop` | Stop campaign |

## Features
- Lead status update: no-show / indecis / closed ("double tap")
- Campaign stop button (when reply < 2%)
- Niche exhausted → "needs scraping" alert
- New client → quota + 90-day objective
- Lead intelligence sheet for call prep
- Gmail sending to CRM prospect (open rate)
- **Trigger Call Description email** (per diagram edge `Client Dashboard HTML > Call Description: post-call summary`): after call, agent clicks to send post-call summary — triggers Resend email type #9

## Edge Cases
- API unavailable → render `<p class="error">Service indisponible</p>`, never crash
- Empty data → empty state, not error
- Iframe blocked by CSP → open in new tab instead
- Demo mode: serve from local dummy JSON files
