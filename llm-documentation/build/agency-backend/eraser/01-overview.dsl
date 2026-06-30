title Marin Agency — Full Funnel
direction down

// ========== PHASE 1: OUTREACH ENGINE ==========

User Account [color: gray, icon: settings] {
  User JSON File [color:gray, icon:file]
}

AI & Orchestration [color: blue, icon: zap] {
  Generate Niches (Gemini) [color:blue, icon:zap]
  Announce on Slack [color:purple, icon:message-circle]
  Hermes Agent [color:purple, icon:zap]
}

Scraping [color: green, icon: search] {
  Outscraper Scrape [color:green, icon:search]
}

Cleaning [color: orange, icon: filter] {
  Quick Clean [color:orange, icon:filter]
  Handshake API [color:yellow, icon:check]
  DB Bounce API [color:orange, icon:shield]
}

Cold Outreach (Instantly) [color: teal, icon: mail] {
  Email Generator [color: purple, icon: file] {
    Email Model Template [color:blue, icon:file]
    Niche Variables (Supabase) [color:green, icon:database]
    A/B/C Variants [color:orange, icon:shuffle]
  }
  Check Campaign Exists [shape:diamond, color:teal, icon:search]
  Sequence Creator [color:purple, icon:edit]
  7-Step Multi-Variant [color: blue, icon: layers] {
    J1 / J4 / J7 [color:blue, icon:mail]
    J10 / J13 / J16 / J19 [color:blue, icon:mail]
  }
  Campaign Setup [color:purple, icon:settings]
  Push Leads [color:teal, icon:upload]
}

Benchmarks [color: red, icon: activity] {
  Analyze Performance [color:red, icon:bar-chart]
  Kill & Replace [color:red, icon:x]
  Scale Campaign [color:green, icon:trending-up]
}

// ========== PHASE 2: FRONTEND ENGINE ==========

Frontend Funnel [color: purple, icon: layout] {
  Interested Lead Captured [color:purple, icon:user]
  Landing Page Questionnaire [color:blue, icon:file-text]
  Zustand Cache [color:gray, icon:database]
  SIRET Qualification [shape:diamond, color:blue, icon:check]
}

Booking [color: green, icon: calendar] {
  Calendly Booked [color:green, icon:calendar]
  Countdown to Call [color:blue, icon:clock]
  Self Discovery Offered [color:yellow, icon:zap]
}

Detective Agent [color: orange, icon: search] {
  Scrape JSON Website [color:orange, icon:search]
  Lead Intelligence [color:orange, icon:file]
}

Transactional Emails (Resend) [color: teal, icon: send] {
  Interested [color:green, icon:mail]
  Info Requested [color:green, icon:mail]
  No-Show [color:green, icon:mail]
  Call Reminder [color:green, icon:mail]
  Indecision [color:green, icon:mail]
  Onboarding [color:green, icon:mail]
  Invoice [color:green, icon:mail]
  Service Delivery [color:green, icon:mail]
  Call Description [color:green, icon:mail]
  Upsell [color:green, icon:mail]
}

Call Stage [color: blue, icon: phone] {
  Call Page [color:blue, icon:phone]
  Live Form Questionnaire [color:blue, icon:edit]
  Progress Saved on Pause [color:green, icon:pause]
}

Post Call [color: red, icon: flag] {
  Decision [shape:diamond, color:red, icon:flag]
  Closed Won [color:green, icon:thumbs-up]
  Indecis [color:yellow, icon:clock]
  Not Interested [color:gray, icon:x]
}

Payment & Contract [color: green, icon: dollar-sign] {
  Stripe Payment [color:green, icon:dollar-sign]
  Gift (Jabra Headset) [color:yellow, icon:gift]
  Dropbox Sign Contract [color:purple, icon:file-text]
}

Aftermath [color: green, icon: check-circle] {
  CRM Update [color:green, icon:database]
  Onboarding in App [color:green, icon:code]
  Client Dashboard HTML [color:green, icon:layout]
  Resend Transactional Sequence [color:purple, icon:mail]
  Looker Studio Embed [color:teal, icon:bar-chart]
}

