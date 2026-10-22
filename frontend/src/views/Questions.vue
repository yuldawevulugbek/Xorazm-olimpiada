<template>
  <div>
    <div class="page-head">
      <div>
        <h2>Testlar</h2>
        <p>Fan → daraja → testlar tartibida ko‘rish paneli.</p>
      </div>
      <button class="secondary-btn" @click="loadData">Yangilash</button>
    </div>

    <div v-if="error" class="error-box">{{ error }}</div>
    <div v-if="loading" class="hint-box">Testlar yuklanmoqda...</div>

    <div class="test-browser">
      <section class="panel test-column">
        <div class="section-title">
          <h3>Fanlar</h3>
          <span>{{ subjectCards.length }} ta fan</span>
        </div>

        <div class="test-list">
          <button
            v-for="subject in subjectCards"
            :key="subject.id"
            type="button"
            class="test-row"
            :class="{ active: activeSubjectId === subject.id }"
            @click="selectSubject(subject.id)"
          >
            <span>
              <b>{{ subject.name }}</b>
              <small>{{ subject.levelCount }} ta daraja/sinf</small>
            </span>
            <strong>{{ subject.questionCount }}</strong>
          </button>
          <p v-if="!subjectCards.length && !loading" class="hint-box">Hozircha test kiritilgan fan yo‘q.</p>
        </div>
      </section>

      <section class="panel test-column">
        <div class="section-title">
          <h3>Darajalar/Sinflar</h3>
          <span v-if="activeSubject">{{ activeSubject.name }}</span>
        </div>

        <div v-if="!activeSubject" class="empty-state">Fan tanlang.</div>
        <div v-else class="test-list">
          <button
            v-for="level in levelCards"
            :key="level.id"
            type="button"
            class="test-row"
            :class="{ active: activeLevelId === level.id }"
            @click="selectLevel(level.id)"
          >
            <span>
              <b>{{ level.name }}</b>
              <small>{{ activeSubject.name }}</small>
            </span>
            <strong>{{ level.questionCount }}</strong>
          </button>
          <p v-if="!levelCards.length" class="hint-box">Bu fanda hali daraja/sinf/test yo‘q.</p>
        </div>
      </section>

      <section class="panel test-column wide">
        <div class="section-title">
          <h3>Testlar</h3>
          <span v-if="activeLevel">{{ activeLevel.name }} — {{ selectedQuestions.length }} ta test</span>
        </div>

        <div v-if="!activeLevel" class="empty-state">Daraja/Sinf tanlang.</div>
        <div v-else>
          <div v-if="versionCards.length > 1" class="version-filter-row">
            <button
              v-for="version in versionCards"
              :key="version.value"
              type="button"
              class="version-filter-btn"
              :class="{ active: activeVersion === version.value }"
              @click="selectVersion(version.value)"
            >
              Version {{ version.value }} <b>{{ version.count }}</b>
            </button>
          </div>
          <div class="question-view-list">
          <article v-for="(q, index) in selectedQuestions" :key="q.id" class="question-view-card">
            <div class="question-top">
              <span class="question-number">{{ index + 1 }}</span>
              <span class="question-version-badge">Version {{ q.version || 1 }}</span>
              <button type="button" class="secondary-btn compact-btn" @click="toggleQuestion(q.id)">
                {{ openedQuestionId === q.id ? 'Yopish' : 'Ko‘rish' }}
              </button>
            </div>
            <h4 class="question-text">{{ q.text }}</h4>
            <img v-if="q.image_url" :src="q.image_url" alt="" class="question-image" loading="lazy" />
            <div v-if="openedQuestionId === q.id" class="answers-grid">
              <div :class="answerClass(q, 'A')"><b>A.</b> {{ q.option_a }}</div>
              <div :class="answerClass(q, 'B')"><b>B.</b> {{ q.option_b }}</div>
              <div v-if="q.option_c" :class="answerClass(q, 'C')"><b>C.</b> {{ q.option_c }}</div>
              <div v-if="q.option_d" :class="answerClass(q, 'D')"><b>D.</b> {{ q.option_d }}</div>
              <p class="correct-answer">To‘g‘ri javob: <b>{{ q.correct_answer }}</b></p>
            </div>
          </article>
          <p v-if="!selectedQuestions.length" class="hint-box">Bu darajada testlar yo‘q.</p>
          </div>
        </div>
      </section>
    </div>

    <div v-if="mainAdmin" class="panel mt">
      <h3>Yangi savol qo‘shish</h3>
      <form @submit.prevent="createQuestion" class="form-grid create-question-grid">
        <label>Fan
          <select v-model="form.subject" required @change="onFormSubjectChange">
            <option value="">Tanlang</option>
            <option v-for="s in subjects" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
        </label>
        <label>Daraja/Sinf/Sinf
          <select v-model="form.level" required>
            <option value="">Tanlang</option>
            <option v-for="l in filteredLevels" :key="l.id" :value="l.id">{{ l.name }}</option>
          </select>
        </label>
        <label>Version
          <select v-model.number="form.version" required>
            <option :value="1">Version 1</option>
            <option :value="2">Version 2</option>
            <option :value="3">Version 3</option>
          </select>
        </label>
        <label class="full-span">Savol matni <textarea v-model="form.text" required rows="3"></textarea></label>
        <label>A javob <input v-model="form.option_a" required /></label>
        <label>B javob <input v-model="form.option_b" required /></label>
        <label>C javob <input v-model="form.option_c" /></label>
        <label>D javob <input v-model="form.option_d" placeholder="Bo‘sh qolsa, 3 ta variant chiqadi" /></label>
        <label class="full-span">Rasm manzili (ixtiyoriy) <input v-model="form.image_url" placeholder="/test-images/rasm.jpg" /></label>
        <label>To‘g‘ri javob
          <select v-model="form.correct_answer" required>
            <option>A</option><option>B</option><option>C</option><option>D</option>
          </select>
        </label>
        <button class="primary-btn">Savol qo‘shish</button>
      </form>
      <p v-if="message" class="success-box">{{ message }}</p>
    </div>

    <div v-else class="hint-box mt">
      Siz testlarni faqat ko‘rishingiz mumkin. Test qo‘shish/o‘zgartirish faqat asosiy admin uchun ochiq.
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import api from '../api/axios'
import { getStoredAdminProfile, isMainAdmin } from '../utils/auth'

