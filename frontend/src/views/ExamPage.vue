<template>
  <div class="exam-page" v-if="payload">
    <header class="exam-header">
      <div>
        <h1>{{ payload.student.full_name }}</h1>
        <p>{{ payload.student.subject_name }} <span v-if="!isMental && !isVersionSelect && hasSecondStage">· {{ currentStage }}/2</span></p>
        <p v-if="payload.student.is_self_registered" class="exam-own-code" title="Sahifa yopilib qolsa, shu code bilan qayta kirasiz">
          Sizning code: <b>{{ payload.student.code }}</b>
        </p>
      </div>
      <div v-if="!isMental && !isVersionSelect" class="timer" :class="{ danger: remainingSeconds < 300 }">{{ formattedTime }}</div>
      <div v-else-if="isMental" class="timer mental-timer" :class="{ danger: remainingSeconds < 60 }">
        {{ formattedTime }} · Mental {{ Math.min(currentMentalIndex + 1, mentalTasks.length) }}/{{ mentalTasks.length }}
      </div>
    </header>

    <main v-if="isVersionSelect" class="version-select-stage">
      <div class="version-select-card">
        <span class="entry-badge">Test versionini tanlang</span>
        <h2>Version tanlash</h2>
        <p>Har bir versionda 20 tadan test bor. Qaysi versionni tanlasangiz, shu versiondagi savollar boshlanadi.</p>

        <div class="version-buttons">
          <button
            v-for="version in availableVersions"
            :key="version.value"
            type="button"
            class="version-choice-btn"
            :disabled="versionLoading"
            @click="chooseVersion(version.value)"
          >
            <b>{{ version.label }}</b>
            <span>{{ version.questions_count }} ta test</span>
          </button>
        </div>

        <p v-if="versionError" class="error-box">{{ versionError }}</p>
        <RouterLink to="/student" class="secondary-btn block-link">Boshqa code kiritish</RouterLink>
      </div>
    </main>

    <main v-else-if="isMental" class="mental-stage">
      <div v-if="mentalPhase === 'countdown'" class="countdown-card">
        <p>Tayyorlaning</p>
        <strong>{{ countdownValue }}</strong>
      </div>

      <div v-else-if="mentalPhase === 'showing'" class="mental-number-card">
        <p>{{ currentMentalIndex + 1 }}-misol</p>
        <strong>{{ shownValue }}</strong>
        <span>Misol 3 sekund ko‘rsatiladi. Javob modalida ham vaqt davom etadi.</span>
      </div>

      <div v-else-if="mentalPhase === 'finished'" class="countdown-card">
        <p>Natija yuborilmoqda...</p>
      </div>

      <div class="mental-progress">
        <span v-for="(task, index) in mentalTasks" :key="task.id" :class="{ active: index === currentMentalIndex, done: mentalAnswers[task.id] !== undefined }"></span>
      </div>

      <div v-if="mentalPhase === 'answer'" class="modal-backdrop">
        <div class="answer-modal">
          <h2>{{ currentMentalIndex + 1 }}-misol javobi</h2>
          <p>Hisoblagan natijangizni kiriting.</p>
          <form @submit.prevent="saveMentalAnswer">
            <input ref="answerInputRef" v-model="answerInput" type="number" inputmode="numeric" placeholder="Javob" required />
            <button class="primary-btn" type="submit">Javobni saqlash</button>
          </form>
        </div>
      </div>

    </main>

    <main v-else class="exam-body">
      <div v-if="hasSecondStage" class="stage-info-card">
        <b>{{ currentStage }}/2-bosqich</b>
        <span>{{ currentStage === 1 ? 'Avval 1–20 savollarni ishlang.' : `2-bosqich: 21–${allQuestions.length} savollarni ishlang.` }}</span>
      </div>

      <div v-for="item in visibleQuestions" :key="item.q.id" class="question-card">
        <h3 class="question-text">{{ item.number }}. {{ item.q.text }}</h3>
        <img v-if="item.q.image_url" :src="item.q.image_url" alt="" class="question-image" loading="lazy" />
        <div class="options-grid">
          <label
            v-for="opt in optionList(item.q)"
            :key="opt.value"
            class="option-card"
            :class="{ selected: answers[item.q.id] === opt.value }"
          >
            <input type="radio" :name="`question-${item.q.id}`" :value="opt.value" v-model="answers[item.q.id]" @change="persistTestProgress" />
            <span>{{ opt.value }}) {{ opt.text }}</span>
          </label>
        </div>
      </div>

      <button v-if="currentStage === 1 && hasSecondStage" class="primary-btn finish-btn" :disabled="!isFirstStageComplete || submitting || finishModal.show" @click="openSecondStage">2-bosqichga o‘tish</button>
      <button v-else class="primary-btn finish-btn" :disabled="submitting || finishModal.show" @click="confirmFinishOpen = true">{{ submitting ? 'Yakunlanmoqda...' : 'Testni yakunlash' }}</button>
      <p v-if="currentStage === 1 && hasSecondStage && !isFirstStageComplete" class="stage-hint">2-bosqichga o‘tish uchun avval 20 ta savolning hammasiga javob bering.</p>
    </main>

    <div v-if="stageBreakModal" class="modal-backdrop success-backdrop">
      <div class="finish-modal-card success">
        <div class="finish-icon">2</div>
        <h2>2-bosqich</h2>
        <p>Endi qolgan {{ allQuestions.length - 20 }} ta test chiqadi. Umumiy vaqt {{ payload?.duration_minutes || 60 }} daqiqa bo‘yicha davom etadi.</p>
        <button class="primary-btn" type="button" @click="startSecondStage">Boshlash</button>
      </div>
    </div>

    <!-- Tasodifan bosib yuborilmasligi uchun yakunlashdan oldin tasdiqlash -->
    <div v-if="confirmFinishOpen && !finishModal.show" class="modal-backdrop success-backdrop" @click.self="confirmFinishOpen = false">
      <div class="finish-modal-card confirm">
        <div class="finish-icon">?</div>
        <h2>Testni yakunlaysizmi?</h2>
        <p v-if="unansweredCount">Javob berilmagan savollar: <b>{{ unansweredCount }} ta</b>. Yakunlagandan keyin javoblarni o‘zgartirib bo‘lmaydi.</p>
        <p v-else>Barcha savollarga javob berdingiz. Yakunlagandan keyin javoblarni o‘zgartirib bo‘lmaydi.</p>
        <div class="confirm-actions">
          <button class="secondary-btn" type="button" @click="confirmFinishOpen = false">Qaytish</button>
          <button class="primary-btn" type="button" @click="confirmFinishOpen = false; submitExam()">Ha, yakunlash</button>
        </div>
      </div>
    </div>

    <div v-if="finishModal.show" class="modal-backdrop success-backdrop">
      <div class="finish-modal-card" :class="finishModal.type">
        <div class="finish-icon">{{ finishModal.type === 'success' ? '✓' : '!' }}</div>
        <h2>{{ finishModal.title }}</h2>
        <p>{{ finishModal.message }}</p>
        <button class="primary-btn" type="button" @click="finishModal.type === 'success' ? goToStudentLogin() : closeFinishModal()">{{ finishModal.type === 'success' ? 'Code kiritish sahifasiga qaytish' : 'Yopish' }}</button>
      </div>
    </div>
  </div>
  <div v-else class="student-entry-page">
    <div class="student-card">
      <h1>Test topilmadi</h1>
      <RouterLink to="/student" class="primary-btn block-link">Code kiritish sahifasiga qaytish</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/axios'

