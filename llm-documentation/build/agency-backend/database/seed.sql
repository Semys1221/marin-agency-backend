-- =============================================
-- Seed Data — Development & Testing
-- =============================================

-- Tenant "marin" (default agency tenant)
INSERT INTO tenants (id, slug, name, email, phone, domain, config)
VALUES (
  '00000000-0000-0000-0000-000000000001',
  'marin',
  'Marin Agency',
  'evan@marin.app',
  '+33600000000',
  'marin.app',
  '{"plan": "main", "features": ["outreach", "frontend", "dashboard"]}'::jsonb
);

-- Client "marin" (self-reference)
INSERT INTO clients (id, tenant_id, name, email, phone, company, siret, status)
VALUES (
  '00000000-0000-0000-0000-000000000010',
  '00000000-0000-0000-0000-000000000001',
  'Evan Nanguy',
  'evan@marin.app',
  '+33600000000',
  'Evan Nanguy EI',
  '88524803900010',
  'active'
);

-- Dummy leads for testing
INSERT INTO leads (id, place_id, email, first_name, company_name, domain, status, city, niche)
VALUES
  ('00000000-0000-0000-0000-000000000101', 'place_test_1', 'test1@example.com', 'Jean', 'Test SARL', 'example.com', 'raw', 'Paris', 'plumbing'),
  ('00000000-0000-0000-0000-000000000102', 'place_test_2', 'test2@example.com', 'Marie', 'Demo SAS', 'demo.com', 'raw', 'Lyon', 'electrician');

-- Niche variable sample
INSERT INTO niche_variable (id, niche, niche_keyword_1, niche_keyword_2, niche_member, objectif, pain_point, methode, offre)
VALUES (
  '00000000-0000-0000-0000-000000000201',
  'plumbing',
  'plumber',
  'plumbing company',
  'founder',
  'Get more plumbing clients',
  'Irregular leads, high competition',
  'Cold email + SEO',
  'Outreach Engine'
);
