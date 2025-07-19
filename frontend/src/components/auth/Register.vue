<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">Register</div>
          <div class="card-body">
            <form @submit.prevent="register">
              <div class="mb-3">
                <label for="firstName" class="form-label">First Name</label>
                <input type="text" class="form-control" :class="{ 'is-invalid': firstNameError }" id="firstName" v-model="firstName" required>
                <div class="invalid-feedback" v-if="firstNameError">{{ firstNameError }}</div>
              </div>
              <div class="mb-3">
                <label for="lastName" class="form-label">Last Name</label>
                <input type="text" class="form-control" :class="{ 'is-invalid': lastNameError }" id="lastName" v-model="lastName" required>
                <div class="invalid-feedback" v-if="lastNameError">{{ lastNameError }}</div>
              </div>
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" class="form-control" :class="{ 'is-invalid': usernameError }" id="username" v-model="username" required>
                <div class="invalid-feedback" v-if="usernameError">{{ usernameError }}</div>
              </div>
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
              <button type="submit" class="btn btn-primary">Register</button>
              <div v-if="registerError" class="alert alert-danger mt-3">{{ registerError }}</div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '../../services/api';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      firstName: '',
      lastName: '',
      username: '',
      email: '',
      password: '',
      firstNameError: '',
      lastNameError: '',
      usernameError: '',
      emailError: '',
      passwordError: '',
      registerError: ''
    };
  },
  methods: {
    validateForm() {
      this.firstNameError = '';
      this.lastNameError = '';
      this.usernameError = '';
      this.emailError = '';
      this.passwordError = '';
      this.registerError = '';

      let isValid = true;

      if (!this.firstName) {
        this.firstNameError = 'First Name is required.';
        isValid = false;
      }

      if (!this.lastName) {
        this.lastNameError = 'Last Name is required.';
        isValid = false;
      }

      if (!this.username) {
        this.usernameError = 'Username is required.';
        isValid = false;
      }

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
      } else if (this.password.length < 6) {
        this.passwordError = 'Password must be at least 6 characters long.';
        isValid = false;
      }

      return isValid;
    },
    async register() {
      if (!this.validateForm()) {
        return;
      }

      try {
        const response = await apiClient.post('/register', {
          first_name: this.firstName,
          last_name: this.lastName,
          username: this.username,
          email: this.email,
          password: this.password
        });

        if (response.status === 201) {
          this.router.push('/login');
        }
      } catch (error) {
        console.error('Registration failed:', error);
        this.registerError = error.response?.data?.message || 'Registration failed. Please try again.';
      }
    }
  }
};
</script>