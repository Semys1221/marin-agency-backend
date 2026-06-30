# Cold Contact — 7-Step Multi-Variant (Instantly)

## Modèle
Pipeline cold outreach via **Instantly**. 7 steps avec variantes A/B/C.
Variables résolues depuis la table `niche_variable` (Supabase).

## Structure

| Step | Jour | Variantes |
|------|------|-----------|
| 1 | J1 | A/B/C |
| 2 | J4 | A/B/C |
| 3 | J7 | A/B |
| 4 | J10 | A |
| 5 | J13 | A |
| 6 | J16 | A |
| 7 | J19 | A |

## Variables niche (résolues depuis Supabase)
- `{niche}` — nom de la niche
- `{niche_keyword_1/2/3}` — mots-clés sujet
- `{niche_member}` — membre singulier
- `{objectif}` — objectif
- `{pain_point}` — problème
- `{methode}` — méthode
- `{timeline}` — durée (ex: "60 jours")

## Variables lead (résolues par Instantly)
- `{{first_name}}` — prénom
- `{{phone_number}}` — téléphone

## Comportement après réponse positive

Quand Instantly détecte une réponse positive (reply detection) :

1. **Stop** — la séquence froide est immédiatement arrêtée pour ce lead
2. **Switch** — le lead passe dans la séquence **"Positive Reply Follow-up"** (3 steps)
3. **3 follow-ups max** — remerciement J+1, cas client J+4, clôture J+7
4. **Passe en manuel** — aucune relance automatique après J+7, le commercial prend le relais

### Les 3 follow-ups

| Step | Jour | Sujet | Contenu |
|------|------|-------|---------|
| 1 | J+1 | RE: {sujet d'origine} | Remerciement + confirmation intérêt + lien prise de RDV |
| 2 | J+4 | Suite de notre échange | Cas client similaire + preuve sociale |
| 3 | J+7 | Pour donner suite | Dernière relance avant passage en suivi manuel |

### Configuration Instantly

Dans le dashboard → **Campaign** → **Reply Detection** :
- `Action on reply` → **Move to another sequence**
- Target → **Positive Reply Follow-up** (3-step sequence)
- Si pas de réponse positive → la séquence froide continue ses 7 steps jusqu'au bout

## Template
Voir `sequence_creator.py` → `COLD_EMAIL_MODEL` pour le template complet.
