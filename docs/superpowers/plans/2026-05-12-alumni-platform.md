# Alumni Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a minimal alumni registration and verification platform with a Vue 3 frontend and FastAPI backend, where verification follows two paths based on graduation year.

**Architecture:** FastAPI serves REST endpoints on `:8000`; Vue 3 SPA runs on `:5173` and proxies `/api` calls to the backend. A simulated external university DB router acts as a swap-out seam for testing. All data is stored in a single SQLite file `alumni.db` via SQLModel.

**Tech Stack:** Python 3.11+, FastAPI, SQLModel, SQLite, uvicorn, httpx; Vue 3, Vite, Vue Router

---

## File Map

```
alumni_platform/
├── backend/
│   ├── main.py                  # FastAPI app, mounts routers, CORS
│   ├── database.py              # SQLite engine, session dependency
│   ├── models.py                # Alumni SQLModel table + enums + Pydantic schemas
│   ├── routers/
│   │   ├── alumni.py            # POST/GET /api/alumni, PATCH verify, POST check
│   │   └── external.py          # GET /api/external/check (simulated)
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── vite.config.js           # /api proxy to :8000
    ├── package.json
    └── src/
        ├── main.js
        ├── router/
        │   └── index.js         # / and /admin routes
        ├── data/
        │   └── faculties.js     # hardcoded faculty→department map
        ├── views/
        │   ├── RegistrationView.vue
        │   └── AdminView.vue
        └── components/
            └── AlumniRow.vue
```

---

## Task 1: Backend scaffold — project structure + dependencies

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/database.py`
- Create: `backend/main.py`

- [ ] **Step 1: Create `backend/requirements.txt`**

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlmodel==0.0.19
httpx==0.27.0
```

- [ ] **Step 2: Install dependencies**

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

- [ ] **Step 3: Create `backend/database.py`**

```python
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./alumni.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```

- [ ] **Step 4: Create `backend/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routers import alumni, external

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alumni.router, prefix="/api/alumni", tags=["alumni"])
app.include_router(external.router, prefix="/api/external", tags=["external"])


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

- [ ] **Step 5: Verify the app starts**

```bash
cd backend
uvicorn main:app --reload
```

Expected: `Application startup complete.` with no errors.

- [ ] **Step 6: Commit**

```bash
git init
git add backend/
git commit -m "feat: backend scaffold with FastAPI, SQLModel, SQLite"
```

---

## Task 2: Data model

**Files:**
- Create: `backend/models.py`

- [ ] **Step 1: Create `backend/models.py`**

```python
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel


class Spol(str, Enum):
    M = "M"
    F = "F"
    Ostalo = "Ostalo"


