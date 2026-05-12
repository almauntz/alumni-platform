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
