// v-tilt: kartani sichqoncha tomonga 3D egadi (faqat sichqonchali qurilmalarda).
const canTilt = () =>
  typeof window !== 'undefined' &&
  window.matchMedia('(pointer: fine)').matches &&
  !window.matchMedia('(prefers-reduced-motion: reduce)').matches

export default {
  mounted(el, binding) {
    if (!canTilt()) return
    const max = Number(binding.value) || 8
    el.classList.add('tilt-3d')
    const onMove = (event) => {
      const rect = el.getBoundingClientRect()
      const x = (event.clientX - rect.left) / rect.width - 0.5
      const y = (event.clientY - rect.top) / rect.height - 0.5
      el.style.setProperty('--tilt-x', `${(-y * max).toFixed(2)}deg`)
      el.style.setProperty('--tilt-y', `${(x * max).toFixed(2)}deg`)
      el.style.setProperty('--glare-x', `${((x + 0.5) * 100).toFixed(1)}%`)
      el.style.setProperty('--glare-y', `${((y + 0.5) * 100).toFixed(1)}%`)
    }
    const onLeave = () => {
      el.style.setProperty('--tilt-x', '0deg')
      el.style.setProperty('--tilt-y', '0deg')
    }
    el.addEventListener('pointermove', onMove)
    el.addEventListener('pointerleave', onLeave)
    el._tiltCleanup = () => {
      el.removeEventListener('pointermove', onMove)
      el.removeEventListener('pointerleave', onLeave)
    }
  },
  unmounted(el) {
    el._tiltCleanup?.()
  },
}