class AlumniStatus(str, Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"


class AlumniBase(SQLModel):
    ime: str
    prezime: str
    spol: Spol
    broj_indeksa: str
    fakultet: str
    odsjek: str
    studijski_program: Optional[str] = None
    usmjerenje: Optional[str] = None
    godina_pocetka: str
    godina_zavrsetka: str
    broj_diplome: str


class Alumni(AlumniBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: AlumniStatus = AlumniStatus.pending
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AlumniCreate(AlumniBase):
    pass


class AlumniRead(AlumniBase):
    id: int
    status: AlumniStatus
    created_at: datetime


class VerifyAction(str, Enum):
    approve = "approve"
    reject = "reject"


class VerifyRequest(SQLModel):
    action: VerifyAction


class ExternalCheckData(SQLModel):
    ime: str
    prezime: str
    broj_indeksa: str
    broj_diplome: str
    fakultet: str
    odsjek: str
    godina_zavrsetka: str


class ExternalCheckResponse(SQLModel):
    found: bool
    data: Optional[ExternalCheckData] = None


class CheckResult(SQLModel):
    submitted: AlumniRead
    external: ExternalCheckResponse
```

- [ ] **Step 2: Restart the backend and verify no import errors**

```bash
uvicorn main:app --reload
```

Expected: startup with no errors.

- [ ] **Step 3: Commit**

```bash
git add backend/models.py
git commit -m "feat: Alumni SQLModel table, enums, and Pydantic schemas"
```

---

## Task 3: External router (simulated university DB)

**Files:**
- Create: `backend/routers/__init__.py`
- Create: `backend/routers/external.py`

- [ ] **Step 1: Create `backend/routers/__init__.py`**

```python
```
(empty file)

- [ ] **Step 2: Create `backend/routers/external.py`**

```python
from fastapi import APIRouter
from models import ExternalCheckData, ExternalCheckResponse

router = APIRouter()

# Simulated university database records — replace with real HTTP call later
_MOCK_DB: list[dict] = [
    {
        "ime": "Ana",
        "prezime": "Kovač",
        "broj_indeksa": "0123456",
        "broj_diplome": "D-2020-001",
        "fakultet": "Pravni fakultet",
        "odsjek": "Pravo",
        "godina_zavrsetka": "2020/2021",
    },
    {
        "ime": "Emir",
        "prezime": "Husić",
        "broj_indeksa": "0654321",
        "broj_diplome": "D-2015-042",
        "fakultet": "Ekonomski fakultet",
        "odsjek": "Menadžment",
        "godina_zavrsetka": "2015/2016",
    },
]


@router.get("/check", response_model=ExternalCheckResponse)
def check_alumni(
    ime: str,
    prezime: str,
    broj_indeksa: str,
    broj_diplome: str,
):
    for record in _MOCK_DB:
        if (
            record["broj_indeksa"] == broj_indeksa
            and record["broj_diplome"] == broj_diplome
        ):
            return ExternalCheckResponse(
                found=True,
                data=ExternalCheckData(**record),
            )
    return ExternalCheckResponse(found=False, data=None)
```

- [ ] **Step 3: Test the endpoint manually**

```bash
curl "http://localhost:8000/api/external/check?ime=Ana&prezime=Kovač&broj_indeksa=0123456&broj_diplome=D-2020-001"
```

Expected:
```json
{"found":true,"data":{"ime":"Ana","prezime":"Kovač","broj_indeksa":"0123456","broj_diplome":"D-2020-001","fakultet":"Pravni fakultet","odsjek":"Pravo","godina_zavrsetka":"2020/2021"}}
```

- [ ] **Step 4: Commit**

```bash
git add backend/routers/
git commit -m "feat: simulated external university DB check endpoint"
```

---

## Task 4: Alumni router

**Files:**
- Create: `backend/routers/alumni.py`

- [ ] **Step 1: Create `backend/routers/alumni.py`**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import (
    Alumni,
    AlumniCreate,
    AlumniRead,
    AlumniStatus,
    CheckResult,
    ExternalCheckResponse,
    VerifyRequest,
)
from routers.external import check_alumni

router = APIRouter()


@router.post("", response_model=AlumniRead, status_code=201)
def register_alumni(payload: AlumniCreate, session: Session = Depends(get_session)):
    alumni = Alumni.model_validate(payload)
    session.add(alumni)
    session.commit()
    session.refresh(alumni)
    return alumni


@router.get("", response_model=list[AlumniRead])
def list_alumni(session: Session = Depends(get_session)):
    return session.exec(select(Alumni)).all()


@router.patch("/{alumni_id}/verify", response_model=AlumniRead)
def verify_alumni(
    alumni_id: int,
    payload: VerifyRequest,
    session: Session = Depends(get_session),
):
    alumni = session.get(Alumni, alumni_id)
    if not alumni:
        raise HTTPException(status_code=404, detail="Alumni not found")
    alumni.status = (
        AlumniStatus.verified if payload.action == "approve" else AlumniStatus.rejected
    )
    session.add(alumni)
    session.commit()
    session.refresh(alumni)
    return alumni


@router.post("/{alumni_id}/check", response_model=CheckResult)
def check_alumni_in_external_db(
    alumni_id: int,
    session: Session = Depends(get_session),
):
    alumni = session.get(Alumni, alumni_id)
    if not alumni:
        raise HTTPException(status_code=404, detail="Alumni not found")
    external_result: ExternalCheckResponse = check_alumni(
        ime=alumni.ime,
        prezime=alumni.prezime,
        broj_indeksa=alumni.broj_indeksa,
        broj_diplome=alumni.broj_diplome,
    )
    return CheckResult(
        submitted=AlumniRead.model_validate(alumni),
        external=external_result,
    )
```

- [ ] **Step 2: Restart backend and verify all routes appear at `/docs`**

Open `http://localhost:8000/docs` — you should see:
- `POST /api/alumni`
- `GET /api/alumni`
- `PATCH /api/alumni/{alumni_id}/verify`
- `POST /api/alumni/{alumni_id}/check`
- `GET /api/external/check`

- [ ] **Step 3: Quick smoke test via curl**

```bash
# Register an alumni
curl -X POST http://localhost:8000/api/alumni \
  -H "Content-Type: application/json" \
  -d '{"ime":"Ana","prezime":"Kovač","spol":"F","broj_indeksa":"0123456","fakultet":"Pravni fakultet","odsjek":"Pravo","godina_pocetka":"2016/2017","godina_zavrsetka":"2020/2021","broj_diplome":"D-2020-001"}'

# List all alumni
curl http://localhost:8000/api/alumni
```

Expected: first call returns the alumni object with `"status":"pending"`, second returns a list with that alumni.

- [ ] **Step 4: Commit**

```bash
git add backend/routers/alumni.py
git commit -m "feat: alumni registration, listing, verification, and external check endpoints"
```

---

## Task 5: Frontend scaffold

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.js`
- Create: `frontend/src/router/index.js`

- [ ] **Step 1: Scaffold Vue project**

```bash
cd alumni_platform
npm create vite@latest frontend -- --template vue
cd frontend
npm install
npm install vue-router@4
```

- [ ] **Step 2: Replace `frontend/vite.config.js`**

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

- [ ] **Step 3: Create `frontend/src/router/index.js`**

```js
import { createRouter, createWebHistory } from 'vue-router'
import RegistrationView from '../views/RegistrationView.vue'
import AdminView from '../views/AdminView.vue'

const routes = [
  { path: '/', component: RegistrationView },
  { path: '/admin', component: AdminView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
```

- [ ] **Step 4: Replace `frontend/src/main.js`**

```js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

createApp(App).use(router).mount('#app')
```

- [ ] **Step 5: Replace `frontend/src/App.vue`**

```vue
<template>
  <nav>
    <router-link to="/">Registracija</router-link> |
    <router-link to="/admin">Admin</router-link>
  </nav>
  <router-view />
</template>
```

- [ ] **Step 6: Start the dev server and verify routing works**

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` — should load without errors. `/admin` should also load (views don't exist yet, so expect a blank or error until Task 6).

- [ ] **Step 7: Commit**

```bash
git add frontend/
git commit -m "feat: Vue 3 frontend scaffold with Vite, Vue Router, and API proxy"
```

---

## Task 6: Faculty and department data

**Files:**
- Create: `frontend/src/data/faculties.js`

- [ ] **Step 1: Create `frontend/src/data/faculties.js`**

```js
export const FACULTIES = {
  "Prirodno-matematički fakultet": [
    "Matematika", "Fizika", "Hemija", "Biologija", "Geografija", "Ostalo"
  ],
  "Filozofski fakultet": [
    "Bosanski jezik i književnost", "Historija", "Pedagogija", "Psihologija",
    "Sociologija", "Filozofija", "Komparativna književnost", "Ostalo"
  ],
  "Pravni fakultet": [
    "Pravo", "Kriminalistika", "Ostalo"
  ],
  "Ekonomski fakultet": [
    "Ekonomija", "Menadžment", "Računovodstvo i revizija", "Finansije",
    "Marketing", "Ostalo"
  ],
  "Medicinski fakultet": [
    "Medicina", "Ostalo"
  ],
  "Farmaceutski fakultet": [
    "Farmacija", "Ostalo"
  ],
  "Fakultet elektrotehnike": [
    "Automatika i elektronika", "Telekomunikacije", "Računarstvo i informatika",
    "Elektroenergetika", "Ostalo"
  ],
  "Rudarsko-Geološko-Građevinski fakultet": [
    "Rudarstvo", "Geologija", "Građevinarstvo", "Geodezija", "Ostalo"
  ],
  "Mašinski fakultet": [
    "Mašinstvo", "Industrijsko inženjerstvo", "Ostalo"
  ],
  "Fakultet za tjelesni odgoj i sport": [
    "Tjelesni odgoj i sport", "Ostalo"
  ],
  "Tehnološki fakultet": [
    "Hemijsko inženjerstvo", "Prehrambena tehnologija", "Tekstilno inženjerstvo", "Ostalo"
  ],
  "Akademija dramskih umjetnosti": [
    "Gluma", "Režija", "Dramaturgija", "Ostalo"
  ],
  "Edukacijsko-rehabilitacijski fakultet": [
    "Logopedija i audiologija", "Specijalna edukacija", "Ostalo"
  ],
}

export const FACULTY_NAMES = Object.keys(FACULTIES)
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/data/faculties.js
git commit -m "feat: hardcoded faculty and department data"
```

---

## Task 7: Registration view

**Files:**
- Create: `frontend/src/views/RegistrationView.vue`

- [ ] **Step 1: Create `frontend/src/views/RegistrationView.vue`**

```vue
<template>
  <div class="registration">
    <h1>Registracija alumni</h1>

    <div v-if="success" class="success">
      Registracija uspješna! Vaš zahtjev je u obradi.
    </div>

    <form v-else @submit.prevent="submit">
      <div class="field">
        <label>Ime *</label>
        <input v-model="form.ime" required />
      </div>

      <div class="field">
        <label>Prezime *</label>
        <input v-model="form.prezime" required />
      </div>

      <div class="field">
        <label>Spol *</label>
        <select v-model="form.spol" required>
          <option value="">-- odaberite --</option>
          <option value="M">Muški</option>
          <option value="F">Ženski</option>
          <option value="Ostalo">Ostalo</option>
        </select>
      </div>

      <div class="field">
        <label>Broj indeksa *</label>
        <input v-model="form.broj_indeksa" required />
      </div>

      <div class="field">
        <label>Fakultet *</label>
        <select v-model="form.fakultet" required @change="form.odsjek = ''">
          <option value="">-- odaberite --</option>
          <option v-for="f in FACULTY_NAMES" :key="f" :value="f">{{ f }}</option>
        </select>
      </div>

      <div class="field">
        <label>Odsjek *</label>
        <select v-model="form.odsjek" required :disabled="!form.fakultet">
          <option value="">-- odaberite --</option>
          <option
            v-for="d in departments"
            :key="d"
            :value="d"
          >{{ d }}</option>
        </select>
      </div>

      <div class="field">
        <label>Studijski program</label>
        <input v-model="form.studijski_program" />
      </div>

      <div class="field">
        <label>Usmjerenje</label>
        <input v-model="form.usmjerenje" />
      </div>

      <div class="field">
        <label>Godina početka studija * (npr. 2015/2016)</label>
        <input v-model="form.godina_pocetka" placeholder="YYYY/YYYY" required pattern="\d{4}/\d{4}" />
      </div>

      <div class="field">
        <label>Godina završetka studija * (npr. 2019/2020)</label>
        <input v-model="form.godina_zavrsetka" placeholder="YYYY/YYYY" required pattern="\d{4}/\d{4}" />
      </div>

      <div class="field">
        <label>Broj diplome *</label>
        <input v-model="form.broj_diplome" required />
      </div>

      <div v-if="errors.length" class="errors">
        <p v-for="e in errors" :key="e">{{ e }}</p>
      </div>

      <button type="submit" :disabled="submitting">
        {{ submitting ? 'Slanje...' : 'Registruj se' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { FACULTIES, FACULTY_NAMES } from '../data/faculties.js'

const form = ref({
  ime: '',
  prezime: '',
  spol: '',
  broj_indeksa: '',
  fakultet: '',
  odsjek: '',
  studijski_program: '',
  usmjerenje: '',
  godina_pocetka: '',
  godina_zavrsetka: '',
  broj_diplome: '',
})

const success = ref(false)
const submitting = ref(false)
const errors = ref([])

const departments = computed(() =>
  form.value.fakultet ? FACULTIES[form.value.fakultet] : []
)

async function submit() {
  errors.value = []
  submitting.value = true
  try {
    const res = await fetch('/api/alumni', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value),
    })
    if (res.ok) {
      success.value = true
    } else {
      const data = await res.json()
      if (data.detail) {
        errors.value = Array.isArray(data.detail)
          ? data.detail.map(e => e.msg)
          : [data.detail]
      }
    }
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.registration { max-width: 540px; margin: 2rem auto; padding: 0 1rem; }
.field { margin-bottom: 1rem; display: flex; flex-direction: column; gap: 4px; }
label { font-weight: 600; font-size: 0.9rem; }
input, select { padding: 6px 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; }
button { padding: 8px 20px; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer; }
button:disabled { opacity: 0.6; cursor: default; }
.success { background: #d1fae5; padding: 1rem; border-radius: 4px; color: #065f46; }
.errors { background: #fee2e2; padding: 0.75rem; border-radius: 4px; color: #991b1b; }
</style>
```

- [ ] **Step 2: Verify registration form in browser**

Open `http://localhost:5173`. You should see:
- All form fields render
- Selecting a faculty populates the department dropdown
- Submitting with all required fields sends a POST to `/api/alumni` and shows the success message
- Submitting with missing fields shows browser validation

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/RegistrationView.vue
git commit -m "feat: alumni registration form with cascading faculty/department dropdowns"
```

---

## Task 8: AlumniRow component

**Files:**
- Create: `frontend/src/components/AlumniRow.vue`

- [ ] **Step 1: Create `frontend/src/components/AlumniRow.vue`**

```vue
<template>
  <tr>
    <td>{{ alumni.id }}</td>
    <td>{{ alumni.ime }} {{ alumni.prezime }}</td>
    <td>{{ alumni.broj_indeksa }}</td>
    <td>{{ alumni.fakultet }}</td>
    <td>{{ alumni.godina_zavrsetka }}</td>
    <td>
      <span :class="['badge', alumni.status]">{{ alumni.status }}</span>
    </td>
    <td class="actions">
      <!-- Pre-2007: manual approve/reject -->
      <template v-if="isPreTwoThousandSeven && alumni.status === 'pending'">
        <button class="btn-approve" @click="verify('approve')">Odobri</button>
        <button class="btn-reject" @click="verify('reject')">Odbij</button>
      </template>

      <!-- Post-2007: check in DB first -->
      <template v-else-if="!isPreTwoThousandSeven && alumni.status === 'pending'">
        <button v-if="!checkResult" class="btn-check" @click="checkInDb" :disabled="checking">
          {{ checking ? 'Provjera...' : 'Provjeri u bazi' }}
        </button>

        <template v-if="checkResult">
          <div class="check-comparison">
            <div>
              <strong>Prijavljeni podaci</strong>
              <pre>{{ submittedSummary }}</pre>
            </div>
            <div>
              <strong>Podaci iz baze</strong>
              <pre v-if="checkResult.external.found">{{ externalSummary }}</pre>
              <span v-else class="not-found">Nije pronađen u bazi</span>
            </div>
          </div>
          <button class="btn-approve" @click="verify('approve')">Odobri</button>
          <button class="btn-reject" @click="verify('reject')">Odbij</button>
        </template>
      </template>

      <!-- Already actioned -->
      <span v-else class="done">—</span>
    </td>
  </tr>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  alumni: { type: Object, required: true },
})

const emit = defineEmits(['updated'])

const checking = ref(false)
const checkResult = ref(null)

const graduationYear = computed(() =>
  parseInt(props.alumni.godina_zavrsetka.slice(0, 4))
)

const isPreTwoThousandSeven = computed(() => graduationYear.value < 2007)

const submittedSummary = computed(() => {
  const a = props.alumni
  return `Ime: ${a.ime} ${a.prezime}\nIndeks: ${a.broj_indeksa}\nDiploma: ${a.broj_diplome}\nFakultet: ${a.fakultet}\nOdsjek: ${a.odsjek}\nZavršetak: ${a.godina_zavrsetka}`
})

const externalSummary = computed(() => {
  const d = checkResult.value?.external?.data
  if (!d) return ''
  return `Ime: ${d.ime} ${d.prezime}\nIndeks: ${d.broj_indeksa}\nDiploma: ${d.broj_diplome}\nFakultet: ${d.fakultet}\nOdsjek: ${d.odsjek}\nZavršetak: ${d.godina_zavrsetka}`
})

async function checkInDb() {
  checking.value = true
  try {
    const res = await fetch(`/api/alumni/${props.alumni.id}/check`, { method: 'POST' })
    checkResult.value = await res.json()
  } finally {
    checking.value = false
  }
}

async function verify(action) {
  const res = await fetch(`/api/alumni/${props.alumni.id}/verify`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action }),
  })
  if (res.ok) {
    emit('updated')
  }
}
</script>

