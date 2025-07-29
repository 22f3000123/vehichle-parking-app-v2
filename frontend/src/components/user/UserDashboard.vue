<template>
  <div class="user-dashboard">
    <header class="dashboard-header">
      <h1><v-icon name="fa-user-circle" /> User Dashboard</h1>
      <p>Welcome, {{ authStore.user?.name }}!</p>
    </header>

    <div class="dashboard-tabs">
      <button class="tab-button" :class="{ active: activeTab === 'summary' }" @click="activeTab = 'summary'">
        <v-icon name="co-chart" /> Summary
      </button>
      <button class="tab-button" :class="{ active: activeTab === 'parking-lots' }" @click="activeTab = 'parking-lots'">
        <v-icon name="fa-parking" /> Available Lots
      </button>
      <button class="tab-button" :class="{ active: activeTab === 'my-reservations' }"
        @click="activeTab = 'my-reservations'">
        <v-icon name="fa-history" /> My Reservations
      </button>
    </div>

    <div>
      <!-- Summary Tab -->
      <div v-if="activeTab === 'summary'">
        <div v-if="summaryData" class="row g-4">
          <div class="col-md-4">
            <div class="stat-card primary">
              <h5><v-icon name="fa-clock" /> Current Booking</h5>
              <h2>{{ summaryData.current_booking ? 'Active' : 'None' }}</h2>
            </div>
          </div>
          <div class="col-md-4">
            <div class="stat-card info">
              <h5><v-icon name="fa-rupee-sign" /> Total Spent</h5>
              <h2>₹{{ (summaryData.total_amount_spent || 0).toFixed(2) }}</h2>
            </div>
          </div>
          <div class="col-md-4">
            <div class="stat-card success">
              <h5><v-icon name="fa-hourglass-half" /> Total Hours Parked</h5>
              <h2>{{ summaryData.total_hours_parked || 0 }}</h2>
            </div>
          </div>
          <div class="col-md-6">
            <div class="chart-container">
              <Bar v-if="userSummaryChartData" :data="userSummaryChartData" :options="chartOptions" />
            </div>
          </div>
          <div class="col-md-6">
            <div class="details-card">
              <h5><v-icon name="fa-info-circle" /> Parking Stats</h5>
              <ul>
                <li>
                  <span><v-icon name="fa-clock" /> Avg. Duration</span>
                  <span>{{ summaryData.average_booking_duration || 0 }} hrs</span>
                </li>
                <li>
                  <span><v-icon name="fa-star" /> Favorite Lot</span>
                  <span>{{ summaryData.favorite_parking_lot || 'N/A' }}</span>
                </li>
                <li v-if="summaryData.last_booking">
                  <span><v-icon name="fa-calendar" /> Last Booking</span>
                  <span>{{ new Date(summaryData.last_booking).toLocaleString() }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Parking Lots Tab -->
      <div v-if="activeTab === 'parking-lots'" class="tab-pane">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th><v-icon name="fa-warehouse" /> Name</th>
                <th><v-icon name="fa-map-marker-alt" /> Address</th>
                <th><v-icon name="fa-car" /> Available Spots</th>
                <th><v-icon name="fa-rupee-sign" /> Price/hr</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="lot in parkingLots" :key="lot.id">
                <td>{{ lot.name }}</td>
                <td>{{ lot.address }}</td>
                <td>{{ lot.number_of_spots }}</td>
                <td>₹{{ lot.price }}</td>
                <td>
                  <button :disabled="isReserved" class="btn btn-sm btn-success" @click="bookSpot(lot)">
                    <v-icon name="fa-check-circle" /> Book Spot
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- My Reservations Tab -->
      <div v-if="activeTab === 'my-reservations'" class="tab-pane">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th><v-icon name="fa-parking" /> Lot</th>
                <th><v-icon name="fa-sign-in-alt" /> Parked At</th>
                <th><v-icon name="fa-sign-out-alt" /> Left At</th>
                <th><v-icon name="fa-wallet" /> Cost</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="res in userReservations" :key="res.id">
                <td>{{ res.parking_lot_name }}</td>
                <td>{{ new Date(res.parking_timestamp).toLocaleString() }}</td>
                <td>
                  {{
                    res.leaving_timestamp
                      ? new Date(res.leaving_timestamp).toLocaleString()
                      : 'Parked'
                  }}
                </td>
                <td>{{ res.parking_cost ? '₹' + res.parking_cost.toFixed(2) : 'N/A' }}</td>
                <td>
                  <button v-if="!res.leaving_timestamp" class="btn btn-sm btn-warning"
                    @click="releaseParkingSpot(res.id)">
                    <v-icon name="fa-door-open" /> Release
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '../../services/api'
import { useAuthStore } from '../../stores/auth'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'UserDashboard',
  components: { Bar },
  data() {
    return {
      authStore: useAuthStore(),
      activeTab: 'summary',
      parkingLots: [],
      userReservations: [],
      summaryData: null,
    }
  },
  computed: {
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
        scales: {
          y: { beginAtZero: true },
        },
      }
    },
    userSummaryChartData() {
      if (!this.summaryData) return null
      return {
        labels: ['Total Hours', 'Avg. Duration'],
        datasets: [
          {
            label: 'Hours',
            backgroundColor: ['rgba(106, 90, 205, 0.5)', 'rgba(255, 99, 71, 0.5)'],
            borderColor: ['rgba(106, 90, 205, 1)', 'rgba(255, 99, 71, 1)'],
            borderWidth: 1,
            data: [
              this.summaryData.total_hours_parked || 0,
              this.summaryData.average_booking_duration || 0,
            ],
          },
        ],
      }
    },
    isReserved() {
      return this.userReservations.some((res) => !res.leaving_timestamp)
    },
  },
  async created() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      console.log('fetching the data')
      this.fetchParkingLots()
      this.fetchUserReservations()
      this.fetchSummaryData()
    },
    async fetchParkingLots() {
      try {
        const response = await apiClient.get('/user/parking-lots')
        this.parkingLots = response.data
      } catch (error) {
        console.error('Error fetching parking lots:', error)
      }
    },
    async fetchUserReservations() {
      try {
        const response = await apiClient.get('/user/reservations')

        if (response.data.length === 0) {
          this.userReservations = []
          return
        }

        const indexOfNonRelease = response.data.findIndex((res) => res.leaving_timestamp === null)

        const el = response.data.splice(indexOfNonRelease, 1)

        response.data.unshift(el[0])

        this.userReservations = response.data
      } catch (error) {
        console.error('Error fetching user reservations:', error)
        this.userReservations = []
      }
    },
    async fetchSummaryData() {
      try {
        const response = await apiClient.get('/user/summary-charts')
        this.summaryData = response.data
      } catch (error) {
        console.error('Error fetching summary data:', error)
      }
    },
    async bookSpot(lot) {
      try {
        const response = await apiClient.post(`/user/parking-lots/${lot.id}/book`)
        this.fetchData()
        toast.success(response.data.message)
      } catch (error) {
        toast.error(error.response?.data?.message || 'Booking failed.')
      }
    },
    async releaseParkingSpot(reservationId) {
      try {
        const response = await apiClient.post(`/user/reservations/${reservationId}/release`)
        this.$router.push({
          name: 'payment',
          params: { resId: reservationId, parkingCost: response.data.parking_cost.toFixed(2) },
        })
      } catch (error) {
        toast.error(error.response?.data?.message || 'Failed to release spot.')
      }
    },
  },
}
</script>

