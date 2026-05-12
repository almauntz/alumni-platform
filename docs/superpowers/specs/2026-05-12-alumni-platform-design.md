# Alumni Platform — Design Spec

**Date:** 2026-05-12  
**Stack:** Vue 3 (Vite) + FastAPI + SQLModel + SQLite  
**Purpose:** Lecture demo for teaching testing and mocking concepts

---

## Overview

A minimal alumni registration and verification platform. Alumni submit a registration form; staff verify them through an admin panel. Verification follows two paths based on graduation year. No auth, no pagination.

---

## Architecture

```
alumni_platform/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routers/
│   │   ├── alumni.py
│   │   └── external.py
│   └── tests/
│       └── test_alumni.py
└── frontend/
    └── src/
        ├── views/
        │   ├── RegistrationView.vue
        │   └── AdminView.vue
        ├── components/
        │   └── AlumniRow.vue
        └── router/index.js
```

- FastAPI on `:8000`, Vue dev server on `:5173` (proxies `/api` to backend)
- Single SQLite file: `alumni.db`

---

## Data Model

**Table: `alumni`**

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | int PK | auto | |
| `ime` | str | yes | First name |
| `prezime` | str | yes | Last name |
| `spol` | enum | yes | `M` / `F` / `Ostalo` |
| `broj_indeksa` | str | yes | Student index number |
| `fakultet` | str | yes | One of 13 faculties |
| `odsjek` | str | yes | Department, or "Ostalo" |
| `studijski_program` | str | no | |
| `usmjerenje` | str | no | |
| `godina_pocetka` | str | yes | Format: "YYYY/YYYY" |
| `godina_zavrsetka` | str | yes | Format: "YYYY/YYYY" |
| `broj_diplome` | str | yes | Diploma number |
| `status` | enum | auto | `pending` / `verified` / `rejected` |
| `created_at` | datetime | auto | |

---

## API Endpoints

### Alumni Router (`/api/alumni`)

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/alumni` | Register new alumni, status = `pending` |
| `GET` | `/api/alumni` | List all alumni (staff admin use) |
| `PATCH` | `/api/alumni/{id}/verify` | Approve or reject; body: `{"action": "approve" \| "reject"}` |
| `POST` | `/api/alumni/{id}/check` | Trigger external DB check; returns submitted + external data |

### External Router (`/api/external`)

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/external/check` | Simulated external university DB check |

Query params: `ime`, `prezime`, `broj_indeksa`, `broj_diplome`

Response (if found):
```json
{
  "found": true,
  "data": {
    "ime": "...",
    "prezime": "...",
    "broj_indeksa": "...",
    "broj_diplome": "...",
    "fakultet": "...",
    "odsjek": "...",
    "godina_zavrsetka": "..."
  }
}
```

Response (if not found):
```json
{ "found": false, "data": null }
```

This router is the **mock seam** — tests patch it to return controlled responses without any real DB.

---

## Verification Logic

Graduation year is extracted from `godina_zavrsetka` (first 4 chars).

**Pre-2007 path** (year < 2007):
- Staff sees the alumni record in the admin panel
- Manual Approve / Reject buttons
- PATCH `/api/alumni/{id}/verify` with `{"action": "approve"}` or `{"action": "reject"}`

**Post-2007 path** (year ≥ 2007):
- Staff clicks "Check in DB" button → frontend calls `POST /api/alumni/{id}/check`
- Backend handler calls `GET /api/external/check` internally (server-to-server) with `ime`, `prezime`, `broj_indeksa`, `broj_diplome`
- Response with submitted data + external data is returned to the frontend
- Admin panel displays submitted data alongside data returned from external check
- Staff reviews both and clicks Approve or Reject
- PATCH `/api/alumni/{id}/verify` finalizes the status

---

## Frontend Views

### `/` — RegistrationView
- Form with all required fields
- `fakultet` dropdown (13 faculties hardcoded)
- `odsjek` dropdown cascades from selected faculty, includes "Ostalo"
- `godina_pocetka` and `godina_zavrsetka` as text inputs, placeholder "YYYY/YYYY"
- Submit → POST `/api/alumni`
- Success: confirmation message; Error: show API validation errors

### `/admin` — AdminView
- Table of all alumni fetched from GET `/api/alumni`
- Each row shows: name, index, faculty, graduation year, status badge
- Pre-2007 rows: Approve / Reject buttons
- Post-2007 rows: "Check in DB" button; after check, shows submitted vs. external data side by side, then Approve / Reject buttons
- No auth, no login

### `AlumniRow.vue`
- Extracted row component for the admin table
- Handles its own check/approve/reject actions and local state (e.g. showing external data after check)

---

## Testing

File: `backend/tests/test_alumni.py`  
Framework: `pytest` + `httpx` (FastAPI `TestClient`) + `unittest.mock`

Key test cases:
1. POST `/api/alumni` creates a record with `status: pending`
2. PATCH approve on pre-2007 alumni sets `status: verified`
3. PATCH reject sets `status: rejected`
4. Post-2007: mock `external.py` router to return `found: true` → verify sets `status: verified`
5. Post-2007: mock returns `found: false` → verify sets `status: rejected`
6. Mock returns different data than submitted → staff still sees both, can approve

The external router is the injection point — `unittest.mock.patch` replaces its response in tests, demonstrating the swap-out pattern.

---

## Faculty & Department Data

13 faculties hardcoded in frontend (and validated in backend enum or list):
- Prirodno-matematički fakultet
- Filozofski fakultet
- Pravni fakultet
- Ekonomski fakultet
- Medicinski fakultet
- Farmaceutski fakultet
- Fakultet elektrotehnike
- Rudarsko-Geološko-Građevinski fakultet
- Mašinski fakultet
- Fakultet za tjelesni odgoj i sport
- Tehnološki fakultet
- Akademija dramskih umjetnosti
- Edukacijsko-rehabilitacijski fakultet

Each faculty has a hardcoded department list plus "Ostalo" as a catch-all for older departments.

---

## Out of Scope

- Authentication / authorization
- Pagination
- Email notifications
- Password reset
- Role management
