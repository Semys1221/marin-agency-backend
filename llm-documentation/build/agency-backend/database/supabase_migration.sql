-- Migration: Create cold_leads and clean_leads tables
-- Run this in Supabase Dashboard SQL Editor or via `supabase db push`

CREATE TABLE IF NOT EXISTS cold_leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL,
  email TEXT NOT NULL,
  company_name TEXT,
  domain TEXT,
  phone TEXT,
  location TEXT,
  source TEXT DEFAULT 'outscraper',
  campaign_id TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(tenant_id, email)
);

CREATE INDEX IF NOT EXISTS idx_cold_leads_tenant ON cold_leads(tenant_id);
CREATE INDEX IF NOT EXISTS idx_cold_leads_campaign ON cold_leads(campaign_id);

CREATE TABLE IF NOT EXISTS clean_leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL,
  campaign_id TEXT,
  email TEXT NOT NULL,
  first_name TEXT,
  last_name TEXT,
  company_name TEXT,
  domain TEXT,
  phone TEXT,
  location TEXT,
  is_role_based BOOLEAN DEFAULT false,
  risk_score TEXT DEFAULT 'medium',
  profession TEXT,
  niche TEXT,
  status TEXT DEFAULT 'fresh',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  cleaned_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(tenant_id, campaign_id, email)
);

CREATE INDEX IF NOT EXISTS idx_clean_leads_tenant ON clean_leads(tenant_id);
CREATE INDEX IF NOT EXISTS idx_clean_leads_status ON clean_leads(status);

-- Optional: migrate existing legacy leads to cold_leads if table has data
-- INSERT INTO cold_leads (tenant_id, email, company_name, domain, phone, location, campaign_id, metadata)
-- SELECT 'sylk-conseils', email, company_name, domain, phone, location, 'legacy', metadata
-- FROM leads
-- ON CONFLICT (tenant_id, email) DO NOTHING;