<style scoped>
:root {
  --primary-color: #6a5acd;
  --glass-bg: rgba(255, 255, 255, 0.1);
  --glass-border: rgba(255, 255, 255, 0.2);
}

.user-dashboard {
  padding: 2rem;
  background: linear-gradient(120deg, #f0f2f5, #e6eaf0);
  min-height: 100vh;
  animation: fadeIn 0.8s ease-in-out;
}

.dashboard-header {
  text-align: center;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  animation: slideFadeIn 0.6s ease-out;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--primary-color);
}

.dashboard-header p {
  color: #555;
  font-size: 1.2rem;
}

.dashboard-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  justify-content: center;
  flex-wrap: wrap;
}

.tab-button {
  background: #fff;
  border: 2px solid transparent;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  color: #555;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.05);
}

.tab-button:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  transform: translateY(-2px);
}

.tab-button.active {
  background: var(--primary-color);
  color: #fff;
  border-color: var(--primary-color);
}

.stat-card {
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  animation: popIn 0.4s ease forwards;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.stat-card.primary {
  background: linear-gradient(135deg, #6a5acd, #836fff);
}

.stat-card.success {
  background: linear-gradient(135deg, #28a745, #70e000);
}

.stat-card.warning {
  background: linear-gradient(135deg, #ffc107, #f7b500);
}

.stat-card.info {
  background: linear-gradient(135deg, #17a2b8, #00c2cb);
}

.chart-container {
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  height: 350px;
  box-shadow: 0 5px 14px rgba(0, 0, 0, 0.05);
  animation: fadeInUp 0.5s ease-out;
}

.lot-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  animation: fadeInUp 0.6s ease;
}

.lot-card:hover {
  transform: scale(1.03);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.table-responsive {
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 5px 14px rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.5s ease;
}

.modal-content {
  border-radius: 12px;
  animation: zoomIn 0.3s ease;
}

.modal-backdrop.show {
  opacity: 0.5 !important;
}

.btn-close {
  transition: transform 0.2s ease;
}

.btn-close:hover {
  transform: scale(1.1);
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideFadeIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes popIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes zoomIn {
  from {
    transform: scale(0.8);
    opacity: 0.6;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

.table-hover tbody tr:hover {
  background-color: rgba(106, 90, 205, 0.1);
  transition: background-color 0.2s ease-in-out;
}

.details-card {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 5px 14px rgba(0, 0, 0, 0.05);
  animation: fadeInUp 0.5s ease-out;
}

.details-card h5 {
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.details-card ul {
  list-style: none;
  padding: 0;
}

.details-card li {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
  font-weight: 500;
}
</style>
