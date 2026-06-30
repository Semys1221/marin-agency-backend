# Webhooks — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=Lsn2Z2RN6-aC7kj-b0I3

**Note:** This component is NOT yet in the Eraser diagram. It is an operational concern (centralized webhook routing) that consolidates webhook handling from Stripe, Calendly, and Dropbox Sign. Should be added as a node in the next diagram update.

## Purpose
Central webhook handler for Stripe, Calendly, and Dropbox Sign. Validates signatures and routes to correct handler.

## Database Tables

No direct tables — updates are delegated to individual feature handlers (see dependencies).

## API Integrations

### Stripe Webhook Verification
```typescript
import Stripe from 'stripe';
const stripe = new Stripe(STRIPE_SECRET_KEY);
const event = stripe.webhooks.constructEvent(
  req.body, req.headers['stripe-signature'], STRIPE_WEBHOOK_SECRET
);
```

### Calendly Webhook Verification
```typescript
// Verify HMAC signature from Calendly
const crypto = require('crypto');
const signature = req.headers['calendly-webhook-signature'];
const expected = crypto.createHmac('sha256', CALENDLY_WEBHOOK_KEY)
  .update(JSON.stringify(req.body)).digest('hex');
// Compare signatures
```

### Dropbox Sign Webhook Verification
```typescript
// Verify API key in webhook payload
if (req.body.api_key !== DROPBOX_SIGN_API_KEY) {
  return res.status(401).json({ error: 'invalid signature' });
}
```

## Env Vars
```
STRIPE_WEBHOOK_SECRET=...
CALENDLY_WEBHOOK_KEY=...
DROPBOX_SIGN_API_KEY=...
```

## Endpoints
| Method | Path | Source | Events |
|--------|------|--------|--------|
| POST | `/webhooks/stripe` | Stripe | `payment_intent.succeeded`, `.failed`, `invoice.finalized` |
| POST | `/webhooks/calendly` | Calendly | `invitee.created`, `invitee.canceled` |
| POST | `/webhooks/dropbox-sign` | Dropbox Sign | `signature_request_signed`, `signature_request_declined` |

## Behavior
1. Receive webhook POST
2. Validate signature with service-specific method
3. Parse event type
4. Route to handler:
   - Stripe → `08-stripe-payment.md`
   - Calendly → `03-calendly-booking.md`
   - Dropbox Sign → `09-dropbox-sign-contract.md`
5. Return 200 OK
6. Log all events for audit trail

## Edge Cases
- Invalid signature → 401, log warning
- Unknown event type → 200 (acknowledge but ignore)
- Duplicate → idempotency via event ID
- Demo mode: accept without signature validation