const router = useRouter()
const payload = ref(null)
const answers = reactive({})
const remainingSeconds = ref(0)
const submitting = ref(false)
const confirmFinishOpen = ref(false)
const unansweredCount = computed(() => (payload.value?.questions || []).filter(q => !answers[q.id]).length)
const finishModal = reactive({
  show: false,
  type: 'success',
  title: '',
  message: '',
  result: null,
})

const mentalPhase = ref('countdown')
const countdownValue = ref(3)
const currentMentalIndex = ref(0)
const shownValue = ref('')
const mentalAnswers = reactive({})
const answerInput = ref('')
const answerInputRef = ref(null)
const versionLoading = ref(false)
const versionError = ref('')
const currentStage = ref(1)
const stageBreakModal = ref(false)
const mentalTimers = []

let intervalId = null
let submitted = false
let progressSaveTimer = null
let lastServerProgressSave = 0
// Har bir o'quvchi boshqa vaqtda yuboradi, hamma bir soniyada emas.
const SERVER_HEARTBEAT_SECONDS = 15
let timerTicksSinceServerSave = Math.floor(Math.random() * SERVER_HEARTBEAT_SECONDS)

const isVersionSelect = computed(() => payload.value?.mode === 'version_select')
const isMental = computed(() => payload.value?.mode === 'mental')
const mentalTasks = computed(() => payload.value?.mental_tasks || [])
const availableVersions = computed(() => payload.value?.available_versions || [])
const allQuestions = computed(() => payload.value?.questions || [])
const visibleQuestions = computed(() => {
  const start = currentStage.value === 1 ? 0 : 20
  return allQuestions.value.slice(start, start + 20).map((q, index) => ({ q, number: start + index + 1 }))
})
const hasSecondStage = computed(() => allQuestions.value.length > 20)
const isFirstStageComplete = computed(() => allQuestions.value.slice(0, 20).every(q => answers[q.id]))
const formattedTime = computed(() => {
  const m = Math.floor(remainingSeconds.value / 60)
  const s = remainingSeconds.value % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})

