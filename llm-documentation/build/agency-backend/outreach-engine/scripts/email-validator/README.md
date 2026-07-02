# Email Validator — 2-Stage Cleaning Pipeline

- **Stage 1 (local)** : syntaxe, MX, role-based, disposable — zéro coût
- **Stage 2 (API)** : MyEmailVerifier — vérification SMTP réelle, catch-all, spam traps

## Installation

```bash
pip install dnspython requests
```

## Usage

### Pipeline complet (recommandé)

```bash
export MYEMAILVERIFIER_API_KEY=...
cat emails.txt | python cleaner.py
```

### Local seulement (gratuit, moins précis)

```bash
cat emails.txt | python cleaner.py --local
```

### Vérifier le solde de crédits

```bash
python cleaner.py --credits
```

### Mode démo (aucun appel API)

```bash
cat emails.txt | python cleaner.py --demo
```

### Script local uniquement (compatible avec l'ancien pipeline)

```bash
cat emails.txt | python email_validator.py [--smtp] [--catchall]
```

## Output

- `stdout` — JSON structuré
- `valid_emails.txt` — emails passés
- `invalid_emails.txt` — emails refusés avec raison

## Architecture

| Fichier | Rôle |
|---------|------|
| `cleaner.py` | Orchestrateur 2 stages (CLI + importable) |
| `email_validator.py` | Stage 1 — vérifications locales (MX, syntaxe, etc.) |
| `myemailverifier_client.py` | Stage 2 — client API MyEmailVerifier |

## Checks

| Check | Stage | Coût |
|-------|-------|------|
| Format (regex) | Local | 0€ |
| MX record | Local | 0€ |
| Role-based | Local + API | 0€ |
| Disposable | Local + API (1000+ domaines) | 0€ |
| SMTP handshake | API | 1 crédit |
| Catch-all | API | 1 crédit |
| Spam traps | API | 1 crédit |

## Comparaison

| Mode | Prix/20K emails | Précision |
|------|----------------|-----------|
| `--local` | 0€ | ~60% (MX + syntaxe seulement) |
| Par défaut (API) | ~$50 (20K crédits à $0.0025) | ~99% |
| `--demo` | 0€ | Aléatoire (test) |

## Intégration dans le pipeline

Ce module correspond au pipeline complet de `04-email-cleaning.md`. Il peut être utilisé en CLI ou importé :

```python
from cleaner import clean_emails
import asyncio

results = asyncio.run(clean_emails(["test@example.com"], use_api=True, api_key="..."))
```

## Doc MyEmailVerifier

https://github.com/pat-myemailverifier/myemailverifier-api
