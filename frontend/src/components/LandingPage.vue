<template>
  <div class="landing-page">
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">ParkSmart</h1>
        <p class="hero-subtitle">The future of hassle-free vehicle parking is here. Find, book, and manage your parking spots with ease.</p>
        <router-link to="/login" class="btn btn-primary">Get Started</router-link>
      </div>
    </section>

    <section class="features">
      <div class="container">
        <h2 class="section-title">Features</h2>
        <div class="row">
          <div class="col-md-4">
            <div class="feature-card">
              <i class="fas fa-search-location feature-icon"></i>
              <h3 class="feature-title">Find Parking</h3>
              <p class="feature-description">Easily locate available parking lots near you with our interactive map.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card">
              <i class="fas fa-calendar-check feature-icon"></i>
              <h3 class="feature-title">Book Instantly</h3>
              <p class="feature-description">Reserve your parking spot in advance and avoid the last-minute rush.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card">
              <i class="fas fa-history feature-icon"></i>
              <h3 class="feature-title">Manage History</h3>
              <p class="feature-description">Keep track of your parking history and expenses all in one place.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
};
</script>

<style scoped>
.landing-page {
  width: 100%;
}

.hero {
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://images.unsplash.com/photo-1543357485-d847a23584a3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80') no-repeat center center/cover;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
}

.hero-title {
  font-size: 4rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.features {
  padding: 4rem 0;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
}

.feature-card {
  text-align: center;
  padding: 2rem;
  border-radius: 10px;
  background-color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-icon {
  font-size: 3rem;
  color: var(--primary-color);
  margin-bottom: 1.5rem;
}

.feature-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}
</style>
