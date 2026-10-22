<template>
  <div class="student-entry-page xz-entry">
    <section class="xz-entry-grid">
      <div class="xz-entry-copy">
        <span class="xz-kicker"><b>★</b> Xorazm viloyati · Online olimpiada</span>
        <h1 class="xz-title">Xorazm<span>Olimpiadasi</span></h1>
        <p class="xz-lead">
          Xiva naqshlari ostida bilim bellashuvi. Admin bergan status code bilan testga kiring,
          savollarni ishlang va javoblaringizni yuboring.
        </p>

        <div class="xz-stage-login">
          <div v-tilt="6" class="student-card entry-card xz-login-card">
            <div class="xz-card-badges">
              <span>O‘QUVCHI KIRISHI</span>
              <span>★ OLIMPIADA</span>
            </div>

            <template v-if="mode === 'code'">
              <h2>Testga kirish</h2>
              <p class="entry-subtitle">Admin bergan 6 xonali status code’ni kiriting.</p>

              <form @submit.prevent="startExam" class="code-form entry-form">
                <label class="code-label">
                  Status code
                  <input
                    v-model="code"
                    maxlength="6"
                    minlength="6"
                    inputmode="numeric"
                    placeholder="582914"
                    required
                  />
                </label>
                <button class="primary-btn entry-start-btn" :disabled="loading">
                  {{ loading ? 'Tekshirilmoqda...' : 'Testni boshlash' }}
                </button>
              </form>

              <button type="button" class="xz-register-toggle" @click="openRegister">
                <span>✍️</span> Ro‘yxatdan o‘tish
              </button>
            </template>

            <template v-else>
              <h2>Ro‘yxatdan o‘tish</h2>
              <p class="entry-subtitle">Ma’lumotlaringizni kiriting, fan va darajani tanlang. Test darhol boshlanadi.</p>

              <form @submit.prevent="register" class="xz-register-form">
                <label>
                  Ism familiya
                  <input v-model.trim="reg.full_name" autocomplete="name" placeholder="Masalan: Aliyev Vali" required />
                </label>
                <label>
                  O‘quv markaz
                  <input v-model.trim="reg.center" list="xz-center-list" placeholder="O‘quv markaz nomini kiriting" required />
                  <datalist id="xz-center-list">
                    <option v-for="name in catalog.centers" :key="name" :value="name" />
                  </datalist>
                </label>
                <label class="xz-register-age">
                  Yosh
                  <input v-model.number="reg.age" type="number" min="4" max="99" inputmode="numeric" placeholder="12" required />
                </label>
                <div class="xz-register-row">
                  <label>
                    Fan
                    <select v-model="reg.subject" required @change="reg.level = ''">
                      <option value="" disabled>Fanni tanlang</option>
                      <option v-for="subject in catalog.subjects" :key="subject.id" :value="subject.id">{{ subject.name }}</option>
                    </select>
                  </label>
                  <label>
                    Daraja
                    <select v-model="reg.level" required :disabled="!selectedSubject">
                      <option value="" disabled>{{ selectedSubject ? 'Darajani tanlang' : 'Avval fanni tanlang' }}</option>
                      <option v-for="level in selectedSubject?.levels || []" :key="level.id" :value="level.id">{{ level.name }}</option>
                    </select>
                  </label>
                </div>
                <button class="primary-btn entry-start-btn" :disabled="loading || catalogLoading">
                  {{ loading ? 'Test tayyorlanmoqda...' : 'Testga kirish' }}
                </button>
              </form>

              <button type="button" class="xz-register-toggle is-back" @click="closeRegister">
                ← Status code bilan kirish
              </button>
            </template>

            <p v-if="error" class="error-box">{{ error }}</p>

            <RouterLink to="/admin/login" class="admin-login-link entry-admin-link">
              Admin panelga kirish
            </RouterLink>
          </div>
        </div>
      </div>

      <div class="xz-stage">
        <XorazmScene />
        <div class="xz-orbit-labels">
          <span>ICHAN QAL‘A</span>
          <span>KALTA MINOR</span>
          <span>ISLOM XO‘JA</span>
        </div>
        <div class="xz-subjects xz-stage-subjects">
          <span>🧮 Matematika</span>
          <span>🇬🇧 English</span>
          <span>📚 Rus tili</span>
          <span>💻 IT Frontend</span>
          <span>🐍 IT Backend</span>
          <span>🧠 Mental arifmetika</span>
        </div>

      </div>
    </section>

    <div v-if="showResultModal" class="modal-backdrop result-lookup-backdrop" @click.self="closeResultModal">
      <div class="answer-modal result-lookup-modal">
        <button type="button" class="modal-close-btn" @click="closeResultModal">×</button>

        <template v-if="!publicResult">
          <div class="result-modal-icon">📊</div>
          <h2>Natijani ko‘rish</h2>
          <p>Natijangizni ko‘rish uchun sizga berilgan 6 xonali status code’ni kiriting.</p>

          <form @submit.prevent="lookupResult" class="result-lookup-form">
            <label class="code-label">
              Status code
              <input
                v-model="resultCode"
                maxlength="6"
                minlength="6"
                inputmode="numeric"
                placeholder="582914"
                required
              />
            </label>
            <button class="primary-btn" :disabled="resultLoading">
              {{ resultLoading ? 'Qidirilmoqda...' : 'Natijani ko‘rish' }}
            </button>
          </form>

          <p v-if="resultError" class="error-box">{{ resultError }}</p>
        </template>

        <template v-else>
          <div class="result-modal-icon success">✓</div>
          <h2>Test yakunlandi</h2>
          <p class="result-meta">
            {{ publicResult.student_full_name }} · {{ publicResult.subject_name }} · {{ publicResult.level_name }}
          </p>

          <div class="public-result-details">
            <div>
              <span>Holat</span>
              <b>Natija adminga yuborildi</b>
            </div>
            <div>
              <span>O‘quv markaz</span>
              <b>{{ publicResult.center_name }}</b>
            </div>
            <div>
              <span>Filial</span>
              <b>{{ publicResult.branch || '—' }}</b>
            </div>
            <div>
              <span>Sarflagan vaqt</span>
              <b>{{ formatSeconds(publicResult.spent_seconds) }}</b>
            </div>
          </div>

          <button type="button" class="secondary-btn block-link" @click="resetResultLookup">
            Boshqa code tekshirish
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/axios'
import XorazmScene from '../components/XorazmScene.vue'

