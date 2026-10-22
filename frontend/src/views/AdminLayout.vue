<template>
  <div class="admin-shell hacker-admin-shell" :class="{ 'light-admin-shell': isLightMode, 'hacker-fullscreen-shell': isHackerRoute }">
    <div class="hacker-matrix-layer" aria-hidden="true"></div>
    <aside v-if="!isHackerRoute" class="sidebar hacker-sidebar" :class="{ open: menuOpen }">
      <div class="sidebar-brand">
        <div class="brand-circle small brand-icon-only xz-emblem">★</div>
        <div>
          <h2>Xorazm Olimpiadasi</h2>
          <span>Admin · {{ adminTitle }}</span>
        </div>
      </div>

      <nav @click="menuOpen = false">
        <RouterLink to="/admin/dashboard">▸ Dashboard</RouterLink>
        <RouterLink v-if="mainAdmin" to="/admin/admins">▸ Adminlar</RouterLink>
        <RouterLink v-if="currentAdmin?.can_create_students" to="/admin/students/create">▸ O‘quvchi yaratish</RouterLink>
        <RouterLink v-if="currentAdmin?.can_create_students" to="/admin/students/import">▸ Excel yuklash</RouterLink>
        <RouterLink to="/admin/students">▸ Yaratilgan o‘quvchilar</RouterLink>
        <RouterLink to="/admin/questions">▸ Testlar</RouterLink>
        <RouterLink to="/admin/results">▸ Natijalar</RouterLink>
        <RouterLink to="/admin/mental-answers">▸ Mental javoblari</RouterLink>
      </nav>

      <div class="hacker-side-status">
        <span></span> Olimpiada faol
      </div>
      <button class="ghost-btn logout" @click="logout">⏻ Chiqish</button>
    </aside>
    <div v-if="menuOpen && !isHackerRoute" class="xz-menu-overlay" @click="menuOpen = false"></div>

    <main class="admin-main">
      <header v-if="!isHackerRoute" class="topbar hacker-topbar">
        <button class="menu-btn" @click="menuOpen = !menuOpen">☰</button>
        <div class="hacker-title-block">
          <span class="hacker-eyebrow">Xiva · Ichan Qal‘a</span>
          <h1>Xorazm Olimpiadasi</h1>
          <p v-if="mainAdmin">Olimpiada admin paneli va natijalar boshqaruvi</p>
          <p v-else>{{ adminTitle }} o‘quvchilari va natijalari</p>
        </div>
        <div class="hacker-top-actions">
          <RouterLink v-if="mainAdmin" to="/admin/hacker" class="hacker-top-link">Hacker</RouterLink>
          <button class="theme-toggle-btn" type="button" @click="toggleTheme" :title="isLightMode ? 'Kechki rejimga o‘tish' : 'Kunduzgi rejimga o‘tish'">
            <span class="moon-icon">{{ isLightMode ? '🌙' : '☀️' }}</span>
            <b>{{ isLightMode ? 'Xiva kechasi' : 'Kunduz' }}</b>
          </button>
          <span class="hacker-live-dot"><i></i> LIVE</span>
          <RouterLink to="/student" class="student-link">O‘quvchi kirishi</RouterLink>
        </div>
      </header>

      <section class="content-wrap">
        <RouterView />
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { clearAuthStorage, fetchCurrentAdmin, getStoredAdminProfile, isMainAdmin } from '../utils/auth'

const route = useRoute()
const router = useRouter()
const menuOpen = ref(false)
const isLightMode = ref(false)
const currentAdmin = ref(getStoredAdminProfile())
const mainAdmin = computed(() => isMainAdmin(currentAdmin.value))
const adminTitle = computed(() => currentAdmin.value?.center_name || currentAdmin.value?.assigned_center_name || currentAdmin.value?.branch || 'Bosh admin')
const isHackerRoute = computed(() => route.path === '/admin/hacker')

function toggleTheme() {
  isLightMode.value = !isLightMode.value
  localStorage.setItem('admin-theme', isLightMode.value ? 'light' : 'hacker')
}

function logout() {
  clearAuthStorage()
  router.push('/admin/login')
}

onMounted(async () => {
  isLightMode.value = localStorage.getItem('admin-theme') === 'light'

  try {
    currentAdmin.value = await fetchCurrentAdmin()
  } catch {
    clearAuthStorage()
    router.push('/admin/login')
  }
})
</script>
