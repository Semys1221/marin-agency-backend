# Duplication d'Instance — Procédure Opérationnelle

**Eraser.io :** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ (nœud "Duplication" dans le Full Funnel)
**Spec technique :** `build/agency-backend/frontend-engine/12-duplication.md`

---

## Quand dupliquer ?

Chaque nouveau client signé nécessite une duplication :
- Offre principale (2 500 €) — 22 steps funnel agency + dashboard
- Offre secondaire (1 900 €) — 11 steps funnel e-commerce + dashboard Shopify

## Processus (vue métier)

### 1. Admin remplit le formulaire de duplication
Champs : nom client, domaine, couleurs, logo, offre (agency/e-commerce), niche

### 2. Backend automatise
- Copie le template frontend → nouveau projet Vercel
- Modifie `config/client.ts` (branding, tokens, tenantId)
- Crée les enregistrements Supabase (client, config campagne)
- Déploie sur Vercel via API
- Crée le JSON utilisateur pour l'outreach engine
- Active Hermes pour le nouveau tenant

### 3. Client reçoit l'accès
- Dashboard client livré
- Campagne Hermes active
- Séquences email prêtes

## Dépendances

| Prérequis | Responsable |
|-----------|-------------|
| Template frontend existant (`build/agency-frontend/template/`) | Dev |
| API Vercel token configuré | Ops |
| Supabase accessible | Ops |
| Hermes agent actif | Ops |
| `context/agency-book/Esthetic/` — logo + favicon du client à uploader | Marketing |

## Références

| Document | Lien |
|----------|------|
| Spec technique duplication | `build/agency-backend/frontend-engine/12-duplication.md` |
| Template frontend | `build/agency-frontend/template/README.md` |
| Template dashboard | `build/agency-frontend/dashboard/template/README.md` |
| Duplication method pattern | `context/duplication-method/DUPLICATION-METHOD.MD` |