function showFinishSuccess() {
  finishModal.show = true
  finishModal.type = 'success'
  finishModal.title = 'Test yakunlandi'
  finishModal.message = 'Javoblaringiz adminga yuborildi.'
  // O‘quvchiga nechta to‘g‘ri topgani va foiz ko‘rsatilmaydi.
  // Natijalar faqat admin panelda ko‘rinadi.
  finishModal.result = null
}

function showFinishError(message) {
  finishModal.show = true
  finishModal.type = 'error'
  finishModal.title = 'Xatolik yuz berdi'
  finishModal.message = message || 'Javoblarni yuborishda xatolik yuz berdi.'
  finishModal.result = null
}

function goToStudentLogin() {
  router.push('/student')
}

function closeFinishModal() {
  finishModal.show = false
}

function optionList(q) {
  return [
    { value: 'A', text: q.option_a },
    { value: 'B', text: q.option_b },
    { value: 'C', text: q.option_c },
    { value: 'D', text: q.option_d },
  ].filter(opt => opt.text)
}

function payloadCode() {
  return payload.value?.code || payload.value?.student?.code || ''
}

function examProgressKey() {
  const code = payloadCode()
  return code ? `exam_progress_${code}` : ''
}

function buildProgressBody() {
  return {
    code: payloadCode(),
    remaining_seconds: Math.max(0, Number(remainingSeconds.value || 0)),
    current_index: isMental.value ? Number(currentMentalIndex.value || 0) : 0,
    answers: isMental.value ? { ...mentalAnswers } : { ...answers },
  }
}

// Server band bo'lsa yoki internet bir zum uzilsa, javoblar yo'qolmasin:
// yakunlash so'rovi bir necha marta, oraliqni oshirib qayta yuboriladi.
async function postSubmitWithRetry(body, attempts = 5) {
  let lastError
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      return await api.post('/exam/submit/', body)
    } catch (e) {
      lastError = e
      const statusCode = e.response?.status
      // Oldingi urinish serverga yetib borgan, faqat javobi kelmagan: test allaqachon saqlangan.
      if (attempt > 0 && statusCode === 400) return null
      if (statusCode && statusCode < 500 && statusCode !== 429) throw e
      const wait = Math.min(8000, 1000 * 2 ** attempt) + Math.random() * 1000
      await new Promise(resolve => setTimeout(resolve, wait))
    }
  }
  throw lastError
}

