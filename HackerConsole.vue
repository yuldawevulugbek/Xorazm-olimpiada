<template>
  <div class="full-hacker-page" @click="focusSecretBox">
    <div class="full-hacker-bg" aria-hidden="true"></div>
    <header class="full-hacker-top">
      <div>
        <span>CODINGWITHULUGBEK // VISUAL MODE</span>
        <h1>Hacker Console</h1>
      </div>
      <div class="full-hacker-top-actions">
        <button type="button" @click.stop="clearAll">Tozalash</button>
        <RouterLink to="/admin/dashboard" @click.stop>Admin panelga qaytish</RouterLink>
      </div>
    </header>

    <main class="full-hacker-desktop">
      <section class="hack-window program-window">
        <div class="hack-window-title">
          <b>Program Console</b>
          <span>— □ ×</span>
        </div>
        <textarea
          ref="secretBox"
          :value="fakeInput"
          spellcheck="false"
          autocomplete="off"
          placeholder="Istalgan tugmani bosing... Siz yozgan matn ko‘rinmaydi, o‘rniga code chiqadi."
          @keydown="handleSecretTyping"
          @paste.prevent="handlePaste"
          @input="handleInput"
          @focus="hasFocus = true"
          @blur="hasFocus = false"
        ></textarea>
      </section>

      <section class="hack-window trace-window">
        <div class="hack-window-title center-title">
          <b>Neural Network Tracing</b>
        </div>
        <svg viewBox="0 0 600 270" class="trace-svg" aria-hidden="true">
          <line
            v-for="edge in edges"
            :key="edge.id"
            :x1="edge.x1"
            :y1="edge.y1"
            :x2="edge.x2"
            :y2="edge.y2"
            class="trace-line"
          />
          <circle
            v-for="node in nodes"
            :key="node.id"
            :cx="node.x"
            :cy="node.y"
            :r="node.hot ? 5 : 3.6"
            :class="node.hot ? 'trace-node hot' : 'trace-node'"
          />
        </svg>
      </section>

      <section class="hack-window matrix-window">
        <div class="hack-window-title"><b>Compiling...</b><span>×</span></div>
        <div class="matrix-grid">
          <span v-for="(char, index) in matrixChars" :key="index">{{ char }}</span>
        </div>
      </section>

      <section class="hack-window editor-window">
        <div class="hack-window-title"><b>Text Editor</b><span>— □ ×</span></div>
        <pre>{{ editorArt }}</pre>
      </section>

      <section class="hack-window graph-window">
        <div class="graph-grid">
          <i v-for="bar in graphBars" :key="bar.id" :style="{ height: `${bar.height}%` }"></i>
        </div>
        <span class="graph-value">{{ graphValue }}</span>
      </section>

      <aside class="hack-icons-panel">
        <button v-for="tool in tools" :key="tool.name" type="button" @click.stop="spawnTool(tool.name)">
          <b>{{ tool.icon }}</b>
          <span>{{ tool.name }}</span>
        </button>
      </aside>

      <section class="hack-window terminal-full-window">
        <div class="hack-window-title">
          <b>Auto Code Stream</b>
          <span>{{ isStreaming ? 'LIVE' : 'PAUSED' }}</span>
        </div>
        <div ref="terminalBody" class="full-terminal-body">
          <p v-for="(line, index) in codeLines" :key="index" :class="line.type">
            <span>{{ String(index + 1).padStart(3, '0') }}</span>
            <code>{{ line.text }}</code>
          </p>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, ref } from 'vue'

const secretBox = ref(null)
const terminalBody = ref(null)
const fakeInput = ref('')
const fakeInputLines = ref([])
const hasFocus = ref(false)
const isStreaming = ref(false)
const codeLines = ref([
  { type: 'info', text: '[BOOT] visual hacker screen loaded' },
  { type: 'ok', text: '[READY] type anything: original text will be hidden' },
])
const matrixChars = ref(createMatrixChars())
const graphValue = ref(5360)
const graphBars = ref(Array.from({ length: 18 }, (_, id) => ({ id, height: random(12, 92) })))
const editorArt = ref(createAsciiLogo())
let timer = null
let cursor = 0

const nodes = Array.from({ length: 34 }, (_, id) => ({
  id,
  x: random(20, 580),
  y: random(28, 242),
  hot: id % 7 === 0,
}))
const edges = Array.from({ length: 52 }, (_, id) => {
  const a = nodes[random(0, nodes.length - 1)]
  const b = nodes[random(0, nodes.length - 1)]
  return { id, x1: a.x, y1: a.y, x2: b.x, y2: b.y }
})

const tools = [
  { icon: '▣', name: 'Visual Miner' },
  { icon: '⌗', name: 'Compiler' },
  { icon: '⇆', name: 'Remote Link' },
  { icon: '◎', name: 'Trace Map' },
  { icon: '▰', name: 'Program Console' },
  { icon: '◈', name: 'Matrix Screen' },
]

const fakeConsoleRows = [
  () => `penetrate.visual_layer --mode demo --sig ${randomHex(10)}`,
  () => `compile.ui.packet(${random(1000, 9999)}) => OK_${randomHex(6)}`,
  () => `matrix.drawLine(x:${random(10, 900)}, y:${random(10, 500)}, glow:true);`,
  () => `neural.trace.node[${random(1, 99)}].pulse = 0.${random(35, 99)}`,
  () => `render.terminal.feed("${randomBinary(16)}")`,
  () => `academy.visual.encryptFrame("${randomHex(12)}")`,
  () => `scan.green_channel >> ${random(18, 98)}% completed`,
  () => `window.spawn("Program Console", seed="${randomHex(8)}")`,
]

