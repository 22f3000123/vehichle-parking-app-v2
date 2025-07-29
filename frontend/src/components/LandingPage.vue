<template>
  <div class="secure-parking-homepage">
    <header class="header">
      <div class="container">
        <nav class="navbar navbar-expand-lg navbar-dark">
          <a class="navbar-brand" href="#"> ParkSmart </a>
          <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
            <ul class="navbar-nav">
              <li class="nav-item">
                <router-link to="/user/dashboard" class="btn btn-primary">Book Parking</router-link>
              </li>
            </ul>
          </div>
        </nav>
      </div>
    </header>

    <section class="hero-section">
      <div class="container">
        <div class="hero-content text-center text-white">
          <h1 class="hero-title">ParkSmart</h1>
          <p class="hero-subtitle">
            The future of hassle-free vehicle parking is here. Find, book, and manage your parking
            spots with ease.
          </p>
          <router-link to="/user/dashboard" class="btn btn-primary">Get Started</router-link>
        </div>
      </div>
    </section>

    <section class="why-us-section py-5">
      <div class="container">
        <h2 class="text-center mb-5">WHY US?</h2>
        <div class="row text-center">
          <div class="col-md-4">
            <div class="feature-card">
              <img
                src="https://images.pexels.com/photos/1036808/pexels-photo-1036808.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
                alt="Superior Service"
                class="feature-icon"
              />
              <h3>Superior Service</h3>
              <p>
                With 40 years of local and international experience and insight from operating
                thousands of car parks.
              </p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card">
              <img
                src="https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
                alt="Innovative Technology"
                class="feature-icon"
              />
              <h3>Innovative Technology</h3>
              <p>
                Through "SecureTech", our in-house IT development centre, we ensure continuous
                innovation.
              </p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card">
              <img
                src="https://images.pexels.com/photos/3184325/pexels-photo-3184325.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
                alt="End-to-End Solution"
                class="feature-icon"
              />
              <h3>End-to-End Solution</h3>
              <p>
                For traffic, revenue and parking management that generates enhanced returns for our
                clients.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="metrics-section py-5 text-white">
      <div class="container">
        <div class="row text-center">
          <div class="col-md-4 mb-4">
            <h2 class="metric-number">250</h2>
            <p class="metric-text">OPERATING CAR PARKS</p>
          </div>
          <div class="col-md-4 mb-4">
            <h2 class="metric-number">38</h2>
            <p class="metric-text">CITIES (Global Presence)</p>
          </div>
          <div class="col-md-4 mb-4">
            <h2 class="metric-number">5000</h2>
            <p class="metric-text">EMPLOYEES</p>
          </div>
          <div class="col-md-4 mb-4">
            <h2 class="metric-number">7.5 Million</h2>
            <p class="metric-text">VEHICLES HANDLED PER MONTH</p>
          </div>
          <div class="col-md-4 mb-4">
            <h2 class="metric-number">2,75,000</h2>
            <p class="metric-text">VEHICLE BAYS</p>
          </div>
          <div class="col-md-4 mb-4">
            <h2 class="metric-number">Rs.350 Crore</h2>
            <p class="metric-text">ANNUAL CAR PARK REVENUE</p>
          </div>
        </div>
      </div>
    </section>

    <section class="about-us-section py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-6">
            <img
              src="https://images.unsplash.com/photo-1635704764831-082c47202c6c?q=80&w=2073&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              alt="About Us"
              class="img-fluid rounded"
            />
          </div>
          <div class="col-md-6">
            <h2>About Us</h2>
            <p>
              Established in 1979, ParkSmart is a global leader in providing comprehensive car park
              management solutions. With a presence in 12 countries, managing over 2000 car parks
              and 2.5 million parking spaces worldwide, we bring unparalleled expertise to the
              Indian market.
            </p>
            <p>
              In India, ParkSmart has been a pioneer for the past 16 years, with offices in Mumbai,
              Delhi NCR, and Bengaluru. We currently manage over 250,000 parking bays across various
              facilities, including airports, shopping malls, hospitals, hotels, and corporate
              buildings.
            </p>
            <p>
              Our philosophy is centered on balancing revenue enhancement for our clients with
              superior customer service for parking patrons.
            </p>
            <a href="#" class="btn btn-outline-primary">Read More</a>
          </div>
        </div>
      </div>
    </section>

    <footer class="footer py-4">
      <div class="container text-center text-white">
        <div class="footer-links mb-3">
          <a href="#">Australia</a> | <a href="#">China</a> | <a href="#">Indonesia</a> |
          <a href="#">Lebanon</a> | <a href="#">Malaysia</a> | <a href="#">New Zealand</a> |
          <a href="#">Singapore</a> | <a href="#">UAE</a> | <a href="#">United Kingdom</a> |
          <a href="#">USA</a>
        </div>
        <p>&copy; 2020 ParkSmart. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'SecureParkingHomepage',
  mounted() {
    // Bootstrap JS is usually initialized globally or imported in main.js
    // If you need specific Bootstrap JS features (like togglers, carousels),
    // ensure Bootstrap's JS bundle is included in your project.
  },
}
</script>