async function saveProgressToServer(force = false) {
  if (!payload.value || submitted || isVersionSelect.value || !payloadCode()) return
  const now = Date.now()
  if (!force && now - lastServerProgressSave < 2500) return
  lastServerProgressSave = now
  try {
    await api.post('/exam/progress/', buildProgressBody())
  } catch (_) {}
}

function scheduleProgressSave() {
  if (!payload.value || submitted) return
  if (progressSaveTimer) clearTimeout(progressSaveTimer)
  progressSaveTimer = setTimeout(() => {
    progressSaveTimer = null
    saveProgressToServer(true)
  }, 1500)
}

function persistTestProgress(sendRemote = true) {
  const key = examProgressKey()
  if (!key) return
  localStorage.setItem(key, JSON.stringify({ answers: { ...answers }, remaining_seconds: remainingSeconds.value, current_stage: currentStage.value }))
  if (sendRemote !== false) scheduleProgressSave()
}

function loadTestProgress() {
  const serverAnswers = payload.value?.saved_answers
  if (serverAnswers && typeof serverAnswers === 'object') {
    Object.assign(answers, serverAnswers)
  }

  const key = examProgressKey()
  if (!key) return
  try {
    const saved = JSON.parse(localStorage.getItem(key) || '{}')
    if (saved.answers && typeof saved.answers === 'object') {
      Object.assign(answers, saved.answers)
    }
    if (Number(saved.current_stage) === 2) currentStage.value = 2
  } catch (_) {}
}

function safeDurationMinutes(defaultMinutes) {
  if (isMental.value) return 5
  const value = Number(defaultMinutes)
  return Number.isFinite(value) && value > 0 ? value : 60
}

function remainingFromStartedAt(defaultMinutes) {
  const minutes = safeDurationMinutes(defaultMinutes)
  const durationSeconds = Math.max(1, minutes * 60)
  const savedRemaining = Number(payload.value?.remaining_seconds)
  if (Number.isFinite(savedRemaining) && savedRemaining >= 0) {
    return Math.max(0, Math.min(durationSeconds, Math.floor(savedRemaining)))
  }

  // Backend yangi test boshlanganda resume=false yuboradi.
  // Shunda yangi yaratilgan o‘quvchi 00:00 bo‘lib qolmaydi, 30:00 dan boshlaydi.
  if (payload.value?.resume === false) {
    return durationSeconds
  }

  const startedAt = Date.parse(payload.value?.started_at || '')
  if (!Number.isFinite(startedAt)) {
    return durationSeconds
  }

  const elapsedSeconds = Math.max(0, Math.floor((Date.now() - startedAt) / 1000))
  return Math.max(0, durationSeconds - elapsedSeconds)
}

function clearMentalTimers() {
  while (mentalTimers.length) clearTimeout(mentalTimers.pop())
}

function mentalProgressKey() {
  const code = payloadCode()
  return code ? `mental_progress_${code}` : ''
}

function persistMentalProgress(sendRemote = true) {
  const key = mentalProgressKey()
  if (!key) return
  localStorage.setItem(key, JSON.stringify({
    answers: { ...mentalAnswers },
    remaining_seconds: remainingSeconds.value,
    current_index: currentMentalIndex.value,
  }))
  if (sendRemote !== false) scheduleProgressSave()
}

