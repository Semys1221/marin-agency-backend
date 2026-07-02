# Outscraper Scraper — Google Maps Lead Scraper

**Doc API:** https://app.outscraper.cloud/api-docs
**SDK:** https://github.com/outscraper/outscraper-python

## Installation

```bash
pip install outscraper
```

## Usage

```bash
export OUTSCRAPER_API_KEY=...
python outscraper_scraper.py "plombier Paris" --limit 200
```

### Options

| Argument | Default | Description |
|----------|---------|-------------|
| `query` | (required) | Search query (e.g. `"plombier Paris"`) |
| `--limit` | 100 | Results per query |
| `--lang` | `fr` | Language |
| `--enrichment` | `contacts_n_leads` | Enrichments (space-separated) |
| `--output`, `-o` | stdout only | Output file (`.json` or `.csv`) |
| `--api-key` | `OUTSCRAPER_API_KEY` | Override API key |

### Enrichments disponibles

- `contacts_n_leads` — emails, téléphones, réseaux sociaux
- `emails_validator_service` — validation d'emails
- `disposable_email_checker` — détection emails jetables
- `whatsapp_checker` — vérification WhatsApp
- `phones_enricher_service` — enrichissement téléphone
- `trustpilot_service` — avis Trustpilot
- `companies_data` — données entreprises

### Output

```bash
python outscraper_scraper.py "plombier Paris" --limit 50 -o results.csv
```

Stdout : JSON brut. Avec `--output`, écrit en CSV ou JSON.

### Import Python

```python
from outscraper_scraper import search_maps

items = search_maps("coiffeur Lyon", limit=100, language="fr")
for item in items:
    email = item.get("email") or item.get("email_1", "")
    name = item.get("name", "")
    print(name, email)
```

### Filtrage

```python
from lead_filter import filter_leads, filter_stats

items = search_maps("plombier Paris", limit=200)
stats = filter_stats(items)
print(f"{stats['valid']}/{stats['total']} leads gardés")
clean = filter_leads(items)
```

## Intégration pipeline

Ce script correspond au scraping de `03-outscraper-scrape.md`. Les leads bruts sont ensuite nettoyés par `scripts/email-validator/cleaner.py`.
