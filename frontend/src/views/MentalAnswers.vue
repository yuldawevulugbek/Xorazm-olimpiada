<template>
  <div>
    <div class="page-head">
      <div>
        <h2>Mental javoblari</h2>
        <p>Mental arifmetika ishlagan o‘quvchilar, ularning javoblari va qaysi misol to‘g‘ri/noto‘g‘ri bo‘lgani</p>
      </div>
      <button class="primary-btn" @click="downloadExcel">Mental javoblarini yuklash</button>
    </div>

    <div class="filter-bar">
      <select v-if="mainAdmin" v-model="filters.center" @change="loadMentalResults">
        <option value="">Barchasi</option>
        <option v-for="center in centers" :key="center.id" :value="center.id">{{ center.name }}</option>
      </select>
      <select v-model="filters.branch" :disabled="!mainAdmin" @change="loadMentalResults">
        <option value="">Barcha filiallar</option>
        <option v-for="branch in branches" :key="branch" :value="branch">{{ branch }}</option>
      </select>
      <button class="secondary-btn" @click="loadMentalResults">Yangilash</button>
    </div>

    <div class="panel">
      <div class="table-wrap">
        <table class="mental-admin-table">
          <thead>
            <tr>
              <th>№</th>
              <th>O‘quvchi</th>
              <th>Fan / Daraja</th>
              <th>Markaz / Filial</th>
              <th>Code</th>
              <th>Natija</th>
              <th>Vaqt</th>
              <th>Yechgan javoblari</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(r, i) in mentalResults" :key="r.id">
              <td>{{ i + 1 }}</td>
              <td><b>{{ r.student_full_name }}</b></td>
              <td>{{ r.subject_name }} / {{ r.level_name }}</td>
              <td>{{ r.center_name }} / {{ r.student_branch || '—' }}</td>
              <td>{{ r.student_code }}</td>
              <td>
                <span class="mental-summary-pill">{{ r.correct_count }}/{{ r.total_questions }} · {{ r.percent }}%</span>
              </td>
              <td>{{ formatSeconds(r.spent_seconds) }}</td>
              <td>
                <div class="mental-answer-list mental-answer-list-wide">
                  <span v-for="item in r.mental_answers" :key="item.id" :class="item.is_correct ? 'ok' : 'bad'">
                    {{ item.task_order }}. {{ item.expression }} = {{ item.student_answer ?? '—' }} / {{ item.correct_answer }}
                  </span>
                </div>
              </td>
            </tr>
            <tr v-if="!mentalResults.length">
              <td colspan="8" class="empty-cell">Mental javoblari topilmadi</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import api from '../api/axios'
import { useBranches } from '../composables/useBranches'
import { useCenters } from '../composables/useCenters'
import { fetchCurrentAdmin, getStoredAdminProfile, isMainAdmin } from '../utils/auth'

const mentalResults = ref([])
const currentAdmin = ref(getStoredAdminProfile())
const { branches, loadBranches } = useBranches()
const { centers, loadCenters } = useCenters()
const filters = reactive({ center: '', branch: '' })
const mainAdmin = computed(() => isMainAdmin(currentAdmin.value))

function formatSeconds(seconds) {
  const total = Number(seconds || 0)
  const min = Math.floor(total / 60)
  const sec = total % 60
  return `${min} daq ${sec} sek`
}

async function loadCurrentAdmin() {
  try {
    currentAdmin.value = await fetchCurrentAdmin()
    if (!mainAdmin.value && currentAdmin.value?.branch) filters.branch = currentAdmin.value.branch
  } catch {
    currentAdmin.value = getStoredAdminProfile()
  }
}

async function loadMentalResults() {
  const params = {}
  if (filters.center && mainAdmin.value) params.center = filters.center
  if (filters.branch && mainAdmin.value) params.branch = filters.branch
  const res = await api.get('/results/mental-answers/', { params })
  mentalResults.value = res.data
}

async function downloadExcel() {
  const params = {}
  if (filters.center && mainAdmin.value) params.center = filters.center
  if (filters.branch && mainAdmin.value) params.branch = filters.branch
  const res = await api.get('/results/mental-answers-export/', { params, responseType: 'blob', timeout: 0 })
  const url = window.URL.createObjectURL(new Blob([res.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'mental_javoblari.xlsx')
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

onMounted(async () => {
  await loadCurrentAdmin()
  await Promise.all([loadBranches(), loadCenters()])
  await loadMentalResults()
})
</script>
