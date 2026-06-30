# Call Recording System

**Depends on:** `template/` + `backend-api` deployed.
**Source of truth:** [Eraser.io model-marin-agency](https://app.eraser.io/workspace/SG0Y12i3rX6JQ8PTTKrZ)

Système d'enregistrement des appels de suivi client (calls commercial). Les enregistrements sont utilisés pour le coaching, l'analyse de performance, et la traçabilité des engagements.

## Architecture

```
Quo.com (appels VoIP)
    │
    ▼
Enregistrement audio (fichier .mp3/.wav)
    │
    ├── Stockage : Supabase Storage (bucket `call-recordings`)
    │
    ├── Dashboard client → Lecture par le commercial (post-call)
    │
    └── Dashboard opérations → Analyse coaching par l'agent Marin
```

## Stack

| Layer | Technologie |
|-------|-------------|
| Appels VoIP | Quo.com (compte client) |
| Enregistrement | Quo.com native recording (activation dashboard) |
| Stockage | Supabase Storage bucket `call-recordings` |
| Upload | Backend API → `POST /api/recordings/upload` |
| Lecture | Dashboard client / Dashboard opérations (lecteur HTML audio) |
| Transcription | Gemini 1.5 Flash (optionnel, pour analyse coaching) |

## Table Supabase

```sql
CREATE TABLE call_recordings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL REFERENCES clients(tenant_id),
  call_id TEXT NOT NULL UNIQUE,  -- Quo.com call ID
  session_id INT REFERENCES call_sessions(id),  -- lié au calls-plan (J15, J30, etc.)
  recording_url TEXT NOT NULL,
  duration_seconds INT,
  file_size_bytes INT,
  transcript TEXT,  -- texte transcrit par Gemini (nullable)
  coaching_notes TEXT,  -- notes de coaching (nullable)
  status TEXT NOT NULL DEFAULT 'pending',  -- pending, transcribed, reviewed, archived
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_call_recordings_tenant ON call_recordings(tenant_id);
CREATE INDEX idx_call_recordings_session ON call_recordings(session_id);
```

## API Endpoints

### POST /api/recordings/upload

Upload d'un enregistrement audio depuis Quo.com vers Supabase Storage.

**Body multipart :**
- `file` — fichier audio (.mp3, .wav, .m4a)
- `tenant_id` — identifiant du client
- `call_id` — identifiant unique Quo.com
- `session_id` — session du calls-plan (optionnel)
- `duration_seconds` — durée de l'appel

**Response (201) :**
```json
{
  "id": "uuid",
  "recording_url": "https://storage.supabase.co/...",
  "status": "pending"
}
```

### GET /api/recordings/:tenant_id

Liste des enregistrements pour un client.

**Query params :**
- `session_id` — filtrer par session
- `status` — filtrer par statut

**Response (200) :**
```json
{
  "recordings": [
    {
      "id": "uuid",
      "session": 3,
      "call_date": "2026-07-15",
      "duration": 2450,
      "status": "transcribed",
      "recording_url": "...",
      "transcript_preview": "..."
    }
  ]
}
```

### GET /api/recordings/:tenant_id/:id

Détail d'un enregistrement + transcription.

**Response (200) :**
```json
{
  "id": "uuid",
  "recording_url": "...",
  "transcript": "Texte complet...",
  "coaching_notes": "Améliorer la gestion des objections...",
  "status": "transcribed",
  "call_date": "2026-07-15"
}
```

### PATCH /api/recordings/:tenant_id/:id

Mettre à jour le coaching notes ou le statut.

**Body :**
```json
{
  "coaching_notes": "Le commercial a bien géré l'objection prix.",
  "status": "reviewed"
}
```

### POST /api/recordings/:tenant_id/:id/transcribe

Déclencher la transcription via Gemini 1.5 Flash.

**Response (200) :**
```json
{
  "status": "processing"
}
```

## Workflow

### 1. Call terminé (Quo.com)

Quo.com enregistre l'appel automatiquement (paramètre dashboard Quo.com : "Record calls" activé).

### 2. Upload manuel (commercial ou agent)

Le commercial ou l'agent télécharge le fichier depuis Quo.com et l'upload via `POST /api/recordings/upload`.

**Alternative automatique (future) :** Webhook Quo.com → `POST /api/recordings/webhook/quo` si Quo.com expose un webhook post-call.

### 3. Transcription (Gemini)

`POST /api/recordings/:id/transcribe` → Gemini 1.5 Flash transcrit l'audio → stocke dans `call_recordings.transcript`.

### 4. Coaching (agent Marin)

L'agent Marin écoute / lit la transcription → rédige `coaching_notes` → update `status = "reviewed"`.

### 5. Visualisation (dashboard client)

Le dashboard client affiche la liste des enregistrements dans la section "Appels" avec un lecteur audio HTML `<audio controls>`.

### 6. Visualisation (dashboard opérations)

Le dashboard opérations affiche la même liste avec en plus les notes de coaching et le statut de transcription.

## Edge Cases

| Scénario | Comportement |
|----------|-------------|
| Fichier audio corrompu | `POST /upload` retourne 422 avec message "Fichier audio invalide" |
| Transcription échouée | `status = "transcription_failed"` + log d'erreur → retry possible |
| Aucun enregistrement | `GET /recordings/:tenant_id` retourne `{ "recordings": [] }` |
| Session sans call recording | Pas de blocage — le calls-plan continue sans enregistrement |
| Fichier trop volumineux | Limite Supabase Storage (50MB) — rejeter avec 413 si dépassé |
| Quo.com non accessible | Message "Service d'enregistrement indisponible" dans le dashboard |

## Dashboard Integration

### Composant dashboard client (HTML statique)

```html
<section id="call-recordings">
  <h2>Appels enregistrés</h2>
  <div id="recordings-list">
    <!-- Template row -->
    <div class="recording-item">
      <div class="recording-info">
        <span class="recording-date">15/07/2026</span>
        <span class="recording-duration">40 min</span>
        <span class="recording-status badge">Transcrit</span>
      </div>
      <audio controls src="..."></audio>
    </div>
    <!-- Empty state -->
    <div class="empty-state">Aucun enregistrement disponible</div>
  </div>
</section>
```

### Composant dashboard opérations (même HTML + coaching)

```html
<section id="coaching">
  <h2>Coaching</h2>
  <div class="coaching-notes">
    <p>Améliorer la gestion des objections sur le prix.</p>
    <p>Le commercial parle trop vite — recommander de ralentir.</p>
  </div>
</section>
```

## Demo mode

Quand `DEMO_MODE=true` :

```json
GET /api/recordings/demo?demo=true
{
  "recordings": [
    {
      "id": "demo-001",
      "session": 1,
      "call_date": "2026-07-01",
      "duration": 3600,
      "status": "transcribed",
      "recording_url": "/demo/call-recording-1.mp3",
      "transcript_preview": "Bonjour, je vous appelle suite à notre échange...",
      "coaching_notes": "Bon premier contact, voix claire."
    },
    {
      "id": "demo-002",
      "session": 3,
      "call_date": "2026-07-15",
      "duration": 2450,
      "status": "reviewed",
      "recording_url": "/demo/call-recording-2.mp3",
      "transcript_preview": "Nous avons bien reçu votre documentation...",
      "coaching_notes": "Améliorer la gestion des objections."
    }
  ],
  "empty_demo": {
    "recordings": []
  }
}
```

## Dependencies

- Quo.com compte client avec "Call recording" activé dans les paramètres
- Supabase Storage bucket `call-recordings` créé avec RLS (tenant_id filter)
- Gemini API key pour la transcription
- Backend API avec endpoint `POST /api/recordings/upload`
- Dashboard client avec section call recordings
- Dashboard opérations avec section coaching
