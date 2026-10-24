<template>
  <div ref="host" class="xorazm-scene" aria-hidden="true">
    <div v-if="fallback" class="xorazm-scene-fallback">
      <span class="fallback-minaret"></span>
    </div>
  </div>
</template>

<script setup>
// Xiva (Ichan Qal'a) uslubidagi 3D sahna: Kalta Minor, Islom Xo'ja minorasi,
// moviy gumbaz, aylanib turuvchi oltin yulduzlar. three.js faqat shu sahifada yuklanadi.
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

  // Poydevor: majolika naqshli aylana maydon
  const plazaTex = keep(bandTexture(THREE, [
    { h: 1, color: '#f1dcb0', pattern: 'bricks', accent: '#d9b77c' },
  ], 6))
  const plaza = new THREE.Mesh(
    keep(new THREE.CylinderGeometry(6.2, 6.6, 0.5, 64)),
    keep(new THREE.MeshStandardMaterial({ map: plazaTex, roughness: 0.9 })),
  )
  plaza.position.y = -2.25
  world.add(plaza)

  const ring = new THREE.Mesh(
    keep(new THREE.TorusGeometry(6.35, 0.08, 12, 96)),
    keep(new THREE.MeshStandardMaterial({ color: 0x18b6c4, emissive: 0x0b8a96, emissiveIntensity: 0.9 })),
  )
  ring.rotation.x = Math.PI / 2
  ring.position.y = -1.98
  world.add(ring)

  // Kalta Minor: keng, kalta, moviy-firuza belbog'li minora
  const kaltaTex = keep(bandTexture(THREE, [
    { h: 1.2, color: '#0f6fa8', pattern: 'stars', accent: '#f7d77a' },
    { h: 0.5, color: '#f6efe0', pattern: 'dots', accent: '#1aa6b7' },
    { h: 1.4, color: '#1aa6b7', pattern: 'zigzag', accent: '#f6efe0' },
    { h: 0.5, color: '#0b3c75', pattern: 'dots', accent: '#f7d77a' },
    { h: 1.6, color: '#2a86c9', pattern: 'stars', accent: '#ffffff' },
    { h: 0.6, color: '#f6efe0', pattern: 'zigzag', accent: '#0f6fa8' },
    { h: 1.4, color: '#1295a3', pattern: 'bricks', accent: '#0b5d68' },
  ], 3))
  const kalta = new THREE.Mesh(
    keep(new THREE.CylinderGeometry(1.25, 1.85, 4.2, 64, 1)),
    keep(new THREE.MeshStandardMaterial({ map: kaltaTex, roughness: 0.45, metalness: 0.08 })),
  )
  kalta.position.set(0, 0.1, 0)
  world.add(kalta)
  const kaltaTop = new THREE.Mesh(
    keep(new THREE.CylinderGeometry(1.32, 1.25, 0.18, 64)),
    keep(new THREE.MeshStandardMaterial({ color: 0xf7d77a, metalness: 0.6, roughness: 0.3 })),
  )
  kaltaTop.position.y = 2.28
  world.add(kaltaTop)

  // Islom Xo'ja minorasi: baland, ingichka
  const tallTex = keep(bandTexture(THREE, [
    { h: 0.4, color: '#f6efe0', pattern: 'dots', accent: '#1aa6b7' },
    { h: 1, color: '#d8b98a', pattern: 'bricks', accent: '#b8915c' },
    { h: 0.35, color: '#1aa6b7', pattern: 'zigzag', accent: '#f6efe0' },
    { h: 1, color: '#d8b98a', pattern: 'bricks', accent: '#b8915c' },
    { h: 0.35, color: '#0f6fa8', pattern: 'stars', accent: '#f7d77a' },
    { h: 1, color: '#d8b98a', pattern: 'bricks', accent: '#b8915c' },
    { h: 0.35, color: '#1aa6b7', pattern: 'zigzag', accent: '#f6efe0' },
  ], 2))
  const tall = new THREE.Mesh(
    keep(new THREE.CylinderGeometry(0.42, 0.78, 7.2, 48)),
    keep(new THREE.MeshStandardMaterial({ map: tallTex, roughness: 0.7 })),
  )
  tall.position.set(3.6, 1.6, -2.2)
  world.add(tall)
  const lantern = new THREE.Mesh(
    keep(new THREE.CylinderGeometry(0.55, 0.45, 0.6, 24)),
    keep(new THREE.MeshStandardMaterial({ color: 0x1aa6b7, roughness: 0.35 })),
  )
  lantern.position.set(3.6, 5.5, -2.2)
  world.add(lantern)
  const tallDome = new THREE.Mesh(
    keep(new THREE.SphereGeometry(0.5, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2)),
    keep(new THREE.MeshStandardMaterial({ color: 0x0f8f9d, roughness: 0.3, metalness: 0.2 })),
  )
  tallDome.position.set(3.6, 5.8, -2.2)
  world.add(tallDome)

  // Moviy gumbazli madrasa
  const base = new THREE.Mesh(
    keep(new THREE.BoxGeometry(2.6, 1.6, 2.6)),
    keep(new THREE.MeshStandardMaterial({ map: plazaTex, color: 0xe8cf9f, roughness: 0.85 })),
  )
  base.position.set(-3.6, -1.2, -1.6)
  world.add(base)
  const drum = new THREE.Mesh(
    keep(new THREE.CylinderGeometry(1, 1.05, 0.5, 48)),
    keep(new THREE.MeshStandardMaterial({ map: kaltaTex, roughness: 0.5 })),
  )
  drum.position.set(-3.6, -0.15, -1.6)
  world.add(drum)
  const dome = new THREE.Mesh(
    keep(new THREE.SphereGeometry(1.05, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2)),
    keep(new THREE.MeshStandardMaterial({ color: 0x14a3b2, roughness: 0.25, metalness: 0.25, emissive: 0x06363c, emissiveIntensity: 0.4 })),
  )
  dome.position.set(-3.6, 0.1, -1.6)
  world.add(dome)

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