Duplication [color: purple, icon: copy] {
  Duplication Form [color:blue, icon:edit]
  Vercel Deploy [color:blue, icon:upload]
  Hermes Activation [color:purple, icon:zap]
}

Sequence Creator (Dual) [color: purple, icon: layout] {
  Instantly Cold Mode [color:teal, icon:mail]
  Resend Transactional Mode [color:teal, icon:send]
}

Ticket System [color: green, icon: life-buoy] {
  Client Email [icon: mail, color: gray]
  Resend Inbound Webhook [icon: send, color: teal]
  Ticket Handler [color: green, icon: life-buoy] {
    POST /api/ticket/incoming [color: green]
    GET /api/tickets [color: green]
    POST /api/tickets/resolve [color: green]
    POST /api/tickets/assign [color: green]
    POST /api/sla/check [color: green]
  }
  Gemini Auto-Reply [color:blue, icon:zap]
  Ticket Dashboard [color:gray, icon:layout]
  SLA Checker [color:orange, icon:clock]
}

Infrastructure [color: gray, icon: server] {
  Supabase Postgres [shape:cylinder, color:blue, icon:database]
  Slack Notifications [color:purple, icon:bell]
  Sequence Creator Server [color:purple, icon:server]
}

Webhooks [color: gray, icon: server] {
  Stripe Webhook [color:green, icon:dollar-sign]
  Calendly Webhook [color:blue, icon:calendar]
  Dropbox Sign Webhook [color:purple, icon:file-text]
}

// ===== PHASE 1 FLOW =====
User JSON File > Generate Niches (Gemini): read config
Generate Niches (Gemini) > Announce on Slack: 10 niches
Announce on Slack > Outscraper Scrape: start
Outscraper Scrape > Quick Clean: raw leads
Quick Clean > Handshake API: MX + syntax
Handshake API > DB Bounce API: semi-clean
DB Bounce API > Check Campaign Exists: clean with phone
Check Campaign Exists > Sequence Creator: NO campaign
Email Model Template > Niche Variables (Supabase): resolve {variables}
Niche Variables (Supabase) > A/B/C Variants: generate per niche
A/B/C Variants > Sequence Creator: render variants
Sequence Creator > 7-Step Multi-Variant: build steps
7-Step Multi-Variant > Campaign Setup: configured
Campaign Setup > Push Leads: push campaign
Check Campaign Exists > Push Leads: YES exists
Push Leads > Analyze Performance: leads in Instantly

Analyze Performance > Kill & Replace: bad perf
Kill & Replace > Generate Niches (Gemini): restart niches
Analyze Performance > Scale Campaign: good perf
Scale Campaign > Outscraper Scrape: scrape more

// ===== HERMES ORCHESTRATION =====
Hermes Agent > Check Campaign Exists: orchestrate
Hermes Agent > Sequence Creator: create cold sequences
Hermes Agent > Sequence Creator Server: use CLI
Hermes Agent > Sequence Creator (Dual): orchestrate both modes
Sequence Creator (Dual) > Instantly Cold Mode: switch
Sequence Creator (Dual) > Resend Transactional Mode: switch
Sequence Creator Server > Instantly Cold Mode: push via CLI
Sequence Creator Server > Resend Transactional Mode: send via HTTP
Hermes Agent > Analyze Performance: monitor
Hermes Agent > Kill & Replace: decide kill
Hermes Agent > Scale Campaign: decide scale

// ===== TRANSITION: interested lead =====
Push Leads > Interested Lead Captured: lead replies/interested

