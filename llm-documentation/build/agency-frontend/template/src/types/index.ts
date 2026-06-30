export interface Lead {
  id: string
  tenantId: string
  email: string
  firstName?: string
  lastName?: string
  companyName?: string
  phone?: string
  status: LeadStatus
  funnelStep?: string
  source?: string
  createdAt: string
}

export type LeadStatus = 'fresh' | 'contacted' | 'replied' | 'interested' | 'client' | 'dead'

export type LeadDecision = 'no_show' | 'indecis' | 'closed'

export interface FunnelStep {
  id: number
  name: string
  data: Record<string, unknown>
  completed: boolean
}

export interface CampaignHealth {
  id: string
  name: string
  status: 'running' | 'paused' | 'completed' | 'failed'
  leadsSent: number
  replyRate: number
}

export interface ApiKeyStatus {
  [key: string]: 'ok' | 'dead' | 'unconfigured'
}
