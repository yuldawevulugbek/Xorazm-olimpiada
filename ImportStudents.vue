<template>
  <div>
    <div class="page-head">
      <div>
        <h2>O‘quvchilarni Excel orqali yuklash</h2>
        <p>Excel faylda nechta o‘quvchi bo‘lsa, hammasiga avtomatik random code beriladi.</p>
      </div>
    </div>

    <div class="grid-2">
      <div class="panel">
        <h3>Excel fayl tanlang</h3>
        <div class="upload-box">
          <input type="file" accept=".xlsx,.xls" @change="onFileChange" />
          <p>Kerakli ustunlar: №, Ism familya, Fan, Daraja/Sinf, O'quv markaz, Filial. Filial Excelda qanday yozilsa, avtomatik qo‘shiladi.</p>
        </div>

        <button class="primary-btn" :disabled="!file || loading" @click="upload">
          {{ loading ? 'Yuklanmoqda...' : 'Excelni yuklash' }}
        </button>

        <p v-if="message" class="success-box">{{ message }}</p>
        <p v-if="error" class="error-box">{{ error }}</p>

        <div v-if="createdStudents.length" class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Ism familya</th>
                <th>Fan</th>
                <th>Daraja/Sinf</th>
                <th>O‘quv markaz</th>
                <th>Filial</th>
                <th>Code</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in createdStudents" :key="student.id">
                <td>{{ student.full_name }}</td>
                <td>{{ student.subject_name }}</td>
                <td>{{ student.level_name }}</td>
                <td>{{ student.center_name }}</td>
                <td>{{ student.branch }}</td>
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
                <th>Ism familya</th>
                <th>Fan</th>
                <th>Daraja/Sinf</th>
                <th>O'quv markaz</th>
                <th>Filial</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>Ali Valiyev</td>
                <td>English</td>
                <td>Beginner</td>
                <td>Al-Aziz Academy</td>
                <td>Navbahor</td>
              </tr>
              <tr>
                <td>2</td>
                <td>Madina Karimova</td>
                <td>Kampyuter</td>
                <td>Kampyuter 1</td>
                <td>Al-Aziz Academy</td>
                <td>Paxtazor</td>
              </tr>
              <tr>
                <td>3</td>
                <td>Jasur Sobirov</td>
                <td>IT</td>
                <td>Frontend 1</td>
                <td>Al-Aziz Academy</td>
                <td>Olmazor</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="hint-text">
          Fan va Daraja/Sinf nomini to‘g‘ri yozing. Filial nomi Excel faylda qanday yozilgan bo‘lsa, shu nom bilan avtomatik qo‘shiladi.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api/axios'

const file = ref(null)
const loading = ref(false)
const message = ref('')
const error = ref('')
const createdStudents = ref([])

function onFileChange(event) {
  file.value = event.target.files[0]
  message.value = ''
  error.value = ''
  createdStudents.value = []
}

async function upload() {
  if (!file.value) return
  loading.value = true
  message.value = ''
  error.value = ''
  createdStudents.value = []

  const formData = new FormData()
  formData.append('file', file.value)

  try {
    const res = await api.post('/students/import-excel/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 0,
    })
    createdStudents.value = res.data.students || []
    const errors = res.data.errors || []
    message.value = `${res.data.created_count} ta o‘quvchi yaratildi va random code berildi.`
    if (errors.length) {
      error.value = `${errors.length} ta qatorda xatolik bor: ${JSON.stringify(errors)}`
    }
  } catch (e) {
    error.value = JSON.stringify(e.response?.data || 'Xatolik')
  } finally {
    loading.value = false
  }
}
</script>
