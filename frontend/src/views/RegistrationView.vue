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
