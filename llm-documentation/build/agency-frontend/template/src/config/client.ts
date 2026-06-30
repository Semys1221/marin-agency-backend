export interface ClientConfig {
  name: string
  domain: string
  offerType: 'agency' | 'ecommerce'
  branding: {
    accent: string
    accentDark: string
    bg: string
    text: string
  }
  tokens: {
    stripePublishableKey?: string
    calendlyUrl: string
    sentryDsn?: string
  }
  links: {
    microsoft?: string
    quo?: string
    looker?: string
    stripeDashboard?: string
  }
  apiBase: string
  tenantId: string
}

// Le frontend appelle UNIQUEMENT le backend-api (NodeJS + Prisma).
// Jamais l'outreach-engine (Python) directement.
// VITE_API_BASE = URL du backend-api en production.
const config: ClientConfig = {
  name: '...',
  domain: '...',
  offerType: 'agency',
  branding: {
    accent: '#49C5B6',
    accentDark: '#015048',
    bg: '#FAFAFA',
    text: '#000000',
  },
  tokens: {
    stripePublishableKey: '...',
    calendlyUrl: '...',
    sentryDsn: '...',
  },
  links: {
    microsoft: '...',
    quo: '...',
    looker: '...',
    stripeDashboard: '...',
  },
  apiBase: import.meta.env.VITE_API_BASE || '/api',
  tenantId: '...',
}

export default config
