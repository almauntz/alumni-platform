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
