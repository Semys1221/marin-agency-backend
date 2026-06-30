# Stripe Payment — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=7Udp0ZPwkqX6VbTMmSy4

## Purpose
Payment collection via Stripe: create payment intents, process invoices, handle webhooks.

## Database Tables

### clients (write — payment_id)
```prisma
model Client {
  id         String   @id @default(uuid()) @db.Uuid
  tenantId   String   @unique @map("tenant_id")
  paymentId  String?  @map("payment_id")
  offer      String   @default("main")  // main=2500€ | secondary=1900€
  status     String   @default("active")
  @@map("clients")
}
```

## API Integrations
### Stripe
```typescript
import Stripe from 'stripe';
const stripe = new Stripe(STRIPE_SECRET_KEY);

// Create payment intent
const intent = await stripe.paymentIntents.create({
  amount: 250000,  // €2500 in cents
  currency: 'eur',
  metadata: { tenant_id: 'client-a' }
});

// Webhook verification
const event = stripe.webhooks.constructEvent(
  req.body, req.headers['stripe-signature'], STRIPE_WEBHOOK_SECRET
);
```

## Env Vars
```
STRIPE_SECRET_KEY=...
STRIPE_PUBLISHABLE_KEY=...
STRIPE_WEBHOOK_SECRET=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## Webhook
| Method | Path | Events |
|--------|------|--------|
| POST | `/webhooks/stripe` | `payment_intent.succeeded`, `.failed`, `invoice.finalized` |

## Behavior
1. After Closed Won → send Onboarding email → create Stripe Payment Intent (€2500 or €1900)
2. Send payment link to lead via Resend
3. Lead completes payment on Stripe Checkout
4. Stripe fires `payment_intent.succeeded` webhook
5. Backend: update `clients.payment_id`, trigger Gift → Dropbox Sign → Invoice → CRM
6. Slack notification: payment received

## Gift (Jabra Headset)
Triggered automatically after successful payment, before contract signing (per Eraser diagram edge `Stripe Payment > Gift (Jabra Headset)`).
1. After `payment_intent.succeeded` webhook processed
2. Create fulfillment record in `clients.metadata.gift`
3. Notify Slack: `🎁 *Gift triggered for {client}* — ship Jabra Evolve2 75`
4. Mark gift as sent in client metadata
5. Proceed to Dropbox Sign contract

## Edge Cases
- Payment fails → notify agent, offer retry link
- Stripe key dead → return descriptive error, not crash
- Demo mode: auto-approve payment, skip Stripe
