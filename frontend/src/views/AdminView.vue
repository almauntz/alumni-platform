<template>
  <div class="admin">
    <h1>Admin panel</h1>
    <p v-if="loading">Učitavanje...</p>
    <p v-else-if="!alumniList.length">Nema registrovanih alumni.</p>
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
