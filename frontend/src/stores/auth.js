import { defineStore } from 'pinia'
import apiClient from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
  }),
  getters: {
    isAdmin: (state) => state.user && state.user.roles && state.user.roles.includes('admin'),
  },
  actions: {
    setUser(user) {
      this.user = user
      this.isAuthenticated = !!user // Set isAuthenticated based on user presence
    },
    async initializeAuth() {
      try {
        const response = await apiClient.get('/me')
        if (response.status === 200 && response.data.id) {
          this.setUser(response.data)
        } else {
          this.logout()
        }
      } catch (error) {
        console.error('Error initializing auth:', error)
        this.logout()
      }
    },
    logout() {
      this.user = null
      this.isAuthenticated = false
    },
  },
})
