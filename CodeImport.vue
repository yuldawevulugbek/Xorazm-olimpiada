<template>
  <div>
    <div class="page-head">
      <div>
        <h2>Code yaratish</h2>
        <p>Excel’dagi har bir o‘quvchi siz yozgan 6 xonali code bilan yaratiladi. O‘quvchi shu code bilan kirsa, Excel’da ko‘rsatilgan fan va darajadan test ishlaydi.</p>
      </div>
      <button class="secondary-btn" :disabled="downloading" @click="downloadTemplate">
        {{ downloading ? 'Yuklanmoqda...' : 'Excel namunasini yuklab olish' }}
      </button>
    </div>

    <div v-if="!canCreateStudents" class="error-box">
      Sizga o‘quvchi yaratish ruxsati berilmagan.
    </div>

    <div v-else class="grid-2">
      <div class="panel">
        <h3>Excel fayl tanlang</h3>
        <div class="upload-box">
          <input type="file" accept=".xlsx" @change="onFileChange" />
          <p>Kerakli ustunlar: Ism familiya, Fan, Daraja, O‘quv markaz, Code. Filial ustuni ixtiyoriy.</p>
        </div>

        <button class="primary-btn" :disabled="!file || loading" @click="upload">
          {{ loading ? 'Yuklanmoqda...' : 'Excelni yuklash va code yaratish' }}
        </button>

        <p v-if="message" class="success-box">{{ message }}</p>
        <p v-if="error" class="error-box">{{ error }}</p>

        <div v-if="rowErrors.length" class="error-box">
          <b>{{ rowErrors.length }} ta qator yaratilmadi:</b>
          <ul>
            <li v-for="item in rowErrors" :key="item.row">
              {{ item.row }}-qator<span v-if="item.full_name"> ({{ item.full_name }})</span>: {{ item.error }}
            </li>
          </ul>
        </div>

        <div v-if="createdStudents.length" class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Ism familiya</th>
                <th>Fan</th>
                <th>Daraja</th>
                <th>O‘quv markaz</th>
                <th>Code</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in createdStudents" :key="student.id">
                <td>{{ student.full_name }}</td>
                <td>{{ student.subject_name }}</td>
                <td>{{ student.level_name }}</td>
                <td>{{ student.center_name }}</td>
                <td><b>{{ student.code }}</b></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="panel">
        <h3>Excel namunasi</h3>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>№</th>
                <th>Ism familiya</th>
                <th>Fan</th>
                <th>Daraja</th>
                <th>O‘quv markaz</th>
                <th>Code</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>Ali Valiyev</td>
                <td>Matematika</td>
                <td>5-sinf</td>
                <td>Al-Aziz Academy</td>
                <td>123456</td>
              </tr>
              <tr>
                <td>2</td>
                <td>Madina Karimova</td>
                <td>IT</td>
                <td>Python</td>
                <td>Al-Aziz Academy</td>
                <td>654321</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3>Testi bor fan va darajalar</h3>
        <div class="code-catalog">
          <div v-for="subject in catalog" :key="subject.id">
            <b>{{ subject.name }}:</b> {{ subject.levels.map(level => level.name).join(', ') }}
          </div>
        </div>
        <p class="hint-text">
          Code 6 xonali son bo‘lishi kerak va boshqa o‘quvchida takrorlanmasligi kerak. Excel code boshidagi 0 ni tushirib yuborsa (012345 → 12345), u avtomatik qaytariladi.
          Xato qatorlar yaratilmaydi va ro‘yxatda sababi bilan ko‘rsatiladi.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '../api/axios'
import { fetchCurrentAdmin, getStoredAdminProfile } from '../utils/auth'

const file = ref(null)
const loading = ref(false)
const downloading = ref(false)
const message = ref('')
const error = ref('')
const rowErrors = ref([])
const createdStudents = ref([])
const catalog = ref([])
const currentAdmin = ref(getStoredAdminProfile())

const canCreateStudents = computed(() => currentAdmin.value ? Boolean(currentAdmin.value.can_create_students) : true)

function onFileChange(event) {
  file.value = event.target.files[0]
  message.value = ''
  error.value = ''
  rowErrors.value = []
  createdStudents.value = []
}

async function upload() {
  if (!file.value) return
  loading.value = true
  message.value = ''
  error.value = ''
  rowErrors.value = []
  createdStudents.value = []

  const formData = new FormData()
  formData.append('file', file.value)

  try {
    const res = await api.post('/students/import-codes/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 0,
    })
    createdStudents.value = res.data.students || []
    rowErrors.value = res.data.errors || []
    message.value = `${res.data.created_count} ta o‘quvchi Excel’dagi code bilan yaratildi.`
  } catch (e) {
    error.value = e.response?.data?.detail || JSON.stringify(e.response?.data || 'Xatolik')
  } finally {
    loading.value = false
  }
}

async function downloadTemplate() {
  downloading.value = true
  try {
    const res = await api.get('/students/code-template/', { responseType: 'blob', timeout: 0 })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'code_yaratish_namuna.xlsx')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } finally {
    downloading.value = false
  }
}

onMounted(async () => {
  try {
    const [me, cat] = await Promise.all([fetchCurrentAdmin(), api.get('/exam/catalog/')])
    currentAdmin.value = me
    catalog.value = cat.data.subjects || []
  } catch {
    // Profil yoki katalog yuklanmasa ham sahifa ishlaydi.
  }
})
</script>