const streamRows = [
  () => `[SYS] visual packet accepted :: ${randomHex(18)}`,
  () => `const neon_${cursor} = createPulse({ speed: ${random(12, 96)}, color: "#00ff00" });`,
  () => `for (let i = 0; i < ${random(4, 18)}; i++) screen.matrix.push("${randomBinary(8)}");`,
  () => `trace.map.connect(${random(10, 99)}, ${random(10, 99)}) // demo route`,
  () => `ui.window("console").writeLine(hash("${randomHex(10)}"));`,
  () => `neuralGraph.update({ nodes: ${random(14, 88)}, status: "ONLINE" });`,
  () => `visualFirewall.simulate("PASS", token="${randomHex(12)}")`,
  () => `render.asciiLogo("TEXT EDITOR", frame=${random(1, 60)});`,
  () => `[STREAM] ${randomBinary(4)} ${randomBinary(4)} ${randomBinary(4)} ${randomBinary(4)} :: OK`,
]

function handleSecretTyping(event) {
  if (event.ctrlKey || event.metaKey || event.altKey) return
  const keysToHide = event.key.length === 1 || ['Enter', 'Backspace', 'Delete', 'Tab', ' '].includes(event.key)
  if (!keysToHide) return
  event.preventDefault()
  registerHiddenTyping(event.key === 'Enter' ? 2 : 1)
}

function handlePaste() {
  registerHiddenTyping(8)
}

function handleInput(event) {
  event.target.value = fakeInput.value
  registerHiddenTyping(1)
}

function registerHiddenTyping(amount = 1) {
  for (let i = 0; i < amount; i += 1) {
    fakeInputLines.value.push(fakeConsoleRows[cursor % fakeConsoleRows.length]())
    addLine()
    cursor += 1
  }
  if (fakeInputLines.value.length > 18) fakeInputLines.value.splice(0, fakeInputLines.value.length - 18)
  fakeInput.value = fakeInputLines.value.join('\n')
  matrixChars.value = createMatrixChars()
  graphValue.value = random(2000, 9999)
  graphBars.value = graphBars.value.map(bar => ({ ...bar, height: random(12, 95) }))
  editorArt.value = createAsciiLogo()
  startAutoStream()
  nextTick(() => {
    if (secretBox.value) {
      secretBox.value.value = fakeInput.value
      secretBox.value.scrollTop = secretBox.value.scrollHeight
    }
  })
}

function addLine(typeOverride = null) {
  const maker = streamRows[cursor % streamRows.length]
  const type = typeOverride || (cursor % 8 === 0 ? 'warn' : cursor % 5 === 0 ? 'ok' : 'code')
  codeLines.value.push({ type, text: maker() })
  if (codeLines.value.length > 120) codeLines.value.splice(0, codeLines.value.length - 120)
  nextTick(() => {
    if (terminalBody.value) terminalBody.value.scrollTop = terminalBody.value.scrollHeight
  })
}

function startAutoStream() {
  if (timer) return
  isStreaming.value = true
  timer = setInterval(() => {
    addLine()
    cursor += 1
    if (cursor % 4 === 0) {
      fakeInputLines.value.push(fakeConsoleRows[cursor % fakeConsoleRows.length]())
      if (fakeInputLines.value.length > 18) fakeInputLines.value.splice(0, fakeInputLines.value.length - 18)
      fakeInput.value = fakeInputLines.value.join('\n')
    }
  }, 380)
}

function stopAutoStream() {
  isStreaming.value = false
  if (timer) clearInterval(timer)
  timer = null
}

function clearAll() {
  stopAutoStream()
  cursor = 0
  fakeInputLines.value = []
  fakeInput.value = ''
  codeLines.value = [
    { type: 'info', text: '[CLEAR] screen cleaned' },
    { type: 'ok', text: '[READY] type anything to generate fake code' },
  ]
  nextTick(() => focusSecretBox())
}

function spawnTool(name) {
  codeLines.value.push({ type: 'info', text: `[OPEN] ${name} module rendered in visual mode` })
  registerHiddenTyping(2)
}

function focusSecretBox() {
  if (secretBox.value && !hasFocus.value) secretBox.value.focus()
}

function createMatrixChars() {
  const chars = '01アイウエオカキクケコサシスセソタチツテトABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&*+-'
  return Array.from({ length: 260 }, () => chars[random(0, chars.length - 1)])
}

function createAsciiLogo() {
  return [
    '████████╗███████╗██╗  ██╗████████╗',
    '╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝',
    '   ██║   █████╗   ╚███╔╝    ██║   ',
    '   ██║   ██╔══╝   ██╔██╗    ██║   ',
    '   ██║   ███████╗██╔╝ ██╗   ██║   ',
    '   ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝   ',
    '        CODE EDITOR // VISUAL ONLY  ',
  ].join('\n')
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

function randomHex(length) {
  const chars = 'ABCDEF0123456789'
  return Array.from({ length }, () => chars[random(0, chars.length - 1)]).join('')
}

function randomBinary(length) {
  return Array.from({ length }, () => random(0, 1)).join('')
}

onBeforeUnmount(stopAutoStream)
</script>
