import { ref } from 'vue'
import api from '../api/axios'

const centers = ref([])
const centerSummaries = ref([])

export function useCenters() {
  async function loadCenters() {
    const res = await api.get('/centers/')
    centers.value = res.data || []
    return centers.value
  }

  async function loadCenterSummaries() {
    const res = await api.get('/centers/summary/')
    centerSummaries.value = res.data || []
    return centerSummaries.value
  }

  async function addCenter(name) {
    const cleanName = String(name || '').trim()
    if (!cleanName) throw new Error('O‘quv markaz nomini kiriting.')
    const res = await api.post('/centers/', { name: cleanName })
    const saved = res.data
    if (!centers.value.some(center => Number(center.id) === Number(saved.id))) {
      centers.value.push(saved)
      centers.value.sort((a, b) => a.name.localeCompare(b.name))
    }
    return saved
  }

  return { centers, centerSummaries, loadCenters, loadCenterSummaries, addCenter }
}
