# Comptes & Services utilisés dans le projet

> Généré depuis `.env.local`

## Infrastructure & Hébergement

| Service | Rôle | Variables concernées |
|---------|------|----------------------|
| Supabase | Base de données, auth, stockage | `SUPABASE_URL`, `SUPABASE_EMAIL`, `SUPABASE_PASSWORD`, `SUPABASE_PUBLISHABLE`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY`, `DATABASE_URL` |
| Render | Déploiement backend | `RENDER_API_KEY` |
| Vercel | Déploiement frontend | `VERCEL_TOKEN`, `VERCEL_TEAM_ID` |
| Engine / Outreach Engine | API moteur outreach | `ENGINE_URL` |
| GitHub | Hébergement code | `GIT_REPO_URL` |

## Outreach Engine (Phase 1)

| Service | Rôle | Variables concernées |
|---------|------|----------------------|
| Outscraper | Scraping de leads | `OUTSCRAPER_API_KEY` |
| Google Gemini | LLM pour génération de contenu | `HERMES_API_KEY` |
| Handshake | Intégration partnership | `HANDSHAKE_API_KEY` |
| DBBounce | Service B2B | `DBBOUNCE_API_KEY` |
| Instantly | Cold email + campagnes | `INSTANTLY_API_KEY`, `INSTANTLY_DEFAULT_CAMPAIGN_ID` |
| Sequence Creator | Création de séquences emails | `SEQUENCE_CREATOR_API_KEY` |
| Slack | Notifications, bot, approbations | `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_CHANNEL_ID`, `SLACK_APPROVAL_CHANNEL_ID` |

## Frontend Engine (Phase 2)

| Service | Rôle | Variables concernées |
|---------|------|----------------------|
| Stripe | Paiements | `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET` |
| Calendly | Prise de rendez-vous | `CALENDLY_URL`, `CALENDLY_CLIENT_ID`, `CALENDLY_CLIENT_SECRET`, `CALENDLY_WEBHOOK_KEY` |
| Dropbox Sign | Signature électronique devis | `DROPBOX_SIGN_API_KEY` |
| Resend | Envoi d'emails transactionnels | `RESEND_API_KEY`, `RESEND_FROM_EMAIL` |
| Sentry | Monitoring / erreurs | `SENTRY_DSN` |
| Shopify | E-commerce | `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET`, `SHOPIFY_ADMIN_TOKEN_TEMPLATE` |
| Ticket system | Support client | `TICKET_SYSTEM_API_KEY` |

## Client-facing

| Service | Rôle | Variables concernées |
|---------|------|----------------------|
| Shopify Storefront (client) | Boutique e-commerce publik | `VITE_SHOPIFY_STOREFRONT_TOKEN`, `VITE_SHOPIFY_STORE_DOMAIN`, `VITE_DEMO_MODE` |
| Worker API (backend) | Accès API backend | `VITE_API_BASE_URL`, `VITE_TENANT_ID`, `VITE_WORKER_API_KEY`, `WORKER_API_KEY` |

## Google & INSEE

| Service | Rôle | Variables concernées |
|---------|------|----------------------|
| Google OAuth | Auth Google | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` |
| INSEE / La Poste | API SIRET, données entreprises | `INSEE_API_KEY`, `INSEE_CLIENT_ID`, `INSEE_CLIENT_SECRET` |
| Looker | Reporting | `LOOKER_REPORT_ID` |

## Résumé par phase

- **Phase 1 (Outreach)** : 8 services externes
- **Phase 2 (Frontend/Client)** : 7 services externes
- **Infra/Hosting** : 4 plateformes
- **Google/INSEE** : 2 services

Total : **~20 services distincts** avec accès par API key / compte.
