<template>
  <div>
    <div class="page-head">
      <div>
        <h2>Natijalar</h2>
        <p>Test va mental arifmetika natijalari: o‘quvchi, fan, daraja, nechtadan nechta to‘g‘ri va foiz</p>
      </div>
      <button class="primary-btn" @click="downloadExcel">Natijalarni Excelga yuklash</button>
    </div>

    <div class="filter-bar">
      <select v-if="mainAdmin" v-model="filters.center" @change="loadResults">
        <option value="">Barchasi</option>
        <option v-for="center in centers" :key="center.id" :value="center.id">{{ center.name }}</option>
      </select>
      <select v-model="filters.branch" :disabled="!mainAdmin" @change="loadResults">
        <option value="">Barcha filiallar</option>
        <option v-for="branch in branches" :key="branch" :value="branch">{{ branch }}</option>
      </select>
      <button class="secondary-btn" @click="loadResults">Yangilash</button>
    </div>

    <div v-if="mainAdmin" class="filter-bar">
      <input v-model="newBranchName" placeholder="Yangi filial nomi" />
      <button class="secondary-btn" :disabled="addingBranch" @click="createBranch">
        {{ addingBranch ? 'Qo‘shilmoqda...' : '+ Filial qo‘shish' }}
      </button>
      <span v-if="branchMessage" class="success-text">{{ branchMessage }}</span>
      <span v-if="branchError" class="error-text">{{ branchError }}</span>
    </div>

    <div class="panel">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>№</th>
              <th>O‘quvchi</th>
              <th>Fan</th>
              <th>Daraja/Sinf</th>
              <th>Version</th>
              <th>O‘quv markaz</th>
              <th>Filial</th>
              <th>Code</th>
              <th>Nechta to‘g‘ri</th>
              <th>Foiz</th>
              <th>Vaqt</th>
              <th>Javoblar</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(r, i) in results" :key="r.id">
              <td>{{ i + 1 }}</td>
              <td><b>{{ r.student_full_name }}</b></td>
              <td>{{ r.subject_name }}</td>
              <td>{{ r.level_name }}</td>
              <td>{{ r.student_selected_version ? `Version ${r.student_selected_version}` : '—' }}</td>
              <td>{{ r.center_name }}</td>
              <td>{{ r.student_branch }}</td>
              <td>{{ r.student_code }}</td>
              <td><b>{{ r.correct_count }}/{{ r.total_questions }}</b></td>
              <td>{{ r.percent }}%</td>
              <td>{{ formatSeconds(r.spent_seconds) }}</td>
              <td>
                <button class="secondary-btn small-action-btn" @click="openResultDetails(r)">
                  Javoblarni ko‘rish
                </button>
              </td>
            </tr>
            <tr v-if="!results.length">
              <td colspan="12" class="empty-cell">Natija topilmadi</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="selectedResult" class="modal-backdrop" @click.self="closeResultDetails">
      <div class="result-detail-modal">
        <div class="modal-head">
          <div>
            <h3>{{ selectedResult.student_full_name }} javoblari</h3>
            <p>
              {{ selectedResult.subject_name }} • {{ selectedResult.level_name }}
              <span v-if="selectedResult.student_selected_version"> • Version {{ selectedResult.student_selected_version }}</span>
            </p>
          </div>
          <button type="button" class="modal-close-btn" @click="closeResultDetails">×</button>
        </div>

        <div class="result-detail-summary">
          <div>
            <span>Code</span>
            <b>{{ selectedResult.student_code }}</b>
          </div>
          <div>
            <span>Natija</span>
            <b>{{ selectedResult.correct_count }}/{{ selectedResult.total_questions }}</b>
          </div>
          <div>
            <span>Foiz</span>
            <b>{{ selectedResult.percent }}%</b>
          </div>
          <div>
            <span>Vaqt</span>
            <b>{{ formatSeconds(selectedResult.spent_seconds) }}</b>
          </div>
        </div>

        <div v-if="isMentalResult" class="answers-list">
          <div v-for="task in mentalAnswers" :key="task.id" class="answer-detail-card" :class="task.is_correct ? 'answer-ok' : 'answer-bad'">
            <div class="answer-card-head">
              <strong>{{ task.task_order }}-misol</strong>
              <span>{{ task.is_correct ? 'To‘g‘ri' : 'Noto‘g‘ri' }}</span>
            </div>
            <p class="question-text">{{ task.expression }}</p>
            <div class="answer-meta-grid">
              <div>
                <span>O‘quvchi javobi</span>
                <b>{{ task.student_answer ?? 'Belgilanmagan' }}</b>
              </div>
              <div>
                <span>To‘g‘ri javob</span>
                <b>{{ task.correct_answer }}</b>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="answers-list">
          <div v-for="(answer, index) in normalAnswers" :key="answer.id" class="answer-detail-card" :class="answer.is_correct ? 'answer-ok' : 'answer-bad'">
            <div class="answer-card-head">
              <strong>{{ index + 1 }}-savol</strong>
              <span>{{ answer.is_correct ? 'To‘g‘ri' : 'Noto‘g‘ri' }}</span>
            </div>
            <p class="question-text">{{ answer.question_text }}</p>

            <div class="option-review-list">
              <div v-for="letter in optionLetters" :key="letter" :class="optionClass(answer, letter)">
                <b>{{ letter }}</b>
                <span>{{ optionText(answer, letter) }}</span>
              </div>
            </div>

            <div class="answer-meta-grid">
              <div>
                <span>O‘quvchi belgilagan</span>
                <b>{{ answerLabel(answer.selected_answer) }}</b>
              </div>
              <div>
                <span>To‘g‘ri javob</span>
                <b>{{ answerLabel(answer.correct_answer) }}</b>
              </div>
            </div>
          </div>

          <div v-if="!normalAnswers.length" class="empty-cell">
            Bu natija uchun savollar bo‘yicha javoblar topilmadi.
          </div>
        </div>

        <div class="modal-actions">
          <button class="secondary-btn" @click="closeResultDetails">Yopish</button>
        </div>
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

