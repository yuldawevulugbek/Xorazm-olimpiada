<template>
  <div class="xorazm-backdrop" :class="`is-${variant}`" aria-hidden="true">
    <div class="xb-sky"></div>
    <div class="xb-tiles"></div>
    <div class="xb-skyline"></div>
    <div class="xb-cubes">
      <div v-for="cube in cubes" :key="cube.id" class="xb-cube-wrap" :style="cube.style">
        <div class="xb-cube">
          <span v-for="face in faces" :key="face" :class="`xb-face xb-${face}`"></span>
        </div>
      </div>
    </div>
    <div class="xb-sparkles">
      <i v-for="s in sparkles" :key="s.id" :style="s.style"></i>
    </div>
  </div>
</template>

<script setup>
// Butun platforma uchun yengil CSS fon: majolika naqshi, Xiva silueti,
// suzib yuruvchi 3D kublar va yulduzchalar. WebGL talab qilmaydi.
import { computed } from 'vue'

const props = defineProps({
  variant: { type: String, default: 'full' },
})

const faces = ['front', 'back', 'right', 'left', 'top', 'bottom']

const cubes = computed(() => {
  const list = [
    { left: '2%', top: '4%', size: 54, delay: 0, dur: 22 },
    { left: '88%', top: '12%', size: 40, delay: -6, dur: 26 },
    { left: '92%', top: '78%', size: 64, delay: -12, dur: 30 },
    { left: '4%', top: '90%', size: 36, delay: -3, dur: 20 },
    { left: '48%', top: '6%', size: 28, delay: -9, dur: 24 },
  ]
  const shown = props.variant === 'calm' ? list.slice(0, 3) : list
  return shown.map((c, i) => ({
    id: i,
    style: {
      left: c.left,
      top: c.top,
      '--size': `${c.size}px`,
      animationDelay: `${c.delay}s`,
      animationDuration: `${c.dur}s`,
    },
  }))
})

const sparkles = computed(() => {
  const n = props.variant === 'calm' ? 14 : 32
  return Array.from({ length: n }, (_, i) => ({
    id: i,
    style: {
      left: `${(i * 37) % 100}%`,
      top: `${(i * 53) % 100}%`,
      animationDelay: `${(i % 7) * -0.9}s`,
      animationDuration: `${3 + (i % 5)}s`,
    },
  }))
})
</script>