function loadMentalProgress() {
  const serverAnswers = payload.value?.saved_answers
  if (serverAnswers && typeof serverAnswers === 'object') {
    Object.assign(mentalAnswers, serverAnswers)
  }

  const key = mentalProgressKey()
  try {
    if (key) {
      const saved = JSON.parse(localStorage.getItem(key) || '{}')
      if (saved.answers && typeof saved.answers === 'object') {
        Object.assign(mentalAnswers, saved.answers)
      }
    }
    const firstUnansweredIndex = mentalTasks.value.findIndex(task => mentalAnswers[task.id] === undefined)
    const serverIndex = Number(payload.value?.progress_current_index || 0)
    currentMentalIndex.value = firstUnansweredIndex === -1
      ? mentalTasks.value.length
      : Math.max(0, Math.min(firstUnansweredIndex, Number.isFinite(serverIndex) ? serverIndex : firstUnansweredIndex))
  } catch (_) {
    currentMentalIndex.value = 0
  }
}

function startMentalCountdown(startIndex = 0) {
  mentalPhase.value = 'countdown'
  countdownValue.value = 3
  const tick = () => {
    if (countdownValue.value <= 1) {
      playMentalTask(startIndex)
      return
    }
    countdownValue.value -= 1
    mentalTimers.push(setTimeout(tick, 1000))
  }
  mentalTimers.push(setTimeout(tick, 1000))
}

function playMentalTask(index) {
  clearMentalTimers()
  const task = mentalTasks.value[index]
  if (!task) {
    submitMentalExam()
    return
  }

  currentMentalIndex.value = index
  mentalPhase.value = 'showing'
  shownValue.value = ''
  answerInput.value = ''

  const flashes = task.flashes || []
  const taskDisplayMs = Number(task.task_display_ms || 3000)
  const perFlashMs = flashes.length ? Math.max(250, Math.floor(taskDisplayMs / flashes.length)) : taskDisplayMs

  flashes.forEach((value, flashIndex) => {
    mentalTimers.push(setTimeout(() => {
      shownValue.value = value
    }, flashIndex * perFlashMs))
  })

  mentalTimers.push(setTimeout(async () => {
    mentalPhase.value = 'answer'
    shownValue.value = ''
    await nextTick()
    answerInputRef.value?.focus()
  }, taskDisplayMs))
}

function saveMentalAnswer() {
  const task = mentalTasks.value[currentMentalIndex.value]
  if (!task) return

  mentalAnswers[task.id] = answerInput.value
  persistMentalProgress()

  const nextIndex = currentMentalIndex.value + 1
  if (remainingSeconds.value <= 0 || nextIndex >= mentalTasks.value.length) {
    submitMentalExam()
  } else {
    playMentalTask(nextIndex)
  }
}

async function submitMentalExam() {
  if (submitted || !payload.value) return
  submitted = true
  submitting.value = true
  mentalPhase.value = 'finished'
  clearMentalTimers()

  const lastAttemptedIndex = Math.min(currentMentalIndex.value, mentalTasks.value.length - 1)
  const answerList = mentalTasks.value
    .filter((task, index) => index <= lastAttemptedIndex || mentalAnswers[task.id] !== undefined)
    .map(task => ({
      task_id: task.id,
      answer: mentalAnswers[task.id] ?? '',
    }))

  try {
    await postSubmitWithRetry({
      code: payloadCode(),
      answers: answerList,
      remaining_seconds: Math.max(0, Number(remainingSeconds.value || 0)),
    })
    sessionStorage.removeItem('exam_payload')
    localStorage.removeItem(mentalProgressKey())
    localStorage.removeItem(examProgressKey())
    showFinishSuccess()
  } catch (e) {
    submitted = false
    showFinishError(e.response?.data?.detail || 'Mental javoblarni yuborishda xatolik.')
  } finally {
    submitting.value = false
  }
}


function openSecondStage() {
  if (!isFirstStageComplete.value) return
  stageBreakModal.value = true
}

