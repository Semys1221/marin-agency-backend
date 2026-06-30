# Dashboard API — Phase 2

**Eraser diagram:** https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ?diagram=E-X9VSDsMQMxTsY5gOEL

## Purpose
Single aggregated API endpoint that returns all data needed by the 3 dashboards (internal, client agency, client e-commerce). Replaces 13 individual fetches with 1 call.

## Dependencies
- `agency-backend` fully deployed (all individual API endpoints exist on Render)

## Architecture
```
Dashboard (HTML) ── GET /api/dashboard?tenant_id=X ──> Backend API (NodeJS)
                                                          │
                                                   ┌──────┴──────┐
                                                   ▼              ▼
                                            Supabase DB    Individual API
                                                           endpoints (fallback)
```

## Behavior
1. Dashboard calls `GET /api/dashboard?tenant_id=X`
2. Backend aggregates data from Supabase (reads all relevant tables)
3. Returns a single JSON response with all sections
4. If any section fails, return `null` for that section (never crash the whole response)
5. Demo mode: return full mock JSON from `config/demo.js`

## Response Schema
```json
GET /api/dashboard?tenant_id=marin
{
  "tenant_id": "marin",
  "updated_at": "2026-06-29T09:00:00Z",
  "leads": [
    {
      "id": "lead-001",
      "email": "contact@example.com",
      "company_name": "Example SARL",
      "first_name": "Jean",
      "status": "new",
      "created_at": "2026-06-25T08:00:00Z",
      "last_contacted_at": null
    }
  ],
  "campaigns": {
    "health": [
      {
        "id": "camp-001",
        "name": "Grossistes Beauté Paris",
        "niche": "grossiste_beaute",
        "status": "active",
        "reply_rate": 1.93,
        "is_exhausted": false,
        "leads_found": 1450,
        "last_updated": "2026-06-29T08:00:00Z"
      }
    ],
    "sequences": [
      {
        "id": "seq-001",
        "name": "Cold Outreach",
        "sent": 120,
        "open_rate": 37.5,
        "reply_rate": 6.7
      }
    ]
  },
  "keys": {
    "outscraper": "ok",
    "gemini": "ok"
  },
  "renewals": [
    {
      "email": "contact@sportpro.fr",
      "service": "Microsoft",
      "expires_at": "2026-07-01",
      "days_remaining": 2
    }
  ],
  "scripts": [
    {
      "call_number": 1,
      "title": "Appel Découverte",
      "duration_minutes": 30
    }
  ],
  "prospects": [
    {
      "id": "crm-001",
      "email": "jean@example.com",
      "company_name": "ClientX",
      "status": "contacted",
      "last_contacted": "2026-06-10"
    }
  ],
  "funnel": {
    "avg_step_duration_ms": 23400,
    "dropout_rate": 0.32,
    "dead_links": ["/gift"],
    "total_active_sessions": 14
  },
  "reports": [
    {
      "id": "err-001",
      "message": "TypeError: cannot read prop",
      "level": "error",
      "url": "/checkout",
      "timestamp": "2026-06-29",
      "count": 5
    }
  ],
  "services": {
    "calendly": "https://calendly.com/{tenant}",
    "stripe": "https://dashboard.stripe.com",
    "looker_studio": "https://lookerstudio.google.com/embed/reporting/{REPORT_ID}",
    "microsoft": "https://account.microsoft.com",
    "quo": "https://quo.com",
    "shopify": null
  }
}
```

## Consumers

| Dashboard | tenant_id | shopify |
|-----------|-----------|---------|
| Internal (équipe Marin) | `marin` | null |
| Client Marin Agency | `{client_tenant_id}` | null |
| Client E-commerce | `{client_tenant_id}` | `{shopify_domain}` |

## Implementation

### Backend (NodeJS/Express)
```typescript
// src/routes/dashboard.ts
router.get('/api/dashboard', async (req, res) => {
  const { tenant_id } = req.query;
  if (!tenant_id) return res.status(400).json({ error: 'tenant_id required' });

  try {
    const [leads, campaigns, keys, renewals, sequences, scripts, prospects, funnel, reports] =
      await Promise.allSettled([
        prisma.cleanLead.findMany({ where: { tenantId: tenant_id.toString() }, take: 50 }),
        prisma.campaignAnalytics.findMany({ where: { tenantId: tenant_id.toString() }, orderBy: { checkedAt: 'desc' }, take: 20 }),
        // ... other queries
      ]);

    res.json({
      tenant_id,
      updated_at: new Date().toISOString(),
      leads: leads.status === 'fulfilled' ? leads.value : null,
      campaigns: campaigns.status === 'fulfilled' ? { health: campaigns.value } : null,
      // ... aggregate
    });
  } catch (err) {
    res.status(500).json({ error: 'dashboard aggregation failed' });
  }
});
```

### Frontend (HTML)
```javascript
// js/fetcher.js
async function loadDashboard(tenantId) {
  const res = await fetch(`/api/dashboard?tenant_id=${tenantId}`, {
    headers: { 'X-Tenant-ID': tenantId }
  });
  const data = await res.json();
  renderLeads(data.leads);
  renderCampaigns(data.campaigns);
  renderKeys(data.keys);
  // ... each section handles null gracefully
}
```

## Edge Cases
- Tenant not found → return empty arrays, not error
- Individual section fails → return `null` for that section, other sections still render
- Backend down → return 503, dashboard shows loading state
- Demo mode → return mock JSON, no DB calls