const subjects = ref([])
const levels = ref([])
const questions = ref([])
const activeSubjectId = ref(null)
const activeLevelId = ref(null)
const activeVersion = ref(1)
const openedQuestionId = ref(null)
const loading = ref(false)
const message = ref('')
const error = ref('')
const adminProfile = ref(getStoredAdminProfile())

const mainAdmin = computed(() => isMainAdmin(adminProfile.value))

const form = reactive({
  subject: '',
  level: '',
  version: 1,
  text: '',
  option_a: '',
  option_b: '',
  option_c: '',
  option_d: '',
  image_url: '',
  correct_answer: 'A'
})

const questionCountsBySubject = computed(() => {
  const counts = new Map()
  questions.value.forEach(q => {
    const key = Number(q.subject)
    counts.set(key, (counts.get(key) || 0) + 1)
  })
  return counts
})

const questionCountsByLevel = computed(() => {
  const counts = new Map()
  questions.value.forEach(q => {
    const key = Number(q.level)
    counts.set(key, (counts.get(key) || 0) + 1)
  })
  return counts
})

const subjectCards = computed(() => subjects.value
  .map(subject => {
    const questionCount = questionCountsBySubject.value.get(Number(subject.id)) || 0
    const levelCount = new Set(
      questions.value
        .filter(q => Number(q.subject) === Number(subject.id))
        .map(q => Number(q.level))
    ).size
    return { ...subject, questionCount, levelCount }
  })
  .filter(subject => subject.questionCount > 0)
)

const activeSubject = computed(() => subjects.value.find(s => Number(s.id) === Number(activeSubjectId.value)))

const levelCards = computed(() => levels.value
  .filter(level => Number(level.subject) === Number(activeSubjectId.value))
  .map(level => ({
    ...level,
    questionCount: questionCountsByLevel.value.get(Number(level.id)) || 0
  }))
  .filter(level => level.questionCount > 0)
)

const activeLevel = computed(() => levels.value.find(l => Number(l.id) === Number(activeLevelId.value)))

const versionCards = computed(() => {
  const counts = new Map()
  questions.value
    .filter(q => Number(q.level) === Number(activeLevelId.value))
    .forEach(q => {
      const version = Number(q.version || 1)
      counts.set(version, (counts.get(version) || 0) + 1)
    })
  return [...counts.entries()]
    .sort((a, b) => a[0] - b[0])
    .map(([value, count]) => ({ value, count }))
})

const selectedQuestions = computed(() => questions.value.filter(q =>
  Number(q.level) === Number(activeLevelId.value) && Number(q.version || 1) === Number(activeVersion.value)
))

const filteredLevels = computed(() => levels.value.filter(l => String(l.subject) === String(form.subject)))

function selectSubject(subjectId) {
  activeSubjectId.value = Number(subjectId)
  const firstLevel = levels.value.find(level =>
    Number(level.subject) === Number(subjectId) && (questionCountsByLevel.value.get(Number(level.id)) || 0) > 0
  )
  activeLevelId.value = firstLevel ? Number(firstLevel.id) : null
  setFirstVersionForActiveLevel()
  openedQuestionId.value = null
}

function setFirstVersionForActiveLevel() {
  const versions = questions.value
    .filter(q => Number(q.level) === Number(activeLevelId.value))
    .map(q => Number(q.version || 1))
    .sort((a, b) => a - b)
  activeVersion.value = versions.length ? versions[0] : 1
}

function selectLevel(levelId) {
  activeLevelId.value = Number(levelId)
  setFirstVersionForActiveLevel()
  openedQuestionId.value = null
}

function selectVersion(version) {
  activeVersion.value = Number(version || 1)
  openedQuestionId.value = null
}

function toggleQuestion(questionId) {
  openedQuestionId.value = openedQuestionId.value === questionId ? null : questionId
}

