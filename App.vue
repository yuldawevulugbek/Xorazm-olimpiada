<template>
  <div class="xz">
    <XorazmBackdrop v-if="backdrop" :variant="backdrop" />
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import XorazmBackdrop from './components/XorazmBackdrop.vue'

const route = useRoute()

// Imtihon va admin sahifalarida fon tinchroq, Hacker konsolida o'chiriladi.
const backdrop = computed(() => {
  if (route.path === '/admin/hacker') return ''
  if (route.path === '/exam' || route.path.startsWith('/admin/')) return 'calm'
  return 'full'
})
</script>