const router = useRouter()
const code = ref('')
const loading = ref(false)
const error = ref('')
const showResultModal = ref(false)
const resultCode = ref('')
const resultLoading = ref(false)
const resultError = ref('')
const publicResult = ref(null)

// Ro'yxatdan o'tish: o'quvchi o'zi fan va darajani tanlab testga kiradi.
const mode = ref('code')
const catalog = reactive({ subjects: [], centers: [] })
const catalogLoading = ref(false)
const reg = reactive({ full_name: '', center: '', age: '', subject: '', level: '' })
const selectedSubject = computed(() => catalog.subjects.find(item => item.id === reg.subject))

function cleanCode(value) {
  return String(value || '').trim()
}

function formatSeconds(seconds) {
  const total = Number(seconds || 0)
  const min = Math.floor(total / 60)
  const sec = total % 60
  return `${min} daq ${sec} sek`
}

function openResultModal() {
  showResultModal.value = true
  resultCode.value = cleanCode(code.value)
  resultError.value = ''
  publicResult.value = null
}

function closeResultModal() {
  showResultModal.value = false
}

function resetResultLookup() {
  publicResult.value = null
  resultCode.value = ''
  resultError.value = ''
}

async function openExam(finalCode) {
  const res = await api.post('/exam/start/', { code: finalCode })
  sessionStorage.setItem('exam_payload', JSON.stringify({ ...res.data, code: finalCode }))
  router.push('/exam')
}

async function startExam() {
  loading.value = true
  error.value = ''
  try {
    await openExam(cleanCode(code.value))
  } catch (e) {
    error.value = e.response?.data?.detail || 'Code xato yoki oldin ishlatilgan.'
  } finally {
    loading.value = false
  }
}

async function openRegister() {
  mode.value = 'register'
  error.value = ''
  if (catalog.subjects.length) return
  catalogLoading.value = true
  try {
    const res = await api.get('/exam/catalog/')
    catalog.subjects = res.data.subjects || []
    catalog.centers = res.data.centers || []
  } catch (e) {
    error.value = 'Fanlar ro‘yxatini yuklab bo‘lmadi. Sahifani yangilang.'
  } finally {
    catalogLoading.value = false
  }
}

function closeRegister() {
  mode.value = 'code'
  error.value = ''
}

async function register() {
  loading.value = true
  error.value = ''
  try {
    const res = await api.post('/exam/register/', {
      full_name: reg.full_name,
      center: reg.center,
      age: reg.age,
      level: reg.level,
    })
    code.value = res.data.code
    await openExam(res.data.code)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ro‘yxatdan o‘tishda xatolik. Qayta urinib ko‘ring.'
  } finally {
    loading.value = false
  }
}

async function lookupResult() {
  resultLoading.value = true
  resultError.value = ''
  publicResult.value = null
  try {
    const res = await api.post('/exam/result/', { code: cleanCode(resultCode.value) })
    publicResult.value = res.data
  } catch (e) {
    resultError.value = e.response?.data?.detail || 'Natija topilmadi.'
  } finally {
    resultLoading.value = false
  }
}
</script>
