<template>
  <div>
    <div class="page-head">
      <div>
        <h2>Dashboard</h2>
        <p>Umumiy holat va statistikalar</p>
      </div>
      <button class="secondary-btn" @click="loadData">Yangilash</button>
    </div>

    <div class="stats-grid">
      <div v-tilt="10" class="stat-card dark"><span>Jami o‘quvchilar</span><strong>{{ students.length }}</strong></div>
      <div v-tilt="10" class="stat-card red"><span>Ishlamagan</span><strong>{{ countByStatus('not_started') }}</strong></div>
      <div v-tilt="10" class="stat-card yellow"><span>Ishlayapti</span><strong>{{ countByStatus('in_progress') }}</strong></div>
      <div v-tilt="10" class="stat-card green"><span>Ishlab bo‘ldi</span><strong>{{ countByStatus('completed') }}</strong></div>
      <div v-tilt="10" class="stat-card blue"><span>Natijalar</span><strong>{{ results.length }}</strong></div>
      <div v-tilt="10" class="stat-card purple"><span>O‘rtacha foiz</span><strong>{{ averagePercent }}%</strong></div>
    </div>

    <div class="panel mt">
      <h3>Oxirgi natijalar</h3>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>O‘quvchi</th><th>Fan</th><th>Daraja/Sinf</th><th>To‘g‘ri</th><th>Foiz</th><th>Vaqt</th></tr>
          </thead>
          <tbody>
            <tr v-for="r in results.slice(0, 8)" :key="r.id">
              <td>{{ r.student_full_name }}</td>
              <td>{{ r.subject_name }}</td>
              <td>{{ r.level_name }}</td>
              <td>{{ r.correct_count }}/{{ r.total_questions }}</td>
              <td>{{ r.percent }}%</td>
              <td>{{ formatSeconds(r.spent_seconds) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '../api/axios'

const students = ref([])
const results = ref([])


function formatSeconds(seconds) {
  const total = Number(seconds || 0)
  const min = Math.floor(total / 60)
  const sec = total % 60
  return `${min} daq ${sec} sek`
}

function countByStatus(status) {
  return students.value.filter(s => s.status === status).length
}

const averagePercent = computed(() => {
  if (!results.value.length) return 0
  const avg = results.value.reduce((sum, r) => sum + Number(r.percent || 0), 0) / results.value.length
  return avg.toFixed(1)
})

async function loadData() {
  const [studentsRes, resultsRes] = await Promise.all([api.get('/students/'), api.get('/results/')])
  students.value = studentsRes.data
  results.value = resultsRes.data
}

onMounted(loadData)
</script>
