<template>
  <div>
    <div class="page-head">
      <div>
        <h2>O‘quvchi yaratish</h2>
        <p>O‘quvchiga fan, daraja/sinf, o‘quv markaz va filial biriktiriladi. Kichik admin faqat o‘z markaziga o‘quvchi qo‘sha oladi.</p>
      </div>
      <RouterLink v-if="canCreateStudents" class="primary-btn" to="/admin/students/import">Excel orqali yuklash</RouterLink>
    </div>

    <div v-if="!canCreateStudents" class="error-box">
      Sizga o‘quvchi yaratish ruxsati berilmagan.
    </div>

    <div v-else class="grid-2">
      <div class="panel">
        <h3>Yangi o‘quvchi</h3>
        <form @submit.prevent="createStudent" class="form-grid">
          <label>
            O‘quvchi Ism Familyasi
            <input v-model="form.full_name" placeholder="Masalan: Aliyev Vali" required />
          </label>

          <label>Fan
            <select v-model="form.subject" required @change="filterLevels">
              <option value="">Tanlang</option>
              <option v-for="s in subjects" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </label>

          <label>Daraja/Sinf/Sinf
            <select v-model="form.level" required>
              <option value="">Tanlang</option>
              <option v-for="l in filteredLevels" :key="l.id" :value="l.id">
                {{ l.name }} — {{ l.duration_minutes }} daqiqa
              </option>
            </select>
          </label>

          <label v-if="mainAdmin">O‘quv markaz
            <select v-model="form.center" required>
              <option value="">O‘quv markaz tanlang</option>
              <option v-for="center in centers" :key="center.id" :value="center.id">{{ center.name }}</option>
            </select>
          </label>
          <div v-else class="locked-center-box">
            <span>O‘quv markaz</span>
            <b>{{ currentAdmin?.center_name || currentAdmin?.assigned_center_name }}</b>
          </div>


          <label>Filial
            <select v-model="form.branch" required>
              <option value="">Filial tanlang</option>
              <option v-for="branch in branches" :key="branch" :value="branch">{{ branch }}</option>
            </select>
          </label>

          <div v-if="mainAdmin" class="inline-create-box">
            <label>Yangi filial qo‘shish
              <input v-model="newBranchName" placeholder="Masalan: Yangiyo‘l" />
            </label>
            <button type="button" class="secondary-btn" :disabled="addingBranch" @click="createBranch">
              {{ addingBranch ? 'Qo‘shilmoqda...' : '+ Filial qo‘shish' }}
            </button>
          </div>

          <button class="primary-btn">Yaratish</button>
        </form>
        <p v-if="error" class="error-box">{{ error }}</p>
      </div>

      <div class="panel result-panel" v-if="createdStudent">
        <h3>O‘quvchi yaratildi</h3>
        <div class="success-code">{{ createdStudent.code }}</div>
        <p><b>{{ createdStudent.full_name }}</b></p>
        <p>{{ createdStudent.subject_name }} / {{ createdStudent.level_name }}</p>
        <p>{{ createdStudent.center_name }} / {{ createdStudent.branch }}</p>
        <button class="secondary-btn" @click="copyCode(createdStudent.code)">Code copy qilish</button>
        <RouterLink class="primary-btn block-link" to="/admin/students">Yaratilgan o‘quvchilarga o‘tish</RouterLink>
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

const subjects = ref([])
const levels = ref([])
const createdStudent = ref(null)
const error = ref('')
const currentAdmin = ref(getStoredAdminProfile())
const { branches, loadBranches, addBranch } = useBranches()
const { centers, loadCenters } = useCenters()
const newBranchName = ref('')
const addingBranch = ref(false)
const form = reactive({ full_name: '', subject: '', level: '', center: '', branch: '' })

const SUBJECT_ORDER = ['Mental arifmetika']
const KOREYS_LEVEL_ORDER = ['Koreys tili 1', 'Koreys tili 2']

function sortByKnownOrder(items, order) {
  return [...items].sort((a, b) => {
    const ai = order.indexOf(a.name)
    const bi = order.indexOf(b.name)
    if (ai === -1 && bi === -1) return a.name.localeCompare(b.name)
    if (ai === -1) return 1
    if (bi === -1) return -1
    return ai - bi
  })
}