<style scoped>
.secure-parking-homepage {
  font-family: Arial, sans-serif;
  color: var(--dark-color);
}

/* Header */
.header {
  color: black;
}

.header .navbar-brand {
  color: black;
  font-size: 1.8rem;
  font-weight: bold;
}

.header .nav-link {
  color: black;
  margin-left: 15px;
}

/* Hero Section */
.hero-section {
  /* Updated background image */
  background:
    linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url('https://images.unsplash.com/photo-1495435229349-e86db7bfa013?q=80&w=2877&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
      no-repeat center center/cover;
  height: 770px;
  /* Adjust as needed */
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  position: relative;
}

.hero-section .container {
  z-index: 1;
  /* Ensure content is above overlay */
}

.hero-section h1 {
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.hero-section p {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.hero-section .btn {
  padding: 1rem 2rem;
  font-size: 1.2rem;
}

/* Why Us Section */
.why-us-section {
  background-color: var(--light-color);
}

.why-us-section h2 {
  color: var(--dark-color);
  font-weight: bold;
}

.why-us-section .feature-card {
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
  height: 100%;
  /* Ensure cards are same height */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.why-us-section .feature-card:hover {
  transform: translateY(-10px);
}

.why-us-section .feature-icon {
  width: 80px;
  /* Adjust icon size */
  height: 80px;
  margin-bottom: 1rem;
  object-fit: cover;
  /* Ensures image covers the area without distortion */
  border-radius: 50%;
  /* Make it circular if desired for icons */
}

.why-us-section h3 {
  font-size: 1.8rem;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.why-us-section p {
  font-size: 1rem;
  color: var(--secondary-color);
}

/* Key Metrics Section */
.metrics-section {
  background-color: var(--primary-color);
  /* Use a distinct color */
  color: white;
  padding: 4rem 0;
}

.metrics-section .metric-number {
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.metrics-section .metric-text {
  font-size: 1.2rem;
  text-transform: uppercase;
}

/* About Us Section */
.about-us-section h2 {
  color: var(--dark-color);
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.about-us-section p {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.about-us-section .btn {
  margin-top: 1rem;
}

/* Our Services Section */
.our-services-section {
  background-color: var(--light-color);
}

.our-services-section h2 {
  color: var(--dark-color);
  font-weight: bold;
}

.our-services-section .service-card {
  background-color: white;
  border: 1px solid #ddd;
  min-height: 200px;
  /* Ensure consistent card height */
}

.our-services-section .service-card h3 {
  color: var(--primary-color);
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

/* Find Parking Section */
.find-parking-section {
  background-color: var(--dark-color);
  /* Dark background for this section */
  padding: 4rem 0;
}

.find-parking-section h2 {
  font-weight: bold;
  margin-bottom: 2rem;
}

.find-parking-section p {
  font-size: 1.2rem;
}

/* Our Clients Section */
.our-clients-section h2 {
  color: var(--dark-color);
  font-weight: bold;
}

.client-logos img {
  max-width: 150px;
  /* Adjust as needed */
  height: auto;
  margin: 15px;
  filter: grayscale(100%);
  /* Often client logos are desaturated */
  transition: filter 0.3s ease-in-out;
}

.client-logos img:hover {
  filter: grayscale(0%);
}

/* Club Secure Section */
.club-secure-section {
  background:
    linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
    url('https://images.unsplash.com/photo-1543616644-8d48c8b6b0c9?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
      no-repeat center center/cover;
  padding: 5rem 0;
}

.club-secure-section h2 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
}

/* Media Gallery Section */
.media-gallery-section h2 {
  color: var(--dark-color);
  font-weight: bold;
}

.media-card {
  border: none;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
}

.media-card:hover {
  transform: translateY(-5px);
}

.media-card .card-img-top {
  height: 200px;
  object-fit: cover;
}

.media-card .card-body {
  padding: 1.5rem;
}

.media-card .card-title {
  font-size: 1.2rem;
  font-weight: bold;
  min-height: 60px;
  /* Ensure consistent title height */
}

.media-card .btn-link {
  color: var(--primary-color);
  text-decoration: none;
}

/* Footer */
.footer {
  background-color: black;
  color: black;
}

.footer-links a {
  color: white;
  text-decoration: none;
  margin: 0 5px;
}

.footer-links a:hover {
  text-decoration: underline;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2.5rem;
  }

  .hero-section p {
    font-size: 1.2rem;
  }

  .metrics-section .metric-number {
    font-size: 2.5rem;
  }

  .metrics-section .metric-text {
    font-size: 1rem;
  }

  .club-secure-section h2 {
    font-size: 1.8rem;
  }
}
</style>
