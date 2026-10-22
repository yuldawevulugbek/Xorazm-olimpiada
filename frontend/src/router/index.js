import { createRouter, createWebHistory } from 'vue-router'
import AdminLogin from '../views/AdminLogin.vue'
import AdminLayout from '../views/AdminLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import AdminUsers from '../views/AdminUsers.vue'
import CreateStudent from '../views/CreateStudent.vue'
import StudentsList from '../views/StudentsList.vue'
import ImportStudents from '../views/ImportStudents.vue'
import Results from '../views/Results.vue'
import MentalAnswers from '../views/MentalAnswers.vue'
import Questions from '../views/Questions.vue'
import HackerConsole from '../views/HackerConsole.vue'
import StudentCodeLogin from '../views/StudentCodeLogin.vue'
import ExamPage from '../views/ExamPage.vue'
import { getStoredAdminProfile, isMainAdmin } from '../utils/auth'

const routes = [
  { path: '/', redirect: '/student' },
  { path: '/student', component: StudentCodeLogin },
  { path: '/exam', component: ExamPage },
  { path: '/admin/login', component: AdminLogin },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard', component: Dashboard },
      { path: 'admins', component: AdminUsers, meta: { mainAdminOnly: true } },
      { path: 'students/create', component: CreateStudent },
      { path: 'students', component: StudentsList },
      { path: 'students/import', component: ImportStudents },
      { path: 'results', component: Results },
      { path: 'mental-answers', component: MentalAnswers },
      { path: 'questions', component: Questions },
      { path: 'hacker', component: HackerConsole, meta: { mainAdminOnly: true } },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // Yangi sahifa doim tepadan ochiladi (masalan, ro'yxatdan o'tgach test 1-savoldan boshlanadi).
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0, left: 0 }
  },
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth) && !localStorage.getItem('access')) {
    next('/admin/login')
    return
  }

  if (to.matched.some(record => record.meta.mainAdminOnly)) {
    const profile = getStoredAdminProfile()
    if (!isMainAdmin(profile)) {
      next('/admin/students')
      return
    }
  }

  next()
})

export default router