function answerClass(question, letter) {
  return ['answer-box', question.correct_answer === letter ? 'correct' : '']
}

function onFormSubjectChange() {
  form.level = ''
  form.version = 1
}

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    const [subjectsRes, levelsRes, questionsRes] = await Promise.all([
      api.get('/subjects/'),
      api.get('/levels/'),
      api.get('/questions/')
    ])
    subjects.value = Array.isArray(subjectsRes.data) ? subjectsRes.data : subjectsRes.data.results || []
    levels.value = Array.isArray(levelsRes.data) ? levelsRes.data : levelsRes.data.results || []
    questions.value = Array.isArray(questionsRes.data) ? questionsRes.data : questionsRes.data.results || []

    if (!activeSubjectId.value && subjectCards.value.length) {
      selectSubject(subjectCards.value[0].id)
    } else if (activeSubjectId.value && !subjectCards.value.some(s => Number(s.id) === Number(activeSubjectId.value))) {
      activeSubjectId.value = null
      activeLevelId.value = null
      openedQuestionId.value = null
    }
  } catch (e) {
    error.value = JSON.stringify(e.response?.data || 'Testlarni yuklashda xatolik yuz berdi.')
  } finally {
    loading.value = false
  }
}

async function createQuestion() {
  message.value = ''
  error.value = ''
  try {
    await api.post('/questions/', form)
    Object.assign(form, {
      subject: '',
      level: '',
      version: 1,
      text: '',
      option_a: '',
      option_b: '',
      option_c: '',
      option_d: '',
      image_url: '',
      correct_answer: 'A'
    })
    message.value = 'Savol qo‘shildi.'
    await loadData()
  } catch (e) {
    error.value = JSON.stringify(e.response?.data || 'Savol qo‘shishda xatolik yuz berdi.')
  }
}

onMounted(loadData)
</script>

<style scoped>
.test-browser {
  display: grid;
  grid-template-columns: minmax(220px, 0.8fr) minmax(220px, 0.8fr) minmax(320px, 1.4fr);
  gap: 18px;
  align-items: start;
}

.test-column {
  min-height: 360px;
}

.test-column.wide {
  min-height: 520px;
}

.section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.section-title h3 {
  margin: 0;
}

.section-title span {
  color: #64748b;
  font-size: 14px;
  font-weight: 800;
}

.test-list,
.question-view-list {
  display: grid;
  gap: 12px;
}

.test-row {
  width: 100%;
  border: 1px solid rgba(148, 163, 184, 0.28);
  background: rgba(248, 250, 252, 0.9);
  border-radius: 18px;
  padding: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  cursor: pointer;
  text-align: left;
  transition: 0.2s ease;
}

.test-row:hover,
.test-row.active {
  border-color: rgba(79, 70, 229, 0.55);
  background: rgba(79, 70, 229, 0.09);
  transform: translateY(-1px);
}

.test-row span {
  display: grid;
  gap: 4px;
}

.test-row small {
  color: #64748b;
}

.test-row strong {
  min-width: 38px;
  height: 38px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  background: #eff6ff;
  color: #1d4ed8;
}

.empty-state {
  min-height: 220px;
  border: 1px dashed rgba(148, 163, 184, 0.45);
  border-radius: 22px;
  display: grid;
  place-items: center;
  color: #64748b;
  background: rgba(248, 250, 252, 0.72);
  font-weight: 800;
}

.question-view-card {
  border: 1px solid rgba(148, 163, 184, 0.28);
  border-radius: 22px;
  padding: 16px;
  background: rgba(248, 250, 252, 0.82);
}

.question-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.question-number {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: #0f172a;
  color: #fff;
  font-weight: 900;
}

.question-view-card h4 {
  margin: 0 0 12px;
  line-height: 1.5;
}

.compact-btn {
  padding: 8px 12px;
  border-radius: 12px;
}


.version-filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 14px;
}

.version-filter-btn,
.question-version-badge {
  border: 1px solid rgba(79, 70, 229, 0.25);
  border-radius: 999px;
  background: #eef2ff;
  color: #3730a3;
  font-weight: 900;
}

.version-filter-btn {
  padding: 9px 13px;
  cursor: pointer;
}

.version-filter-btn.active {
  background: #4f46e5;
  color: #fff;
}

.version-filter-btn b {
  margin-left: 8px;
}

.question-version-badge {
  padding: 7px 10px;
  font-size: 12px;
}

.answers-grid {
  display: grid;
  gap: 10px;
}

.answer-box {
  border: 1px solid rgba(148, 163, 184, 0.28);
  border-radius: 16px;
  padding: 12px;
  background: #fff;
}

.answer-box.correct {
  border-color: rgba(22, 163, 74, 0.5);
  background: rgba(220, 252, 231, 0.75);
  color: #166534;
}

.correct-answer {
  margin: 0;
  color: #166534;
  font-weight: 800;
}

.create-question-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.full-span {
  grid-column: 1 / -1;
}

@media (max-width: 1100px) {
  .test-browser,
  .create-question-grid {
    grid-template-columns: 1fr;
  }
}
</style>
