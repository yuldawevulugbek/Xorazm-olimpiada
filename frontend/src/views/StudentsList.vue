<template>
  <div>
    <div class="page-head">
      <div>
        <h2>Yaratilgan o‘quvchilar</h2>
        <p>Code, test holati, filial, natijalar va fan/darajalarni nazorat qilish</p>
      </div>
      <div class="page-actions">
        <button class="secondary-btn" :disabled="downloading" @click="downloadStudentsExcel">
          {{ downloading ? 'Yuklanmoqda...' : 'Excel yuklash' }}
        </button>
        <RouterLink v-if="mainAdmin" to="/admin/students/create" class="primary-btn">+ O‘quvchi yaratish</RouterLink>
      </div>
    </div>

    <div class="filter-bar">
      <input v-model="filters.q" placeholder="Ism, familya yoki code qidirish" @input="loadStudents" />
      <select v-model="filters.status" @change="loadStudents">
        <option value="">Barcha status</option>
        <option value="not_started">Ishlamagan</option>
        <option value="in_progress">Ishlayapti</option>
        <option value="completed">Ishlab bo‘ldi</option>
      </select>
      <select v-if="mainAdmin" v-model="filters.center" @change="loadStudents">
        <option value="">Barchasi</option>
        <option v-for="center in centers" :key="center.id" :value="center.id">{{ center.name }}</option>
      </select>
      <select v-model="filters.branch" :disabled="!mainAdmin" @change="loadStudents">
        <option value="">Barcha filiallar</option>
        <option v-for="branch in branches" :key="branch" :value="branch">{{ branch }}</option>
      </select>
      <button class="secondary-btn" @click="loadStudents">Yangilash</button>
    </div>

    <div v-if="mainAdmin" class="filter-bar">
      <input v-model="newBranchName" placeholder="Yangi filial nomi" />
      <button class="secondary-btn" :disabled="addingBranch" @click="createBranch">
        {{ addingBranch ? 'Qo‘shilmoqda...' : '+ Filial qo‘shish' }}
      </button>
      <span v-if="branchMessage" class="success-text">{{ branchMessage }}</span>
      <span v-if="branchError" class="error-text">{{ branchError }}</span>
    </div>

    <div v-if="!canManageStudents" class="success-box">
      Siz filial adminisiz: o‘quvchilarni ko‘rishingiz mumkin, lekin tahrirlash yoki o‘chirish mumkin emas.
    </div>

    <div v-if="canManageStudents" class="bulk-action-bar">
      <div>
        <b>{{ selectedCount }}</b> ta o‘quvchi tanlandi
        <span v-if="students.length">/ {{ students.length }} ta ko‘rinib turibdi</span>
      </div>
      <div class="bulk-action-buttons">
        <button class="secondary-btn" type="button" :disabled="!students.length" @click="toggleAllVisible">
          {{ allVisibleSelected ? 'Tanlovni bekor qilish' : 'Hamma ko‘rinib turganlarni belgilash' }}
        </button>
        <button class="danger-btn" type="button" :disabled="!selectedCount || bulkDeleting" @click="deleteSelectedStudents">
          {{ bulkDeleting ? 'O‘chirilmoqda...' : 'Tanlanganlarni o‘chirish' }}
        </button>
      </div>
      <p v-if="bulkDeleteError" class="error-text">{{ bulkDeleteError }}</p>
    </div>

    <div class="panel">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th v-if="canManageStudents" class="select-col">
                <input type="checkbox" :checked="allVisibleSelected" :disabled="!students.length" @change="toggleAllVisible" />
              </th>
              <th>№</th>
              <th>O‘quvchi</th>
              <th>Fan</th>
              <th>Daraja/Sinf</th>
              <th>Yosh</th>
              <th>O‘quv markaz</th>
              <th>Filial</th>
              <th>Code</th>
              <th>Status</th>
              <th>Natija</th>
              <th>Sarflagan vaqt</th>
              <th v-if="canManageStudents">Amal</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(s, i) in students" :key="s.id">
              <td v-if="canManageStudents" class="select-col">
                <input v-model="selectedStudentIds" type="checkbox" :value="s.id" />
              </td>
              <td>{{ i + 1 }}</td>
              <td>
                <b>{{ s.full_name }}</b>
                <small v-if="s.is_self_registered" class="self-reg-tag">o‘zi ro‘yxatdan o‘tgan</small>
              </td>
              <td>{{ s.subject_name }}</td>
              <td>{{ s.level_name }}</td>
              <td>{{ s.age || '—' }}</td>
              <td>{{ s.center_name }}</td>
              <td>{{ s.branch }}</td>
              <td>
                <div class="code-copy-cell">
                  <button class="code-pill" :title="`${s.code} codeni copy qilish`" @click="copyCode(s.code)">
                    {{ s.code }}
                  </button>
                  <button class="copy-code-btn" :class="{ copied: copiedCode === s.code }" @click="copyCode(s.code)">
                    {{ copiedCode === s.code ? 'Copy qilindi' : 'Copy' }}
                  </button>
                </div>
              </td>
              <td><StatusBadge :status="s.status" /></td>
              <td>
                <span v-if="s.correct_count !== null && s.correct_count !== undefined">
                  {{ s.correct_count }}/{{ s.total_questions }} ta / {{ s.percent }}%
                </span>
                <span v-else>—</span>
              </td>
              <td>{{ s.spent_seconds !== null && s.spent_seconds !== undefined ? formatSeconds(s.spent_seconds) : '—' }}</td>
              <td v-if="canManageStudents">
                <div class="student-row-actions">
                  <button class="secondary-btn small-action-btn" @click="openEditModal(s)">
                    Tahrirlash
                  </button>
                  <button class="danger-btn small-action-btn" @click="openDeleteModal(s)">
                    O‘chirish
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!students.length">
              <td :colspan="canManageStudents ? 13 : 11" class="empty-cell">O‘quvchi topilmadi</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="editModalOpen" class="modal-backdrop" @click.self="closeEditModal">
      <div class="edit-student-modal">
        <div class="modal-head">
          <div>
            <h3>O‘quvchini tahrirlash</h3>
            <p>{{ editingStudent?.full_name }}</p>
          </div>
          <button class="modal-close-btn" @click="closeEditModal">×</button>
        </div>

        <form class="form-grid" @submit.prevent="saveStudentEdit">
          <label>
            Fan
            <select v-model="editForm.subject" required @change="onEditSubjectChange">
              <option value="">Fan tanlang</option>
              <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                {{ subject.name }}
              </option>
            </select>
          </label>

          <label>
            Daraja/Sinf
            <select v-model="editForm.level" required>
              <option value="">Daraja/Sinf tanlang</option>
              <option v-for="level in editFilteredLevels" :key="level.id" :value="level.id">
                {{ level.name }} — {{ level.duration_minutes }} daqiqa
              </option>
            </select>
          </label>

          <label>
            Filial
            <select v-model="editForm.branch" required>
              <option value="">Filial tanlang</option>
              <option v-for="branch in branches" :key="branch" :value="branch">{{ branch }}</option>
            </select>
          </label>

          <p v-if="editError" class="error-box">{{ editError }}</p>

          <div class="modal-actions">
            <button type="button" class="secondary-btn" @click="closeEditModal">Bekor qilish</button>
            <button class="primary-btn" :disabled="savingEdit">
              {{ savingEdit ? 'Saqlanmoqda...' : 'Saqlash' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="deleteModalOpen" class="modal-backdrop" @click.self="closeDeleteModal">
      <div class="edit-student-modal delete-confirm-modal">
        <div class="modal-head">
          <div>
            <h3>O‘quvchini o‘chirish</h3>
            <p>{{ deletingStudent?.full_name }}</p>
          </div>
          <button class="modal-close-btn" @click="closeDeleteModal">×</button>
        </div>

        <div class="delete-warning-box">
          <b>O‘chirishni xohlaysizmi?</b>
          <span>Ha bosilganda o‘quvchi, natijasi va javoblari o‘chiriladi.</span>
        </div>

        <p v-if="deleteError" class="error-box">{{ deleteError }}</p>

        <div class="modal-actions">
          <button type="button" class="secondary-btn" @click="closeDeleteModal">Yo‘q</button>
          <button class="danger-btn" :disabled="deleting" @click="deleteStudent">
            {{ deleting ? 'O‘chirilmoqda...' : 'Ha, o‘chirish' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import api from '../api/axios'
import StatusBadge from '../components/StatusBadge.vue'
import { useBranches } from '../composables/useBranches'
import { useCenters } from '../composables/useCenters'
import { fetchCurrentAdmin, getStoredAdminProfile, isMainAdmin } from '../utils/auth'

const students = ref([])
const subjects = ref([])
const levels = ref([])
const downloading = ref(false)
const currentAdmin = ref(getStoredAdminProfile())
const { branches, loadBranches, addBranch } = useBranches()
const { centers, loadCenters } = useCenters()
const newBranchName = ref('')
const addingBranch = ref(false)
const branchMessage = ref('')
const branchError = ref('')

const editModalOpen = ref(false)
const editingStudent = ref(null)
const savingEdit = ref(false)
const editError = ref('')

const deleteModalOpen = ref(false)
const deletingStudent = ref(null)
const deleting = ref(false)
const deleteError = ref('')
const selectedStudentIds = ref([])
const bulkDeleting = ref(false)
const bulkDeleteError = ref('')
const copiedCode = ref('')
let copiedTimer = null

const filters = reactive({ q: '', status: '', center: '', branch: '' })
const editForm = reactive({ subject: '', level: '', branch: '' })

const SUBJECT_ORDER = ['English', 'Koreys tili', 'Rus tili', 'Arab tili', 'Matematika', 'IT', 'Kampyuter', 'Biologiya', 'Hamshiralik', 'Mental arifmetika']
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
const canManageStudents = computed(() => Boolean(currentAdmin.value?.can_edit_students && currentAdmin.value?.can_delete_students))
const selectedCount = computed(() => selectedStudentIds.value.length)
const visibleStudentIds = computed(() => students.value.map(student => student.id))
const allVisibleSelected = computed(() => {
  const visibleIds = visibleStudentIds.value
  return Boolean(visibleIds.length) && visibleIds.every(id => selectedStudentIds.value.includes(id))
})

const editFilteredLevels = computed(() => {
  const list = levels.value.filter(level => String(level.subject) === String(editForm.subject))
  const selectedSubject = subjects.value.find(subject => String(subject.id) === String(editForm.subject))

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



function formatSeconds(seconds) {
  const total = Number(seconds || 0)
  const min = Math.floor(total / 60)
  const sec = total % 60
  return `${min} daq ${sec} sek`
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
    await loadStudents()
  } catch (e) {
    branchError.value = e.message || JSON.stringify(e.response?.data || 'Filial qo‘shishda xatolik')
  } finally {
    addingBranch.value = false
  }
}

async function loadStudents() {
  const params = {}
  if (filters.q) params.q = filters.q
  if (filters.status) params.status = filters.status
  if (filters.center && mainAdmin.value) params.center = filters.center
  if (filters.branch && mainAdmin.value) params.branch = filters.branch
  const res = await api.get('/students/', { params })
  students.value = res.data
  selectedStudentIds.value = selectedStudentIds.value.filter(id => students.value.some(student => student.id === id))
}

function normalizeApiList(data) {
  return Array.isArray(data) ? data : (data?.results || [])
}

async function loadOptions() {
  const [subjectsRes, levelsRes] = await Promise.all([
    api.get('/subjects/'),
    api.get('/levels/'),
  ])
  subjects.value = sortByKnownOrder(normalizeApiList(subjectsRes.data), SUBJECT_ORDER)
  levels.value = normalizeApiList(levelsRes.data)
}

async function loadCurrentAdmin() {
  try {
    currentAdmin.value = await fetchCurrentAdmin()
    if (!mainAdmin.value && currentAdmin.value?.branch) filters.branch = currentAdmin.value.branch
  } catch {
    currentAdmin.value = getStoredAdminProfile()
  }
}

function toggleAllVisible() {
  const visibleIds = visibleStudentIds.value
  if (!visibleIds.length) return
  if (allVisibleSelected.value) {
    selectedStudentIds.value = selectedStudentIds.value.filter(id => !visibleIds.includes(id))
  } else {
    selectedStudentIds.value = Array.from(new Set([...selectedStudentIds.value, ...visibleIds]))
  }
}

async function deleteSelectedStudents() {
  if (!selectedStudentIds.value.length) return
  const ok = window.confirm(`${selectedStudentIds.value.length} ta o‘quvchini o‘chirishni xohlaysizmi? Natijalari va javoblari ham o‘chadi.`)
  if (!ok) return

  bulkDeleting.value = true
  bulkDeleteError.value = ''
  try {
    await api.post('/students/bulk-delete/', { ids: selectedStudentIds.value })
    selectedStudentIds.value = []
    await loadStudents()
  } catch (e) {
    bulkDeleteError.value = JSON.stringify(e.response?.data || 'Tanlangan o‘quvchilarni o‘chirishda xatolik.')
  } finally {
    bulkDeleting.value = false
  }
}

function openEditModal(student) {
  editingStudent.value = student
  editForm.subject = student.subject
  editForm.level = student.level
  editForm.branch = student.branch || ''
  editError.value = ''
  editModalOpen.value = true
}

function closeEditModal() {
  editModalOpen.value = false
  editingStudent.value = null
  editError.value = ''
  editForm.subject = ''
  editForm.level = ''
  editForm.branch = ''
}

function onEditSubjectChange() {
  editForm.level = ''
}

async function saveStudentEdit() {
  if (!editingStudent.value) return

  savingEdit.value = true
  editError.value = ''

  try {
    const res = await api.patch(`/students/${editingStudent.value.id}/`, {
      subject: editForm.subject,
      level: editForm.level,
      branch: editForm.branch,
    })

    const index = students.value.findIndex(student => student.id === editingStudent.value.id)
    if (index !== -1) students.value[index] = res.data

    closeEditModal()
  } catch (e) {
    editError.value = JSON.stringify(e.response?.data || 'Tahrirlashda xatolik yuz berdi.')
  } finally {
    savingEdit.value = false
  }
}

function openDeleteModal(student) {
  deletingStudent.value = student
  deleteError.value = ''
  deleteModalOpen.value = true
}

function closeDeleteModal() {
  deleteModalOpen.value = false
  deletingStudent.value = null
  deleteError.value = ''
}

async function deleteStudent() {
  if (!deletingStudent.value) return

  deleting.value = true
  deleteError.value = ''

  try {
    await api.delete(`/students/${deletingStudent.value.id}/`)
    students.value = students.value.filter(student => student.id !== deletingStudent.value.id)
    selectedStudentIds.value = selectedStudentIds.value.filter(id => id !== deletingStudent.value.id)
    closeDeleteModal()
  } catch (e) {
    deleteError.value = JSON.stringify(e.response?.data || 'O‘chirishda xatolik yuz berdi.')
  } finally {
    deleting.value = false
  }
}

async function downloadStudentsExcel() {
  downloading.value = true
  try {
    const params = {}
    if (filters.center && mainAdmin.value) params.center = filters.center
    if (filters.branch && mainAdmin.value) params.branch = filters.branch
    const res = await api.get('/students/export-excel/', { params, responseType: 'blob', timeout: 0 })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'barcha_oquvchilar.xlsx')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } finally {
    downloading.value = false
  }
}

async function copyCode(code) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(code)
    } else {
      const textarea = document.createElement('textarea')
      textarea.value = code
      textarea.setAttribute('readonly', '')
      textarea.style.position = 'fixed'
      textarea.style.left = '-9999px'
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      textarea.remove()
    }

    copiedCode.value = code
    if (copiedTimer) clearTimeout(copiedTimer)
    copiedTimer = setTimeout(() => {
      copiedCode.value = ''
      copiedTimer = null
    }, 1600)
  } catch (e) {
    alert('Code copy bo‘lmadi. Iltimos, code ustidan qo‘lda belgilang va Ctrl + C bosing.')
  }
}

onMounted(async () => {
  await loadCurrentAdmin()
  await Promise.all([loadStudents(), loadOptions(), loadBranches(), loadCenters()])
})
</script>
