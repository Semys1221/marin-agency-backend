-- =============================================
-- RLS Policies — Tenant Isolation
-- =============================================
-- Auth model: shared DB, X-Tenant-ID header, pas de login
-- service_role bypasses RLS (backend API)
-- anon key sees only their tenant data via X-Tenant-ID
-- =============================================

-- Enable RLS on all tenant-scoped tables
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE call_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE call_recordings ENABLE ROW LEVEL SECURITY;
ALTER TABLE tickets ENABLE ROW LEVEL SECURITY;
ALTER TABLE ticket_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE contracts ENABLE ROW LEVEL SECURITY;
ALTER TABLE funnel_submissions ENABLE ROW LEVEL SECURITY;

-- Legacy tables (outreach engine) — no tenant isolation needed (internal)
-- campaign_queue, leads, campaign_settings, campaign_analytics, niche_variable
-- RLS not enabled on these (service_role only)

-- =============================================
-- Tenant isolation policies (NEW tables)
-- =============================================

-- Each policy uses current_setting('request.x-tenant-id') to get the tenant
-- The backend middleware sets this from the X-Tenant-ID header

-- TENANTS
DROP POLICY IF EXISTS tenant_isolation_tenants ON tenants;
CREATE POLICY tenant_isolation_tenants ON tenants
  FOR ALL
  USING (id = current_setting('request.x-tenant-id', true)::uuid)
  WITH CHECK (id = current_setting('request.x-tenant-id', true)::uuid);

-- CLIENTS
DROP POLICY IF EXISTS tenant_isolation_clients ON clients;
CREATE POLICY tenant_isolation_clients ON clients
  FOR ALL
  USING (tenant_id = current_setting('request.x-tenant-id', true)::uuid)
  WITH CHECK (tenant_id = current_setting('request.x-tenant-id', true)::uuid);

-- CALL SESSIONS
DROP POLICY IF EXISTS tenant_isolation_call_sessions ON call_sessions;
CREATE POLICY tenant_isolation_call_sessions ON call_sessions
  FOR ALL
  USING (tenant_id = current_setting('request.x-tenant-id', true)::uuid)
  WITH CHECK (tenant_id = current_setting('request.x-tenant-id', true)::uuid);

-- CALL RECORDINGS
DROP POLICY IF EXISTS tenant_isolation_call_recordings ON call_recordings;
CREATE POLICY tenant_isolation_call_recordings ON call_recordings
  FOR ALL
  USING (tenant_id = current_setting('request.x-tenant-id', true)::uuid)
  WITH CHECK (tenant_id = current_setting('request.x-tenant-id', true)::uuid);

-- TICKETS
DROP POLICY IF EXISTS tenant_isolation_tickets ON tickets;
CREATE POLICY tenant_isolation_tickets ON tickets
  FOR ALL
  USING (tenant_id = current_setting('request.x-tenant-id', true)::uuid)
  WITH CHECK (tenant_id = current_setting('request.x-tenant-id', true)::uuid);

-- TICKET MESSAGES (via join)
DROP POLICY IF EXISTS tenant_isolation_ticket_messages ON ticket_messages;
CREATE POLICY tenant_isolation_ticket_messages ON ticket_messages
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM tickets t
      WHERE t.id = ticket_id
        AND t.tenant_id = current_setting('request.x-tenant-id', true)::uuid
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM tickets t
      WHERE t.id = ticket_id
        AND t.tenant_id = current_setting('request.x-tenant-id', true)::uuid
    )
  );

-- INVOICES
DROP POLICY IF EXISTS tenant_isolation_invoices ON invoices;
CREATE POLICY tenant_isolation_invoices ON invoices
  FOR ALL
  USING (tenant_id = current_setting('request.x-tenant-id', true)::uuid)
  WITH CHECK (tenant_id = current_setting('request.x-tenant-id', true)::uuid);

-- CONTRACTS
DROP POLICY IF EXISTS tenant_isolation_contracts ON contracts;
CREATE POLICY tenant_isolation_contracts ON contracts
  FOR ALL
  USING (tenant_id = current_setting('request.x-tenant-id', true)::uuid)
  WITH CHECK (tenant_id = current_setting('request.x-tenant-id', true)::uuid);

-- FUNNEL SUBMISSIONS
DROP POLICY IF EXISTS tenant_isolation_funnel_submissions ON funnel_submissions;
CREATE POLICY tenant_isolation_funnel_submissions ON funnel_submissions
  FOR ALL
  USING (tenant_id = current_setting('request.x-tenant-id', true)::uuid)
  WITH CHECK (tenant_id = current_setting('request.x-tenant-id', true)::uuid);

-- =============================================
-- Storage: call-recordings bucket
-- =============================================
-- Execute in Supabase SQL Editor (superuser required)

ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS tenant_isolation ON storage.objects;
CREATE POLICY tenant_isolation ON storage.objects
  FOR ALL
  USING (auth.role() = 'service_role' OR bucket_id = 'call-recordings')
  WITH CHECK (auth.role() = 'service_role' OR bucket_id = 'call-recordings');
