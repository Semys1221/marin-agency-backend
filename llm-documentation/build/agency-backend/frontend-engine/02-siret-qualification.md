# SIRET Qualification — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=hzN1XFgzPeuiuOWRsW2E

## Purpose
Validates lead's SIRET before allowing Calendly booking. Only qualified companies proceed.

## Env Vars
None required (uses public SIRENE API).

## Behavior
1. Lead enters SIRET (14 digits) on landing page
2. Validate format (14 numeric, Luhn check)
3. Call public SIRENE API (insee.fr) for verification:
   - Company exists? → accept
   - Company active? → accept
   - Valid but inactive → flag for manual review
4. Valid → proceed to Calendly booking
5. Invalid → show retry with explanation

## API Integration
```typescript
// SIRENE API (public, no key required)
const response = await fetch(`https://api.insee.fr/entreprises/sirene/V3/siret/${siret}`)
const data = await response.json()
// Check: data.etablissement.etatAdministratif === 'A'
```

## Edge Cases
- SIRENE API unavailable → skip validation, allow booking with flag
- Invalid format → immediate retry, no API call
- SIRET matches existing client → flag as existing customer
- Demo mode: accept any valid-format SIRET (14 digits)
