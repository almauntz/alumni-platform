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