function startSecondStage() {
  currentStage.value = 2
  stageBreakModal.value = false
  persistTestProgress(true)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function submitExam() {
  if (submitted || !payload.value) return
  submitted = true
  submitting.value = true
  clearInterval(intervalId)
  const answerList = payload.value.questions.map(q => ({ question_id: q.id, answer: answers[q.id] || '' }))
  try {
    await postSubmitWithRetry({
      code: payloadCode(),
      answers: answerList,
      remaining_seconds: Math.max(0, Number(remainingSeconds.value || 0)),
    })
    sessionStorage.removeItem('exam_payload')
    localStorage.removeItem(examProgressKey())
    localStorage.removeItem(mentalProgressKey())
    showFinishSuccess()
  } catch (e) {
    submitted = false
    showFinishError(e.response?.data?.detail || 'Testni yakunlashda xatolik.')
  } finally {
    submitting.value = false
  }
}


async function chooseVersion(version) {
  if (!payload.value || versionLoading.value) return
  versionLoading.value = true
  versionError.value = ''
  try {
    const res = await api.post('/exam/start/', { code: payloadCode(), version })
    const nextPayload = { ...res.data, code: payloadCode() }
    payload.value = nextPayload
    sessionStorage.setItem('exam_payload', JSON.stringify(nextPayload))
    bootExamPayload()
  } catch (e) {
    versionError.value = e.response?.data?.detail || 'Versionni boshlashda xatolik yuz berdi.'
  } finally {
    versionLoading.value = false
  }
}

function clearObject(target) {
  Object.keys(target).forEach(key => delete target[key])
}

function bootExamPayload() {
  clearInterval(intervalId)
  clearMentalTimers()
  clearObject(answers)
  clearObject(mentalAnswers)
  submitted = false
  submitting.value = false
  versionError.value = ''
  finishModal.show = false
  currentMentalIndex.value = 0
  currentStage.value = 1
  stageBreakModal.value = false
  mentalPhase.value = 'countdown'
  countdownValue.value = 3

  if (!payload.value || isVersionSelect.value) return

  if (isMental.value) {
    // Mentalda code qayta kiritilganda vaqt yangidan boshlanmaydi.
    // Backend bergan started_at bo‘yicha qolgan vaqt hisoblanadi.
    const durationMinutes = safeDurationMinutes(payload.value.duration_minutes || 5)
    remainingSeconds.value = remainingFromStartedAt(durationMinutes)

    loadMentalProgress()
    if (remainingSeconds.value <= 0 || currentMentalIndex.value >= mentalTasks.value.length) {
      submitMentalExam()
    } else {
      startTimer()
      startMentalCountdown(currentMentalIndex.value)
    }
    return
  }

  // Oddiy English testda 60 minut vaqt beriladi. Code qayta kiritilganda avvalgi javoblar va qolgan vaqt saqlanadi.
  const durationMinutes = safeDurationMinutes(payload.value.duration_minutes || 60)
  remainingSeconds.value = remainingFromStartedAt(durationMinutes)
  loadTestProgress()
  if (!hasSecondStage.value) currentStage.value = 1
  else if (currentStage.value !== 2 && isFirstStageComplete.value) currentStage.value = 2

  if (remainingSeconds.value <= 0) {
    submitExam()
  } else {
    startTimer()
  }
}

function startTimer() {
  clearInterval(intervalId)
  intervalId = setInterval(() => {
    if (submitted) {
      clearInterval(intervalId)
      return
    }

    // Vaqt backenddagi started_at bo‘yicha hisoblanadi; bu yerda faqat ekrandagi timer yuradi.
    // Javoblar localStorage’da saqlanadi, code qayta kiritilganda boshidan boshlanmaydi.
    remainingSeconds.value = Math.max(0, remainingSeconds.value - 1)
    if (isMental.value) persistMentalProgress(false)
    else persistTestProgress(false)

    // Javob tanlanganda progress darhol yuboriladi; bu yerda faqat qolgan vaqt
    // har 15 soniyada serverga eslatiladi (har 3 soniyada emas), shunda yuzlab
    // o'quvchi bir vaqtda ishlaganda server ortiqcha so'rovlarga to'lib qolmaydi.
    timerTicksSinceServerSave += 1
    if (timerTicksSinceServerSave >= SERVER_HEARTBEAT_SECONDS) {
      timerTicksSinceServerSave = 0
      saveProgressToServer(false)
    }

    if (remainingSeconds.value <= 0) {
      remainingSeconds.value = 0
      clearInterval(intervalId)
      clearMentalTimers()
      if (isMental.value) submitMentalExam()
      else submitExam()
    }
  }, 1000)
}

function saveProgressBeforeExit() {
  if (!payload.value || submitted || isVersionSelect.value) return
  if (isMental.value) persistMentalProgress(false)
  else persistTestProgress(false)

  try {
    const body = JSON.stringify(buildProgressBody())
    fetch(`${api.defaults.baseURL}/exam/progress/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
      keepalive: true,
    })
  } catch (_) {}
}

function handleVisibilityChange() {
  if (document.visibilityState === 'hidden') saveProgressBeforeExit()
}

onMounted(() => {
  window.addEventListener('beforeunload', saveProgressBeforeExit)
  window.addEventListener('pagehide', saveProgressBeforeExit)
  document.addEventListener('visibilitychange', handleVisibilityChange)
  const saved = sessionStorage.getItem('exam_payload')
  if (!saved) return
  payload.value = JSON.parse(saved)
  bootExamPayload()
  // Test har doim tepadan, 1-savoldan ko'rinadi (savollar chizilgandan keyin ham).
  const scrollToTop = () => window.scrollTo({ top: 0, left: 0, behavior: 'instant' })
  scrollToTop()
  nextTick(() => requestAnimationFrame(scrollToTop))
  setTimeout(scrollToTop, 350)
})

onBeforeUnmount(() => {
  saveProgressBeforeExit()
  window.removeEventListener('beforeunload', saveProgressBeforeExit)
  window.removeEventListener('pagehide', saveProgressBeforeExit)
  document.removeEventListener('visibilitychange', handleVisibilityChange)
  clearInterval(intervalId)
  if (progressSaveTimer) clearTimeout(progressSaveTimer)
  clearMentalTimers()
})
</script>


<style scoped>

.stage-info-card {
  margin-bottom: 18px;
  padding: 16px 18px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid rgba(148, 163, 184, 0.28);
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: #0f172a;
}

.stage-info-card span, .stage-hint {
  color: #64748b;
}

.stage-hint {
  text-align: center;
  margin-top: 10px;
}

.version-select-stage {
  min-height: calc(100vh - 120px);
  display: grid;
  place-items: center;
  padding: 24px;
}

.version-select-card {
  width: min(720px, 100%);
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid rgba(148, 163, 184, 0.26);
  border-radius: 28px;
  padding: 28px;
  box-shadow: 0 24px 70px rgba(15, 23, 42, 0.14);
  text-align: center;
}

.version-select-card h2 {
  margin: 12px 0 8px;
  color: #0f172a;
}

.version-select-card p {
  color: #64748b;
}

.version-buttons {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin: 24px 0;
}

.version-choice-btn {
  border: 1px solid rgba(79, 70, 229, 0.28);
  border-radius: 22px;
  padding: 20px 14px;
  background: linear-gradient(180deg, #ffffff, #eef2ff);
  cursor: pointer;
  display: grid;
  gap: 8px;
  color: #1e1b4b;
  transition: 0.2s ease;
}

.version-choice-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  border-color: rgba(79, 70, 229, 0.65);
  box-shadow: 0 16px 34px rgba(79, 70, 229, 0.18);
}

.version-choice-btn b {
  font-size: 20px;
}

.version-choice-btn span {
  color: #64748b;
  font-weight: 800;
}

@media (max-width: 720px) {
  .version-buttons {
    grid-template-columns: 1fr;
  }
}
</style>
