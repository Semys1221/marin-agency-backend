import config from '@/config/client'

const DEMO_MODE = import.meta.env.VITE_DEMO_MODE === 'true' || location.search.includes('demo=true')

const demoData: Record<string, unknown> = {
  leads: [
    { id: 'lead-001', tenantId: 'marin', email: 'demo@example.com', firstName: 'Jean', companyName: 'Demo SARL', status: 'interested', funnelStep: 'profil', createdAt: '2026-06-25T08:00:00Z' },
    { id: 'lead-002', tenantId: 'marin', email: 'demo2@example.com', firstName: 'Marie', companyName: 'Demo SAS', status: 'fresh', funnelStep: 'landing', createdAt: '2026-06-28T10:00:00Z' },
  ],
  'leads/status': { ok: true },
  'campaigns/health': [
    { id: 'camp-001', name: 'Demo Campaign', status: 'running', leadsSent: 1450, replyRate: 1.93 },
  ],
  'keys/status': { outscraper: 'ok', gemini: 'ok', supabase: 'ok', instantly: 'ok' },
  'sequences/perf': [
    { id: 'seq-001', name: 'Séquence Démo', sent: 1200, opens: 480, openRate: 0.40, replies: 24, replyRate: 0.02 },
  ],
  'crm/prospects': [
    { id: 'crm-001', name: 'Marie Dupont', email: 'marie@demo.fr', company: 'Demo SAS', status: 'appointment_set', callCount: 1 },
    { id: 'crm-002', name: 'Jean Martin', email: 'jean@demo.fr', company: 'Demo SARL', status: 'interested', callCount: 0 },
  ],
  'funnel/health': { avgStepDurationMs: 23400, dropoutRate: 0.32, deadLinks: [], totalActiveSessions: 14 },
  'clients/quota': { callCount: 3, objective: 10, deadline: '2026-09-28' },
  'calls/content': [
    { callNumber: 1, title: 'Appel Commercial', script: 'Présentation du matériel fourni...', durationMin: 30 },
    { callNumber: 2, title: 'Onboarding Commercial', script: 'Setup technique complet...', durationMin: 45 },
  ],
  'shopify/products': [
    { id: 'prod-1', title: 'Lot de 100 pièces', price: '450€' },
    { id: 'prod-2', title: 'Pack découverte 50 unités', price: '250€' },
  ],
}

export async function apiGet<T>(path: string): Promise<T> {
  if (DEMO_MODE) {
    const data = demoData[path]
    if (data) return data as T
    return [] as unknown as T
  }

  const res = await fetch(`${config.apiBase}${path}`, {
    headers: { 'X-Tenant-ID': config.tenantId },
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export async function apiPost(path: string, body: unknown): Promise<{ ok: boolean }> {
  if (DEMO_MODE) return { ok: true }

  const res = await fetch(`${config.apiBase}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Tenant-ID': config.tenantId,
    },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export { DEMO_MODE }
