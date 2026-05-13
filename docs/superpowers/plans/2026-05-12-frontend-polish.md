# Frontend Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply minimal, neutral styling polish to the alumni platform frontend — clean global reset, slim nav bar, registration form as a white card, admin table in a card with hover rows.

**Architecture:** Pure CSS changes only. Replace the Vite boilerplate `style.css` with app-specific globals. Style `App.vue` nav inline. Tighten scoped styles in `RegistrationView.vue`, `AdminView.vue`, and `AlumniRow.vue`. No new dependencies.

**Tech Stack:** Vue 3, Vite, scoped CSS, plain CSS custom properties

---

## File Map

```
frontend/src/
├── style.css                    # Replace entirely — remove Vite boilerplate, add app globals
├── App.vue                      # Add scoped nav styles
├── views/
│   ├── RegistrationView.vue     # Form → white card, tighter spacing, focus ring
│   └── AdminView.vue            # Table → white card wrapper, tighter header
└── components/
    └── AlumniRow.vue            # Table row hover, tighter comparison block
```

---

## Task 1: Replace global stylesheet

**Files:**
- Modify: `frontend/src/style.css`

- [ ] **Step 1: Replace the entire content of `frontend/src/style.css`**

```css
*, *::before, *::after {
  box-sizing: border-box;
}

:root {
  --sans: system-ui, 'Segoe UI', Roboto, sans-serif;
  --bg: #f9fafb;
  --surface: #ffffff;
  --text: #111827;
  --text-muted: #6b7280;
  --border: #e5e7eb;
  --radius: 6px;
  --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
}

body {
  margin: 0;
  font-family: var(--sans);
  font-size: 15px;
  line-height: 1.5;
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}

h1 {
  font-size: 1.4rem;
  font-weight: 600;
  margin: 0 0 1.5rem;
  color: var(--text);
}

p { margin: 0; }

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
```

- [ ] **Step 2: Verify build still passes**

```bash
cd /Users/alma/Projects/RTPP/alumni_platform/frontend
npm run build 2>&1 | tail -3
```

Expected: build succeeds, no errors.

- [ ] **Step 3: Commit**

```bash
cd /Users/alma/Projects/RTPP/alumni_platform
git add frontend/src/style.css
git commit -m "style: replace Vite boilerplate CSS with minimal app globals"
```

---

## Task 2: Style the nav bar

**Files:**
- Modify: `frontend/src/App.vue`

- [ ] **Step 1: Replace the entire content of `frontend/src/App.vue`**

```vue
<template>
  <nav>
    <div class="nav-inner">
      <router-link to="/" class="nav-link">Registracija</router-link>
      <router-link to="/admin" class="nav-link">Admin</router-link>
    </div>
  </nav>
  <main>
    <router-view />
  </main>
</template>

<style scoped>
nav {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 0 1.5rem;
}

.nav-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  gap: 1.5rem;
  height: 48px;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-muted);
  padding-bottom: 2px;
  border-bottom: 2px solid transparent;
  transition: color 0.15s, border-color 0.15s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--text);
  border-bottom-color: var(--text);
}

main {
  flex: 1;
  padding: 2rem 1.5rem;
}
</style>
```

- [ ] **Step 2: Verify build**

```bash
cd /Users/alma/Projects/RTPP/alumni_platform/frontend
npm run build 2>&1 | tail -3
```

Expected: build succeeds.

- [ ] **Step 3: Commit**

```bash
cd /Users/alma/Projects/RTPP/alumni_platform
git add frontend/src/App.vue
git commit -m "style: minimal nav bar with active link underline"
```

---

## Task 3: Polish registration form

**Files:**
- Modify: `frontend/src/views/RegistrationView.vue`

- [ ] **Step 1: Replace the `<style scoped>` block in `frontend/src/views/RegistrationView.vue`**

Find the existing `<style scoped>` block and replace it with:

```vue
<style scoped>
.registration {
  max-width: 520px;
  margin: 0 auto;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 2rem;
}

h1 {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}

.field {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

label {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-muted);
}

input,
select {
  padding: 7px 10px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 0.95rem;
  font-family: inherit;
  color: var(--text);
  background: var(--surface);
  outline: none;
  transition: border-color 0.15s;
}

input:focus,
select:focus {
  border-color: #6b7280;
}

input:disabled,
select:disabled {
  background: var(--bg);
  color: var(--text-muted);
  cursor: not-allowed;
}

button {
  margin-top: 0.5rem;
  padding: 8px 20px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: var(--radius);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s;
}

button:hover:not(:disabled) {
  background: #1d4ed8;
}

button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.success {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  padding: 1rem;
  border-radius: var(--radius);
  color: #166534;
  font-size: 0.9rem;
}

.errors {
  background: #fef2f2;
  border: 1px solid #fecaca;
  padding: 0.75rem 1rem;
  border-radius: var(--radius);
  color: #991b1b;
  font-size: 0.875rem;
}

.errors p {
  margin: 0;
}
</style>
```

- [ ] **Step 2: Verify build**

```bash
cd /Users/alma/Projects/RTPP/alumni_platform/frontend
npm run build 2>&1 | tail -3
```

Expected: build succeeds.

- [ ] **Step 3: Commit**

```bash
cd /Users/alma/Projects/RTPP/alumni_platform
git add frontend/src/views/RegistrationView.vue
git commit -m "style: registration form as white card with clean inputs"
```

---

## Task 4: Polish admin panel and alumni row

**Files:**
- Modify: `frontend/src/views/AdminView.vue`
- Modify: `frontend/src/components/AlumniRow.vue`

- [ ] **Step 1: Replace the `<style scoped>` block in `frontend/src/views/AdminView.vue`**

```vue
<style scoped>
.admin {
  max-width: 1100px;
  margin: 0 auto;
}

h1 {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}

.table-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 10px 14px;
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted);
  background: var(--bg);
  border-bottom: 1px solid var(--border);
}

p {
  color: var(--text-muted);
  font-size: 0.9rem;
}
</style>
```

- [ ] **Step 2: Add the `table-card` wrapper div in `AdminView.vue` template**

Find the `<table v-else>` line and wrap it in a `<div class="table-card">`. The template `v-else` block should become:

```vue
<div v-else class="table-card">
  <table>
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
```

- [ ] **Step 3: Replace the `<style scoped>` block in `frontend/src/components/AlumniRow.vue`**

```vue
<style scoped>
tr {
  border-bottom: 1px solid var(--border);
  transition: background 0.1s;
}

tr:last-child {
  border-bottom: none;
}

tr:hover {
  background: var(--bg);
}

td {
  padding: 10px 14px;
  vertical-align: top;
  font-size: 0.9rem;
  color: var(--text);
}

.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge.pending  { background: #fef3c7; color: #92400e; }
.badge.verified { background: #d1fae5; color: #065f46; }
.badge.rejected { background: #fee2e2; color: #991b1b; }

.actions {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 160px;
}

button {
  padding: 4px 12px;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 500;
  font-family: inherit;
  transition: opacity 0.15s;
}

button:hover { opacity: 0.85; }
button:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-approve { background: #059669; color: white; }
.btn-reject  { background: #dc2626; color: white; }
.btn-check   { background: #2563eb; color: white; }

.check-comparison {
  display: flex;
  gap: 1rem;
  margin-bottom: 8px;
}

.check-comparison > div {
  flex: 1;
}

.check-comparison strong {
  display: block;
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.check-comparison pre {
  font-size: 0.78rem;
  background: var(--bg);
  border: 1px solid var(--border);
  padding: 6px 8px;
  border-radius: var(--radius);
  white-space: pre-wrap;
  margin: 0;
  color: var(--text);
}

.not-found {
  font-size: 0.82rem;
  color: #dc2626;
  font-weight: 600;
}
</style>
```

- [ ] **Step 4: Verify build**

```bash
cd /Users/alma/Projects/RTPP/alumni_platform/frontend
npm run build 2>&1 | tail -3
```

Expected: build succeeds.

- [ ] **Step 5: Commit**

```bash
cd /Users/alma/Projects/RTPP/alumni_platform
git add frontend/src/views/AdminView.vue frontend/src/components/AlumniRow.vue
git commit -m "style: admin table as white card with hover rows and clean comparison block"
```
