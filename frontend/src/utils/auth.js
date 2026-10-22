import api from '../api/axios'

export function getStoredAdminProfile() {
  try {
    return JSON.parse(localStorage.getItem('admin_profile') || 'null')
  } catch {
    return null
  }
}

export function storeAdminProfile(profile) {
  localStorage.setItem('admin_profile', JSON.stringify(profile || {}))
  return profile
}

export async function fetchCurrentAdmin() {
  const res = await api.get('/accounts/me/')
  return storeAdminProfile(res.data)
}

export function clearAuthStorage() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  localStorage.removeItem('admin_profile')
}

export function isMainAdmin(profile) {
  return Boolean(profile?.is_main_admin || profile?.can_manage_admins)
}
