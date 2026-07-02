# Domain & DNS Architecture

## Domain Tree

```
marin.app              → marque principale, Google Workspace (evan@marin.app)
marincie.homes          → domaine transactionnel + envoi (Vercel, Resend, loop.so)
└── *.site (15+)       → cold outreach (Instantly, Smartlead)
```

## DNS Management

DNS est délégué à **Vercel** pour `marincie.homes` (nameservers Vercel pointés depuis le registrar).

### Records requis sur Vercel

| Type | Name | Value | Service |
|------|------|-------|---------|
| `MX` | `@` | `SMTP.GOOGLE.COM` (priority 1, 5, 10) | Google Workspace |
| `TXT` | `@` | `v=spf1 include:_spf.google.com include:spf.resend.com include:spf.loop.so ~all` | SPF |
| `TXT` | `resend._domainkey` | `dkim.resend.com` | Resend DKIM |
| `TXT` | `loop._domainkey` | Valeur donnée par loop.so | loop.so DKIM |
| `TXT` | `_dmarc` | `v=DMARC1; p=quarantine; rua=mailto:evan@marin.app` | DMARC |
| `CNAME` | `www` | `cname.vercel-dns.com` | Vercel |
| `CNAME` | `google._domainkey` | `google.com` | Google Workspace DKIM |
| `CNAME` | `gv-...` | `google.com` | Google Workspace verification |
| `A` | `@` | `76.76.21.21` (ou IP Render engine) | Render Engine (optionnel) |

## Services Integration

### Vercel (DNS + Hosting)
- Nameservers du registrar vers Vercel
- Domaine ajouté dans Vercel Dashboard → Project → Domains
- Vercel gère automatiquement les certificats SSL

### Google Workspace (`marin.app`)
- Boîte `evan@marin.app` active
- Utilisée pour : emails pro, admin console, GCP project
- DNS : MX + TXT SPF + CNAME vérification

### Resend (Transactional Emails)
- Domaine `marincie.homes` ajouté dans Resend Dashboard → Domains
- Resend fournit les enregistrements DKIM/SPF à ajouter dans le DNS Vercel
- Utilisé pour : call reminders, invoices, onboarding, service delivery
- **Code reference**: `build/agency-backend/frontend-engine/05-resend-emails.md`
- **Email templates**: `context/agency-communication/sequence-live/resend/`

### loop.so (Nurturing Emails)
- Domaine `marincie.homes` ajouté dans loop.so Settings → Domain
- loop.so fournit les enregistrements DKIM/SPF à ajouter dans le DNS Vercel
- Utilisé pour : interested, indecision, onboarding, upsell sequences
- **Code reference**: `context/agency-communication/loop-setup.md`
- **Webhook integration**: `context/agency-communication/sequence-live/loop/loop-integration.md`

### Instantly (Cold Outreach)
- Utilise des domaines `.site` dédiés (pas `marincie.homes`)
- Chaque domaine `.site` a ses propres enregistrements SPF/DKIM
- **Code reference**: `context/agency-communication/instantly-setup.md`

## Environment Variables

```env
# ─── Domain & Email ───────────────────────
DOMAIN_PRIMARY=marincie.homes
DOMAIN_BRAND=marin.app
GOOGLE_WORKSPACE_EMAIL=evan@marin.app

# ─── Resend ────────────────────────────────
RESEND_API_KEY=...
RESEND_FROM_EMAIL=Marin Support <support@marincie.homes>

# ─── loop.so ────────────────────────────────
LOOP_API_KEY=...
LOOP_WEBHOOK_SECRET=...
```

## Code Integration Points

### Email Signatures (shared React component)
Tous les emails (Resend + loop.so) utilisent le même composant React pour la signature :
`context/agency-communication/sequence-live/resend/react-model.md`
`context/agency-communication/sequence-live/loop/react-model.md`

### Transactional Emails (Resend)
- API : `resend.emails.send()` avec `from: RESEND_FROM_EMAIL`
- Templates HTML dans `sequence-live/resend/`
- Tracking table : `email_tracking` (Prisma schema dans `05-resend-emails.md`)

### Nurturing Sequences (loop.so)
- Webhook entrant : Hermes → `POST /api/loop/webhook` pour démarrer une séquence
- Webhook sortant : loop.so → `POST /api/loop/events` pour notifier Hermes des événements
- Payload specs dans `loop-integration.md`

## Verification Commands

```bash
# Propagation DNS
dig mx marincie.homes
dig txt marincie.homes
dig cname www.marincie.homes

# Vérification email
curl -X POST https://api.resend.com/emails/test \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -d '{"from":"test@marincie.homes","to":"evan@marin.app","subject":"Test","text":"Hello"}'

# Vérification webhook loop.so
curl -X POST https://app.loop.so/api/v1/webhook/test \
  -H "Authorization: Bearer $LOOP_API_KEY"
```
