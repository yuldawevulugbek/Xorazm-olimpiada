<template>
  <div ref="host" class="xorazm-scene" aria-hidden="true">
    <div v-if="fallback" class="xorazm-scene-fallback">
      <span class="fallback-minaret"></span>
    </div>
  </div>
</template>

<script setup>
// Antalya uslubidagi 3D sahna: Yivli Minare, Hıdırlık minorasi, Hadrian darvozasi,
// O'rta dengiz, palmalar va aylanib turuvchi oltin yulduzlar. three.js faqat shu sahifada yuklanadi.
import { onBeforeUnmount, onMounted, ref } from 'vue'

const props = defineProps({
  compact: { type: Boolean, default: false },
})

const host = ref(null)
const fallback = ref(false)
let cleanup = null

function bandTexture(THREE, bands, repeat = 1) {
  const canvas = document.createElement('canvas')
  canvas.width = 512
  canvas.height = 1024
  const ctx = canvas.getContext('2d')
  const total = bands.reduce((sum, band) => sum + band.h, 0)
  let y = 0
  for (const band of bands) {
    const h = (band.h / total) * canvas.height
    ctx.fillStyle = band.color
    ctx.fillRect(0, y, canvas.width, h)
    if (band.pattern === 'zigzag') {
      ctx.strokeStyle = band.accent
      ctx.lineWidth = 6
      ctx.beginPath()
      for (let x = 0; x <= canvas.width; x += 32) {
        ctx.lineTo(x, (x / 32) % 2 === 0 ? y + h * 0.25 : y + h * 0.75)
      }
      ctx.stroke()
    } else if (band.pattern === 'dots') {
      ctx.fillStyle = band.accent
      for (let x = 16; x < canvas.width; x += 32) {
        ctx.beginPath()
        ctx.arc(x, y + h / 2, Math.min(7, h / 4), 0, Math.PI * 2)
        ctx.fill()
      }
    } else if (band.pattern === 'stars') {
      ctx.fillStyle = band.accent
      for (let x = 24; x < canvas.width; x += 48) {
        const cy = y + h / 2
        const r = Math.min(14, h / 3)
        ctx.beginPath()
        for (let i = 0; i < 16; i++) {
          const a = (i / 16) * Math.PI * 2
          const rr = i % 2 === 0 ? r : r * 0.45
          ctx.lineTo(x + Math.cos(a) * rr, cy + Math.sin(a) * rr)
        }
        ctx.closePath()
        ctx.fill()
      }
    } else if (band.pattern === 'bricks') {
      ctx.strokeStyle = band.accent
      ctx.lineWidth = 2
      for (let row = 0; row < h; row += 18) {
        ctx.beginPath()
        ctx.moveTo(0, y + row)
        ctx.lineTo(canvas.width, y + row)
        ctx.stroke()
        for (let x = (row / 18) % 2 ? 0 : 20; x < canvas.width; x += 40) {
          ctx.beginPath()
          ctx.moveTo(x, y + row)
          ctx.lineTo(x, y + row + 18)
          ctx.stroke()
        }
      }
    }
    y += h
  }
  const texture = new THREE.CanvasTexture(canvas)
  texture.wrapS = THREE.RepeatWrapping
  texture.repeat.set(repeat, 1)
  texture.colorSpace = THREE.SRGBColorSpace
  return texture
}

function starShape(THREE, outer, inner, points = 8) {
  const shape = new THREE.Shape()
  for (let i = 0; i < points * 2; i++) {
    const a = (i / (points * 2)) * Math.PI * 2
    const r = i % 2 === 0 ? outer : inner
    const x = Math.cos(a) * r
    const y = Math.sin(a) * r
    if (i === 0) shape.moveTo(x, y)
    else shape.lineTo(x, y)
  }
  shape.closePath()
  return shape
}

