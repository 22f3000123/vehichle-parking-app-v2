<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">Login</div>
          <div class="card-body">
            <form @submit.prevent="login">
              <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                <input type="email" class="form-control" :class="{ 'is-invalid': emailError }" id="email" v-model="email" required>
                <div class="invalid-feedback" v-if="emailError">{{ emailError }}</div>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" :class="{ 'is-invalid': passwordError }" id="password" v-model="password" required>
                <div class="invalid-feedback" v-if="passwordError">{{ passwordError }}</div>
              </div>
              <button type="submit" class="btn btn-primary">Login</button>
              <div v-if="loginError" class="alert alert-danger mt-3">{{ loginError }}</div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../../stores/auth';
import apiClient from '../../services/api';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    return { authStore, router };
  },
  data() {
    return {
      email: '',
      password: '',
      emailError: '',
      passwordError: '',
      loginError: ''
    };
  },
  methods: {
    validateForm() {
      this.emailError = '';
      this.passwordError = '';
      this.loginError = '';

      let isValid = true;

      if (!this.email) {
        this.emailError = 'Email is required.';
        isValid = false;
      } else if (!/^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/.test(this.email)) {
        this.emailError = 'Invalid email format.';
        isValid = false;
      }

      if (!this.password) {
        this.passwordError = 'Password is required.';
        isValid = false;
      }

      return isValid;
    },
    async login() {
      if (!this.validateForm()) {
        return;
      }

      try {
        const response = await apiClient.post('/login', {
          email: this.email,
          password: this.password
        });
          console.log('User logged in:', response);

        if (response.status === 200) {
          const user = response.data.user;
          this.authStore.setUser(user);



          if (this.authStore.isAdmin) {
            this.router.push('/admin/dashboard');
          } else {
            this.router.push('/user/dashboard');
          }
        }
      } catch (error) {
        console.error('Login failed:', error);
        this.loginError = error.response?.data?.message || 'Login failed. Please check your credentials.';
      }
    }
  }
};
</script>
