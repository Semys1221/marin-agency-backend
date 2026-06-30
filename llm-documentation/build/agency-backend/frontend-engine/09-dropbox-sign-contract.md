# Dropbox Sign Contract — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=MC4Q49k19ArM9fjDEDg6

## Purpose
Sends contract for e-signature via Dropbox Sign after payment is confirmed.

## Database Tables

### clients (write — contract_id)
```prisma
model Client {
  id         String   @id @default(uuid()) @db.Uuid
  tenantId   String   @unique @map("tenant_id")
  contractId String?  @map("contract_id")
  status     String   @default("active")
  @@map("clients")
}
```

## API Integrations
### Dropbox Sign (HelloSign)
```typescript
import { SignatureRequestApi } from '@dropbox/sign';

const api = new SignatureRequestApi();
api.username = DROPBOX_SIGN_API_KEY;

await api.signatureRequestSend({
  signatureRequest: {
    title: 'Contrat de prestation Marin',
    subject: 'Veuillez signer votre contrat',
    signers: [{ email_address: client.email, name: client.companyName }],
    files: [contractPdf]
  }
});

// Webhook verification: check API key in payload
```

## Env Vars
```
DROPBOX_SIGN_API_KEY=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Webhook
| Method | Path | Events |
|--------|------|--------|
| POST | `/webhooks/dropbox-sign` | `signature_request_signed`, `signature_request_declined` |

## Behavior
1. After payment → generate contract from template with client vars
2. Send via Dropbox Sign API for e-signature
3. Webhook `signature_request_signed` fires
4. Store signed contract URL in `clients.contract_id`
5. Update `clients.status = 'active'`
6. Send signed copy to client, Slack notification

## Edge Cases
- Signer email invalid → retry with correct email
- Contract expired → regenerate and resend
- Key dead → return descriptive error
- Demo mode: auto-sign, skip API calls