onMounted(async () => {
  const el = host.value
  if (!el) return
  let THREE
  try {
    THREE = await import('three')
  } catch {
    fallback.value = true
    return
  }

  let renderer
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'low-power' })
  } catch {
    fallback.value = true
    return
  }

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2))
  renderer.outputColorSpace = THREE.SRGBColorSpace
  el.appendChild(renderer.domElement)

  const scene = new THREE.Scene()
  scene.fog = new THREE.Fog(0x0b1e3f, 14, 30)
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100)
  camera.position.set(0, 3.6, props.compact ? 19 : 17)

  scene.add(new THREE.HemisphereLight(0xfff1d6, 0x0b2a55, 1.1))
  const sun = new THREE.DirectionalLight(0xffd59a, 1.8)
  sun.position.set(6, 10, 7)
  scene.add(sun)
  const glow = new THREE.PointLight(0x2de2e6, 22, 18)
  glow.position.set(-3, 2, 4)
  scene.add(glow)

  const world = new THREE.Group()
  scene.add(world)
  const disposables = []
  const keep = (obj) => {
    disposables.push(obj)
    return obj
  }

  // Poydevor: O'rta dengiz rangidagi aylana maydon va qumli qirg'oq
  const plazaTex = keep(bandTexture(THREE, [
    { h: 1, color: '#f1dcb0', pattern: 'bricks', accent: '#d9b77c' },
  ], 6))
  const seaTex = keep(bandTexture(THREE, [
    { h: 1, color: '#0e7fb5', pattern: 'zigzag', accent: '#5ce1e6' },
    { h: 1, color: '#0b5f94', pattern: 'zigzag', accent: '#9fe8f0' },
    { h: 1, color: '#0e7fb5', pattern: 'zigzag', accent: '#5ce1e6' },
  ], 8))
  const plaza = new THREE.Mesh(
    keep(new THREE.CylinderGeometry(6.2, 6.6, 0.5, 64)),
    keep(new THREE.MeshStandardMaterial({ map: plazaTex, roughness: 0.9 })),
  )
  plaza.position.y = -2.25
  world.add(plaza)
  const sea = new THREE.Mesh(
    keep(new THREE.CylinderGeometry(6.0, 6.0, 0.06, 64, 1, false, Math.PI * 0.95, Math.PI * 0.9)),
    keep(new THREE.MeshStandardMaterial({ map: seaTex, roughness: 0.2, metalness: 0.3, emissive: 0x053a5c, emissiveIntensity: 0.5 })),
  )
  sea.position.y = -1.98
  world.add(sea)

  const ring = new THREE.Mesh(
    keep(new THREE.TorusGeometry(6.35, 0.08, 12, 96)),
    keep(new THREE.MeshStandardMaterial({ color: 0x18b6c4, emissive: 0x0b8a96, emissiveIntensity: 0.9 })),
  )
  ring.rotation.x = Math.PI / 2
  ring.position.y = -1.98
  world.add(ring)

  // Yivli Minare: qizil g'ishtdan, sakkiz qirrali (yivli) tanasi, firuza koshin belbog'lari
  const yivliTex = keep(bandTexture(THREE, [
    { h: 1.6, color: '#b5523b', pattern: 'bricks', accent: '#8a3a28' },
    { h: 0.3, color: '#1aa6b7', pattern: 'dots', accent: '#f6efe0' },
    { h: 1.6, color: '#b5523b', pattern: 'bricks', accent: '#8a3a28' },
    { h: 0.3, color: '#0f6fa8', pattern: 'zigzag', accent: '#f6efe0' },
    { h: 1.6, color: '#b5523b', pattern: 'bricks', accent: '#8a3a28' },
  ], 4))
  const yivliGeo = keep(new THREE.CylinderGeometry(0.85, 1.0, 6.2, 96, 1))
  const pos = yivliGeo.attributes.position
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i)
    const z = pos.getZ(i)
    const r = Math.hypot(x, z)
    if (r < 0.01) continue
    const a = Math.atan2(z, x)
    const k = 1 + 0.09 * Math.cos(a * 8)
    pos.setX(i, x * k)
    pos.setZ(i, z * k)
  }
  yivliGeo.computeVertexNormals()
  const yivli = new THREE.Mesh(yivliGeo, keep(new THREE.MeshStandardMaterial({ map: yivliTex, roughness: 0.75 })))
  yivli.position.set(0, 0.9, 0)
  world.add(yivli)
  const yivliBase = new THREE.Mesh(
    keep(new THREE.BoxGeometry(2.4, 1.1, 2.4)),
    keep(new THREE.MeshStandardMaterial({ map: plazaTex, color: 0xe2c58f, roughness: 0.85 })),
  )
  yivliBase.position.set(0, -1.45, 0)
  world.add(yivliBase)
  const balcony = new THREE.Mesh(
    keep(new THREE.CylinderGeometry(1.2, 1.0, 0.25, 48)),
    keep(new THREE.MeshStandardMaterial({ color: 0xf7d77a, metalness: 0.5, roughness: 0.35 })),
  )
  balcony.position.y = 4.05
  world.add(balcony)
  const yivliTop = new THREE.Mesh(
    keep(new THREE.CylinderGeometry(0.55, 0.7, 0.8, 32)),
    keep(new THREE.MeshStandardMaterial({ map: yivliTex, roughness: 0.7 })),
  )
  yivliTop.position.y = 4.55
  world.add(yivliTop)
  const cap = new THREE.Mesh(
    keep(new THREE.ConeGeometry(0.62, 1.3, 32)),
    keep(new THREE.MeshStandardMaterial({ color: 0x5b6670, metalness: 0.6, roughness: 0.35 })),
  )
  cap.position.y = 5.6
  world.add(cap)

  // Hıdırlık minorasi: kvadrat poydevor ustidagi dumaloq tosh minora
  const stoneTex = keep(bandTexture(THREE, [
    { h: 1, color: '#d8c3a0', pattern: 'bricks', accent: '#a98d64' },
  ], 3))
  const stoneMat = keep(new THREE.MeshStandardMaterial({ map: stoneTex, roughness: 0.9 }))
  const hidirBase = new THREE.Mesh(keep(new THREE.BoxGeometry(2.4, 1.6, 2.4)), stoneMat)
  hidirBase.position.set(3.7, -1.2, -2.0)
  world.add(hidirBase)
  const hidir = new THREE.Mesh(keep(new THREE.CylinderGeometry(1.0, 1.05, 2.4, 48)), stoneMat)
  hidir.position.set(3.7, 0.8, -2.0)
  world.add(hidir)
  const merlonGeo = keep(new THREE.BoxGeometry(0.28, 0.32, 0.28))
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2
    const merlon = new THREE.Mesh(merlonGeo, stoneMat)
    merlon.position.set(3.7 + Math.cos(a) * 0.9, 2.15, -2.0 + Math.sin(a) * 0.9)
    world.add(merlon)
  }

  // Hadrian darvozasi (Üç Kapılar): uch ravoqli marmar darvoza
  const marbleMat = keep(new THREE.MeshStandardMaterial({ color: 0xf3ead8, roughness: 0.55 }))
  const gate = new THREE.Group()
  const lintel = new THREE.Mesh(keep(new THREE.BoxGeometry(3.6, 0.45, 0.8)), marbleMat)
  lintel.position.y = 0.45
  gate.add(lintel)
  const cornice = new THREE.Mesh(keep(new THREE.BoxGeometry(3.8, 0.12, 0.9)), keep(new THREE.MeshStandardMaterial({ color: 0xf7d77a, metalness: 0.5, roughness: 0.35 })))
  cornice.position.y = 0.74
  gate.add(cornice)
  const columnGeo = keep(new THREE.CylinderGeometry(0.13, 0.15, 2.2, 20))
  for (const x of [-1.6, -0.55, 0.55, 1.6]) {
    for (const z of [-0.28, 0.28]) {
      const col = new THREE.Mesh(columnGeo, marbleMat)
      col.position.set(x, -0.9, z)
      gate.add(col)
    }
  }
  const archGeo = keep(new THREE.TorusGeometry(0.42, 0.07, 10, 24, Math.PI))
  for (const x of [-1.07, 0, 1.07]) {
    const arch = new THREE.Mesh(archGeo, marbleMat)
    arch.position.set(x, 0.08, 0.36)
    gate.add(arch)
  }
  for (const x of [-2.2, 2.2]) {
    const tower = new THREE.Mesh(keep(new THREE.BoxGeometry(0.8, 2.9, 0.9)), stoneMat)
    tower.position.set(x, -0.55, 0)
    gate.add(tower)
  }
  gate.position.set(-3.5, 0, -1.4)
  gate.rotation.y = 0.5
  world.add(gate)

  // Palmalar
  const trunkMat = keep(new THREE.MeshStandardMaterial({ color: 0x8a6239, roughness: 0.9 }))
  const leafMat = keep(new THREE.MeshStandardMaterial({ color: 0x2f9e5b, roughness: 0.6, side: THREE.DoubleSide }))
  const trunkGeo = keep(new THREE.CylinderGeometry(0.08, 0.14, 2.6, 10))
  const leafGeo = keep(new THREE.PlaneGeometry(1.4, 0.32))
  for (const [x, z] of [[1.9, 2.6], [-1.8, 2.9], [5.0, 1.2]]) {
    const palm = new THREE.Group()
    const trunk = new THREE.Mesh(trunkGeo, trunkMat)
    trunk.rotation.z = 0.08
    palm.add(trunk)
    for (let i = 0; i < 7; i++) {
      const leaf = new THREE.Mesh(leafGeo, leafMat)
      leaf.position.set(0, 1.3, 0)
      leaf.rotation.set(0, (i / 7) * Math.PI * 2, -0.45)
      leaf.translateX(0.62)
      palm.add(leaf)
    }
    palm.position.set(x, -0.7, z)
    world.add(palm)
  }
  // Oltin sakkiz qirrali yulduzlar va bilim kristallari
  const starGeo = keep(new THREE.ExtrudeGeometry(starShape(THREE, 0.5, 0.26), { depth: 0.14, bevelEnabled: true, bevelSize: 0.03, bevelThickness: 0.03, bevelSegments: 2 }))
  starGeo.center()
  const goldMat = keep(new THREE.MeshStandardMaterial({ color: 0xf5c84c, metalness: 0.85, roughness: 0.22, emissive: 0x6b4a00, emissiveIntensity: 0.35 }))
  const crystalGeo = keep(new THREE.OctahedronGeometry(0.32, 0))
  const crystalMat = keep(new THREE.MeshStandardMaterial({ color: 0x5ce1e6, metalness: 0.2, roughness: 0.1, transparent: true, opacity: 0.85, emissive: 0x0b6c78, emissiveIntensity: 0.6 }))
  const floaters = []
  const count = props.compact ? 8 : 14
  for (let i = 0; i < count; i++) {
    const isStar = i % 2 === 0
    const mesh = new THREE.Mesh(isStar ? starGeo : crystalGeo, isStar ? goldMat : crystalMat)
    const angle = (i / count) * Math.PI * 2
    const radius = 4.2 + (i % 3) * 1.1
    mesh.userData = { angle, radius, height: 0.5 + (i % 4) * 1.1, speed: 0.12 + (i % 5) * 0.03, spin: 0.6 + (i % 3) * 0.4 }
    floaters.push(mesh)
    world.add(mesh)
  }

  // Yulduzli osmon
  const starCount = 420
  const positions = new Float32Array(starCount * 3)
  for (let i = 0; i < starCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 50
    positions[i * 3 + 1] = Math.random() * 18 - 2
    positions[i * 3 + 2] = -10 - Math.random() * 20
  }
  const skyGeo = keep(new THREE.BufferGeometry())
  skyGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  const sky = new THREE.Points(skyGeo, keep(new THREE.PointsMaterial({ color: 0xfff3c4, size: 0.07, transparent: true, opacity: 0.85 })))
  scene.add(sky)

  const pointer = { x: 0, y: 0 }
  const onPointer = (event) => {
    const rect = el.getBoundingClientRect()
    pointer.x = ((event.clientX - rect.left) / rect.width - 0.5) * 2
    pointer.y = ((event.clientY - rect.top) / rect.height - 0.5) * 2
  }
  window.addEventListener('pointermove', onPointer, { passive: true })

  const resize = () => {
    const w = el.clientWidth || 1
    const h = el.clientHeight || 1
    renderer.setSize(w, h, false)
    camera.aspect = w / h
    camera.updateProjectionMatrix()
  }
  const observer = new ResizeObserver(resize)
  observer.observe(el)
  resize()

  let frame = 0
  let running = true
  const clock = new THREE.Clock()
  const render = () => {
    if (!running) return
    const t = clock.getElapsedTime()
    world.rotation.y = t * 0.12
    for (const mesh of floaters) {
      const d = mesh.userData
      const a = d.angle + t * d.speed
      mesh.position.set(Math.cos(a) * d.radius, d.height + Math.sin(t * 1.3 + d.angle) * 0.35, Math.sin(a) * d.radius)
      mesh.rotation.y = t * d.spin
      mesh.rotation.x = Math.sin(t * 0.7 + d.angle) * 0.5
    }
    ring.material.emissiveIntensity = 0.6 + Math.sin(t * 2) * 0.35
    seaTex.offset.x = t * 0.015
    sky.rotation.y = t * 0.01
    camera.position.x += (pointer.x * 2.2 - camera.position.x) * 0.04
    camera.position.y += (3.6 - pointer.y * 1.2 - camera.position.y) * 0.04
    camera.lookAt(0, 1.2, 0)
    renderer.render(scene, camera)
    if (!reduceMotion) frame = requestAnimationFrame(render)
  }

  const onVisibility = () => {
    cancelAnimationFrame(frame)
    running = !document.hidden
    if (running) render()
  }
  document.addEventListener('visibilitychange', onVisibility)
  render()
  el.classList.add('is-ready')

  cleanup = () => {
    running = false
    cancelAnimationFrame(frame)
    observer.disconnect()
    window.removeEventListener('pointermove', onPointer)
    document.removeEventListener('visibilitychange', onVisibility)
    disposables.forEach(item => item.dispose?.())
    renderer.dispose()
    renderer.domElement.remove()
  }
})

onBeforeUnmount(() => cleanup?.())
</script>
