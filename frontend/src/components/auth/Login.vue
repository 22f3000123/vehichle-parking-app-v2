<template>
  <div class="login-container">
    <div class="row g-0 min-vh-100">
      <!-- Left side - Image (hidden on mobile) -->
      <div class="col-lg-6 d-none d-lg-block">
        <div class="image-container">
          <img
            src="https://images.unsplash.com/photo-1744359678374-4769eacf44d6?q=80&w=1064&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            alt="Login Background"
            class="login-image"
          />
          <div class="image-overlay">
            <div class="overlay-content">
              <h2>Welcome Back</h2>
              <p>Sign in to continue to your account</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Right side - Login Form -->
      <div class="col-lg-6 col-12">
        <div class="form-container">
          <div class="login-card">
            <div class="card-header-custom">
              <h3>Login</h3>
              <p class="text-muted">Enter your credentials to access your account</p>
            </div>

            <div class="card-body-custom">
              <form @submit.prevent="login">
                <div class="form-group-custom">
                  <label for="email" class="form-label-custom">Email Address</label>
                  <input
                    type="email"
                    class="form-control-custom"
                    :class="{ error: emailError }"
                    id="email"
                    v-model="email"
                    placeholder="Enter your email"
                    required
                  />
                  <div class="error-message" v-if="emailError">{{ emailError }}</div>
                </div>

                <div class="form-group-custom">
                  <label for="password" class="form-label-custom">Password</label>
                  <input
                    type="password"
                    class="form-control-custom"
                    :class="{ error: passwordError }"
                    id="password"
                    v-model="password"
                    placeholder="Enter your password"
                    required
                  />
                  <div class="error-message" v-if="passwordError">{{ passwordError }}</div>
                </div>

                <button type="submit" class="btn-login">
                  <span>Sign In</span>
                </button>

                <div v-if="loginError" class="alert-custom">
                  {{ loginError }}
                </div>
              </form>

              <div class="form-footer">
                <a href="#" class="forgot-link">Forgot your password?</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../../stores/auth'
import apiClient from '../../services/api'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    return { authStore, router }
  },
  data() {
    return {
      email: '',
      password: '',
      emailError: '',
      passwordError: '',
      loginError: '',
    }
  },
  methods: {
    validateForm() {
      this.emailError = ''
      this.passwordError = ''
      this.loginError = ''
      let isValid = true

      if (!this.email) {
        this.emailError = 'Email is required.'
        isValid = false
      } else if (!/^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/.test(this.email)) {
        this.emailError = 'Invalid email format.'
        isValid = false
      }

      if (!this.password) {
        this.passwordError = 'Password is required.'
        isValid = false
      }

      return isValid
    },

    async login() {
      if (!this.validateForm()) {
        return
      }

      try {
        const response = await apiClient.post('/login', {
          email: this.email,
          password: this.password,
        })

        console.log('User logged in:', response)

        if (response.status === 200) {
          const user = response.data.user
          this.authStore.setUser(user)

          if (this.authStore.isAdmin) {
            this.router.push('/admin/dashboard')
          } else {
            this.router.push('/user/dashboard')
          }
        }
      } catch (error) {
        console.error('Login failed:', error)
        this.$toast.error('Login failed. Please check your credentials.')
        this.loginError =
          error.response?.data?.message || 'Login failed. Please check your credentials.'
      }
    },
  },
}
</script>

<style scoped>
/* Container Styles */
.login-container {
  font-family:
    'Inter',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Image Section */
.image-container {
  position: relative;
  height: 100vh;
  overflow: hidden;
}

.login-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.3));
  display: flex;
  align-items: center;
  justify-content: center;
}

.overlay-content {
  text-align: center;
  color: white;
  padding: 2rem;
}

.overlay-content h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.overlay-content p {
  font-size: 1.1rem;
  opacity: 0.9;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

/* Form Container */
.form-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Login Card */
.login-card {
  background: white;
  border-radius: 16px;
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  width: 100%;
  max-width: 450px;
  overflow: hidden;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.login-card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 25px 30px -5px rgba(0, 0, 0, 0.15),
    0 15px 15px -5px rgba(0, 0, 0, 0.08);
}

/* Card Header */
.card-header-custom {
  padding: 2.5rem 2.5rem 1rem;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.card-header-custom h3 {
  color: #1f2937;
  font-size: 1.875rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  letter-spacing: -0.025em;
}

.card-header-custom p {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

/* Card Body */
.card-body-custom {
  padding: 2.5rem;
}

/* Form Groups */
.form-group-custom {
  margin-bottom: 1.5rem;
}

.form-label-custom {
  display: block;
  color: #374151;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  letter-spacing: 0.025em;
}

/* Form Controls */
.form-control-custom {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  background-color: #fafafa;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-control-custom:focus {
  outline: none;
  border-color: #667eea;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-control-custom.error {
  border-color: #ef4444;
  background-color: #fef2f2;
}

.form-control-custom.error:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.form-control-custom::placeholder {
  color: #9ca3af;
}

/* Error Messages */
.error-message {
  color: #ef4444;
  font-size: 0.75rem;
  margin-top: 0.5rem;
  font-weight: 500;
}

/* Login Button */
.btn-login {
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.875rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-login:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.btn-login:active {
  transform: translateY(0);
}

.btn-login::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-login:hover::before {
  left: 100%;
}

/* Alert */
.alert-custom {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.875rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  margin-top: 1rem;
  font-weight: 500;
}

/* Form Footer */
.form-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.forgot-link {
  color: #667eea;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: color 0.2s ease;
}

.forgot-link:hover {
  color: #5a67d8;
  text-decoration: underline;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .form-container {
    padding: 1rem;
    background: white;
  }

  .login-card {
    box-shadow: none;
    border-radius: 0;
  }

  .card-header-custom,
  .card-body-custom {
    padding: 1.5rem;
  }

  .card-header-custom h3 {
    font-size: 1.5rem;
  }
}

@media (max-width: 576px) {
  .card-header-custom,
  .card-body-custom {
    padding: 1rem;
  }

  .overlay-content h2 {
    font-size: 2rem;
  }

  .overlay-content p {
    font-size: 1rem;
  }
}

/* Animation for form elements */
.form-group-custom {
  animation: slideUp 0.6s ease forwards;
}

.form-group-custom:nth-child(1) {
  animation-delay: 0.1s;
}

.form-group-custom:nth-child(2) {
  animation-delay: 0.2s;
}

.btn-login {
  animation: slideUp 0.6s ease forwards;
  animation-delay: 0.3s;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
