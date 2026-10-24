import axios from 'axios'

const rawBaseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'
// Netlify'da manzil oxiriga /api yozish esdan chiqsa ham ishlaydi:
// https://xxx.up.railway.app  ->  https://xxx.up.railway.app/api
let baseURL = rawBaseURL.trim().replace(/\/+$/, '')
if (!/\/api$/.test(baseURL)) baseURL += '/api'

if (import.meta.env.PROD && /127\.0\.0\.1|localhost/.test(baseURL)) {
  console.error('VITE_API_BASE_URL Netlify sozlamalarida yozilmagan: frontend backendga ulana olmaydi.')
}

// So'rov cheksiz osilib qolmasin: 25 soniyada javob bo'lmasa xato qaytadi.
const api = axios.create({ baseURL, timeout: 25000 })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      const refresh = localStorage.getItem('refresh')
      if (refresh) {
        try {
          const res = await axios.post(`${api.defaults.baseURL}/auth/refresh/`, { refresh })
          localStorage.setItem('access', res.data.access)
          original.headers.Authorization = `Bearer ${res.data.access}`
          return api(original)
        } catch (e) {
          localStorage.removeItem('access')
          localStorage.removeItem('refresh')
          window.location.href = '/admin/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api