const results = ref([])
const selectedResult = ref(null)
const currentAdmin = ref(getStoredAdminProfile())
const { branches, loadBranches, addBranch } = useBranches()
const { centers, loadCenters } = useCenters()
const newBranchName = ref('')
const addingBranch = ref(false)
const branchMessage = ref('')
const branchError = ref('')
const filters = reactive({ center: '', branch: '' })
const mainAdmin = computed(() => isMainAdmin(currentAdmin.value))
const optionLetters = ['A', 'B', 'C', 'D']
const normalAnswers = computed(() => selectedResult.value?.answers || [])
const mentalAnswers = computed(() => selectedResult.value?.mental_answers || [])
const isMentalResult = computed(() => mentalAnswers.value.length > 0)

function formatSeconds(seconds) {
  const total = Number(seconds || 0)
  const min = Math.floor(total / 60)
  const sec = total % 60
  return `${min} daq ${sec} sek`
}

function answerLabel(value) {
  return value ? value : 'Belgilanmagan'
}

function optionText(answer, letter) {
  return answer?.[`option_${letter.toLowerCase()}`] || ''
}

function optionClass(answer, letter) {
  return {
    'option-review-item': true,
    'student-selected': answer?.selected_answer === letter,
    'correct-option': answer?.correct_answer === letter,
  }
}

function openResultDetails(result) {
  selectedResult.value = result
}

function closeResultDetails() {
  selectedResult.value = null
}

async function createBranch() {
  branchMessage.value = ''
  branchError.value = ''
  addingBranch.value = true
  try {
    const savedName = await addBranch(newBranchName.value)
    filters.branch = savedName
    newBranchName.value = ''
    branchMessage.value = 'Filial qo‘shildi.'
    await Promise.all([loadBranches(), loadCenters()])
    await loadResults()
  } catch (e) {
    branchError.value = e.message || JSON.stringify(e.response?.data || 'Filial qo‘shishda xatolik')
  } finally {
    addingBranch.value = false
  }
}

async function loadCurrentAdmin() {
  try {
    currentAdmin.value = await fetchCurrentAdmin()
    if (!mainAdmin.value && currentAdmin.value?.branch) filters.branch = currentAdmin.value.branch
  } catch {
    currentAdmin.value = getStoredAdminProfile()
  }
}

async function loadResults() {
  const params = {}
  if (filters.center && mainAdmin.value) params.center = filters.center
  if (filters.branch && mainAdmin.value) params.branch = filters.branch
  const res = await api.get('/results/', { params })
  results.value = res.data
}

async function downloadExcel() {
  const params = {}
  if (filters.center && mainAdmin.value) params.center = filters.center
  if (filters.branch && mainAdmin.value) params.branch = filters.branch
  const res = await api.get('/results/export-excel/', { params, responseType: 'blob', timeout: 0 })
  const url = window.URL.createObjectURL(new Blob([res.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'olimpiada_natijalari_filiallar.xlsx')
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

onMounted(async () => {
  await loadCurrentAdmin()
  await Promise.all([loadBranches(), loadCenters()])
  await loadResults()
})
</script>