// ===== PHASE 2 FLOW =====
Interested Lead Captured > Landing Page Questionnaire: redirect to funnel
Landing Page Questionnaire > Zustand Cache: cache all answers
Zustand Cache > SIRET Qualification: validate company
SIRET Qualification > Calendly Booked: valid SIRET
SIRET Qualification > Landing Page Questionnaire: invalid send retry
Calendly Booked > Countdown to Call: set in DB
Countdown to Call > Self Discovery Offered: optional
Self Discovery Offered > Scrape JSON Website: trigger detective
Scrape JSON Website > Lead Intelligence: website analysis
Lead Intelligence > Interested: pre-call authority
Interested > Info Requested: AI responder
Info Requested > No-Show: missed call
No-Show > Call Reminder: upcoming call
Call Reminder > Indecision: post-call
Call Stage: {
  Call Page > Live Form Questionnaire: agent + data
  Live Form Questionnaire > Progress Saved on Pause: any moment
  Progress Saved on Pause > Live Form Questionnaire: resume
  Live Form Questionnaire > Decision: post-call
}
Decision > Closed Won: yes
Decision > Indecis: needs follow-up
Decision > Not Interested: dead
Closed Won > Onboarding: send welcome
Onboarding > Stripe Payment: collect payment
Stripe Payment > Gift (Jabra Headset): send gift
Gift (Jabra Headset) > Dropbox Sign Contract: sign contract
Dropbox Sign Contract > Invoice: send invoice
Invoice > CRM Update: deal closed
Service Delivery > CRM Update: deliverable sent
CRM Update > Onboarding in App: app handles it
Onboarding in App > Client Dashboard HTML: CRM endpoint
Client Dashboard HTML > Looker Studio Embed: embeds analytics
Client Dashboard HTML > Call Description: post-call summary
Call Description > Upsell: cross-sell
Upsell > Resend Transactional Sequence: nurture
Indecis > Resend Transactional Sequence: nurture
Not Interested > Resend Transactional Sequence: final

// ===== DUPLICATION FLOW =====
Aftermath > Duplication Form: new client trigger
Duplication Form > Vercel Deploy: copy template + deploy
Vercel Deploy > Hermes Activation: activate campaign

// ===== WEBHOOKS ROUTING =====
Stripe Webhook > Stripe Payment: route payment events
Calendly Webhook > Calendly Booked: route booking events
Dropbox Sign Webhook > Dropbox Sign Contract: route signature events

// ===== TICKET SYSTEM FLOW =====
Client Email > Resend Inbound Webhook: email entrant
Resend Inbound Webhook > POST /api/ticket/incoming: webhook POST
POST /api/ticket/incoming > Supabase Postgres: INSERT ticket
POST /api/ticket/incoming > Gemini Auto-Reply: generate ack
Gemini Auto-Reply > Resend Inbound Webhook: send reply
POST /api/ticket/incoming > Slack Notifications: notify #tickets
Ticket Dashboard > GET /api/tickets: fetch list
GET /api/tickets > Supabase Postgres: SELECT tickets
Ticket Dashboard > POST /api/tickets/assign: assign human
POST /api/tickets/assign > Supabase Postgres: UPDATE assignee
Ticket Dashboard > POST /api/tickets/resolve: resolve
POST /api/tickets/resolve > Supabase Postgres: UPDATE status
POST /api/tickets/resolve > Slack Notifications: notify resolution
SLA Checker > POST /api/sla/check: cron every 30min
POST /api/sla/check > Supabase Postgres: SELECT overdue
POST /api/sla/check > Slack Notifications: escalate SLA

// ===== CROSS-CUTTING =====
Supabase Postgres > User JSON File: users
Supabase Postgres > Push Leads: store
Supabase Postgres > Niche Variables (Supabase): store
Supabase Postgres > Analyze Performance: metrics
Supabase Postgres > Zustand Cache: persist
Supabase Postgres > Calendly Booked: create user
Supabase Postgres > Countdown to Call: store time
Supabase Postgres > Live Form Questionnaire: real-time store
Supabase Postgres > Stripe Payment: payment record
Supabase Postgres > Dropbox Sign Contract: contract status
Supabase Postgres > CRM Update: client + callsessions
Supabase Postgres > Transactional Emails (Resend): log sends
Slack Notifications > Announce on Slack: notify
Slack Notifications > Outscraper Scrape: notify
Slack Notifications > Quick Clean: notify
Slack Notifications > DB Bounce API: notify
Slack Notifications > Push Leads: notify
Slack Notifications > Analyze Performance: notify
Slack Notifications > Hermes Agent: alerts
Slack Notifications > Stripe Payment: payment notification
Slack Notifications > Dropbox Sign Contract: contract signed