<style scoped>
td { padding: 8px 12px; vertical-align: top; }
.badge { padding: 2px 8px; border-radius: 10px; font-size: 0.8rem; font-weight: 600; }
.badge.pending { background: #fef3c7; color: #92400e; }
.badge.verified { background: #d1fae5; color: #065f46; }
.badge.rejected { background: #fee2e2; color: #991b1b; }
.actions { display: flex; flex-direction: column; gap: 6px; min-width: 160px; }
button { padding: 4px 12px; border: none; border-radius: 4px; cursor: pointer; font-size: 0.85rem; }
.btn-approve { background: #059669; color: white; }
.btn-reject { background: #dc2626; color: white; }
.btn-check { background: #2563eb; color: white; }
.check-comparison { display: flex; gap: 1rem; margin-bottom: 8px; }
.check-comparison pre { font-size: 0.78rem; background: #f3f4f6; padding: 6px; border-radius: 4px; white-space: pre-wrap; }
.not-found { color: #dc2626; font-weight: 600; }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/AlumniRow.vue
git commit -m "feat: AlumniRow component with pre/post-2007 verification UI"
```

---

## Task 9: Admin view

**Files:**
- Create: `frontend/src/views/AdminView.vue`

- [ ] **Step 1: Create `frontend/src/views/AdminView.vue`**

```vue
<template>
  <div class="admin">
    <h1>Admin panel</h1>
    <p v-if="loading">Učitavanje...</p>
    <p v-else-if="!alumniList.length">Nema registrovanih alumni.</p>
    <table v-else>
      <thead>
        <tr>
          <th>#</th>
          <th>Ime i prezime</th>
          <th>Broj indeksa</th>
          <th>Fakultet</th>
          <th>Godina završetka</th>
          <th>Status</th>
          <th>Akcije</th>
        </tr>
      </thead>
      <tbody>
        <AlumniRow
          v-for="alumni in alumniList"
          :key="alumni.id"
          :alumni="alumni"
          @updated="fetchAlumni"
        />
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AlumniRow from '../components/AlumniRow.vue'

const alumniList = ref([])
const loading = ref(true)

async function fetchAlumni() {
  loading.value = true
  try {
    const res = await fetch('/api/alumni')
    alumniList.value = await res.json()
  } finally {
    loading.value = false
  }
}

onMounted(fetchAlumni)
</script>

<style scoped>
.admin { max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 8px 12px; border-bottom: 2px solid #e5e7eb; font-size: 0.85rem; color: #6b7280; }
</style>
```

- [ ] **Step 2: Verify full flow in browser**

1. Open `http://localhost:5173`, register a post-2007 alumni using index `0123456` and diploma `D-2020-001`
2. Open `http://localhost:5173/admin`
3. Click "Provjeri u bazi" — should show side-by-side comparison
4. Click Odobri — status badge should change to `verified`
5. Register a pre-2007 alumni (graduation year `2005/2006`), go to admin, click Odobri directly

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/AdminView.vue
git commit -m "feat: admin panel listing all alumni with verification actions"
```

---

## Task 10: Final wiring check

- [ ] **Step 1: Verify both servers run together**

Terminal 1:
```bash
cd backend && source venv/bin/activate && uvicorn main:app --reload
```

Terminal 2:
```bash
cd frontend && npm run dev
```

- [ ] **Step 2: Full end-to-end smoke test**

1. Register alumni with all required fields filled, post-2007 graduation — confirm success message
2. Register alumni with pre-2007 graduation year (`2003/2004`) — confirm success message
3. Go to `/admin` — both records appear with `pending` status
4. For post-2007: click "Provjeri u bazi", verify comparison appears, click Odobri
5. For pre-2007: click Odobri directly
6. Both records now show `verified` badge
7. Register another post-2007 alumni with an index not in the simulated DB — click "Provjeri u bazi", see "Nije pronađen u bazi", click Odbij — status becomes `rejected`

- [ ] **Step 3: Final commit**

```bash
git add .
git commit -m "feat: complete alumni platform — registration, verification, admin panel"
```
