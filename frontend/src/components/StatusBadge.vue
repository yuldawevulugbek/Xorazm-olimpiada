<template>
  <span class="status-badge" :class="statusClass">
    <span class="dot"></span>
    {{ label }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: { type: String, required: true }
})

const label = computed(() => {
  return {
    not_started: 'Ishlamagan',
    in_progress: 'Ishlayapti',
    completed: 'Ishlab bo‘ldi'
  }[props.status] || props.status
})

const statusClass = computed(() => `status-${props.status}`)
</script>