const mainAdmin = computed(() => isMainAdmin(currentAdmin.value))
const canCreateStudents = computed(() => Boolean(currentAdmin.value?.can_create_students))

const filteredLevels = computed(() => {
  const list = levels.value.filter(l => String(l.subject) === String(form.subject))
  const selectedSubject = subjects.value.find(s => String(s.id) === String(form.subject))
  if (selectedSubject?.name === 'IT') {
    const order = ['Frontend 1', 'Frontend 2', 'Backend 1', 'Backend 2']
    return [...list].sort((a, b) => order.indexOf(a.name) - order.indexOf(b.name))
  }
  if (selectedSubject?.name === 'English') {
    const order = ['Starter 1', 'Beginner 1', 'Beginner 2', 'Beginner 3', 'Elementary 1', 'Elementary 2', 'Elementary 3', 'Pre-Intermediate 1', 'Pre-Intermediate 2', 'Pre-Intermediate 3', 'Intermediate 1', 'Intermediate 2', 'Intermediate 3', 'Upper-Intermediate 1', 'Advanced 1', 'IELTS']
    return [...list].sort((a, b) => order.indexOf(a.name) - order.indexOf(b.name))
  }
  if (selectedSubject?.name === 'Koreys tili') {
    return sortByKnownOrder(list, KOREYS_LEVEL_ORDER)
  }

  return list
})

function filterLevels() {
  form.level = ''
}

function splitFullName(fullName) {
  const parts = String(fullName || '').trim().split(/\s+/).filter(Boolean)
  if (parts.length < 2) {
    throw new Error('O‘quvchi ism va familyasini to‘liq kiriting.')
  }
  return {
    first_name: parts[0],
    last_name: parts.slice(1).join(' '),
  }
}

function normalizeApiList(data) {
  return Array.isArray(data) ? data : (data?.results || [])
}

async function loadOptions() {
  const [subjectsRes, levelsRes] = await Promise.all([api.get('/subjects/'), api.get('/levels/')])
  subjects.value = sortByKnownOrder(normalizeApiList(subjectsRes.data), SUBJECT_ORDER)
  levels.value = normalizeApiList(levelsRes.data)
}

async function loadCurrentAdmin() {
  try {
    currentAdmin.value = await fetchCurrentAdmin()
    if (!mainAdmin.value && currentAdmin.value?.assigned_center) {
      form.center = currentAdmin.value.assigned_center
    }
    if (!mainAdmin.value && currentAdmin.value?.branch) {
      form.branch = currentAdmin.value.branch
    }
  } catch {
    currentAdmin.value = getStoredAdminProfile()
  }
}


async function createBranch() {
  error.value = ''
  addingBranch.value = true
  try {
    const savedName = await addBranch(newBranchName.value)
    form.branch = savedName
    newBranchName.value = ''
  } catch (e) {
    error.value = e.message || JSON.stringify(e.response?.data || 'Filial qo‘shishda xatolik')
  } finally {
    addingBranch.value = false
  }
}

async function createStudent() {
  error.value = ''
  try {
    if (!canCreateStudents.value) throw new Error('Sizga o‘quvchi yaratish ruxsati yo‘q.')
    const { first_name, last_name } = splitFullName(form.full_name)
    const centerId = mainAdmin.value ? form.center : currentAdmin.value?.assigned_center
    if (!centerId) throw new Error('O‘quv markaz tanlanmagan.')

    const payload = {
      first_name,
      last_name,
      subject: form.subject,
      level: form.level,
      center: centerId,
      branch: form.branch,
    }
    const res = await api.post('/students/', payload)
    createdStudent.value = res.data
    Object.assign(form, {
      full_name: '',
      subject: '',
      level: '',
      center: mainAdmin.value ? '' : currentAdmin.value?.assigned_center,
      branch: !mainAdmin.value && currentAdmin.value?.branch ? currentAdmin.value.branch : '',
    })
  } catch (e) {
    error.value = e.message || JSON.stringify(e.response?.data || 'Xatolik')
  }
}

async function copyCode(code) {
  await navigator.clipboard.writeText(code)
}

onMounted(async () => {
  await Promise.all([loadOptions(), loadCurrentAdmin(), loadBranches(), loadCenters()])
})
</script>
