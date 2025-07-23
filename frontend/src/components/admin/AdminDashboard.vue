<template>
  <div class="admin-dashboard">
    <header class="dashboard-header">
      <h1><v-icon name="fa-tools" /> Admin Dashboard</h1>
      <p><v-icon name="fa-user-shield" /> Welcome, Admin!</p>
    </header>

    <div class="dashboard-tabs">
      <button class="tab-button" :class="{ active: activeTab === 'summary' }" @click="activeTab = 'summary'">
        <v-icon name="co-chart" /> Summary
      </button>
      <button class="tab-button" :class="{ active: activeTab === 'parking-lots' }" @click="activeTab = 'parking-lots'">
        <v-icon name="fa-parking" /> Parking Lots
      </button>
      <button class="tab-button" :class="{ active: activeTab === 'users' }" @click="activeTab = 'users'">
        <v-icon name="fa-users" /> Users
      </button>
      <button class="tab-button" :class="{ active: activeTab === 'parking-spots' }"
        @click="activeTab = 'parking-spots'">
        <v-icon name="fa-map-marker-alt" /> Parking Spots
      </button>
    </div>

    <div>
      <!-- Summary Tab -->
      <div v-if="activeTab === 'summary'">
        <div v-if="summaryData" class="row g-4">
          <!-- Stats Cards -->
          <div class="col-md-3">
            <div class="stat-card primary">
              <h5>Total Parking Lots</h5>
              <h2>{{ summaryData.total_parking_lots }}</h2>
            </div>
          </div>
          <div class="col-md-3">
            <div class="stat-card success">
              <h5>Available Spots</h5>
              <h2>{{ summaryData.available_spots }}</h2>
            </div>
          </div>
          <div class="col-md-3">
            <div class="stat-card warning">
              <h5>Occupied Spots</h5>
              <h2>{{ summaryData.occupied_spots }}</h2>
            </div>
          </div>
          <div class="col-md-3">
            <div class="stat-card info">
              <h5>Total Revenue</h5>
              <h2>₹{{ summaryData.total_revenue }}</h2>
            </div>
          </div>

          <!-- Charts -->
          <div class="col-md-8">
            <div class="chart-container">
              <Line v-if="dailyReservationsChartData" :data="dailyReservationsChartData" :options="lineChartOptions" />
            </div>
          </div>
          <div class="col-md-4">
            <div class="chart-container">
              <Pie v-if="spotDistributionChartData" :data="spotDistributionChartData" :options="chartOptions" />
            </div>
          </div>
        </div>
      </div>

      <!-- Parking Lots Tab -->
      <div v-if="activeTab === 'parking-lots'" class="tab-pane">
        <button class="btn btn-primary mb-3" @click="showCreateLotModal = true">
          Create New Parking Lot
        </button>
        <div v-if="parkingLots.length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          <div class="col" v-for="lot in parkingLots" :key="lot.id">
            <div class="lot-card">
              <h5>{{ lot.name }}</h5>
              <p>{{ lot.address }}, {{ lot.pincode }}</p>
              <p>
                <strong>Spots:</strong> {{ lot.number_of_spots }} | <strong>Price:</strong> ₹{{
                  lot.price
                }}/hr
              </p>
              <div class="lot-actions">
                <button class="btn btn-sm btn-info me-2" @click="editParkingLot(lot)">Edit</button>
                <button class="btn btn-sm btn-danger" @click="deleteParkingLot(lot.id)">
                  Delete
                </button>
                <button class="btn btn-sm btn-secondary ms-2" @click="viewParkingLotDetails(lot.id)">
                  View
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Users Tab -->
      <div v-if="activeTab === 'users'" class="tab-pane">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Username</th>
                <th>Email</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.first_name }} {{ user.last_name }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <span class="badge" :class="user.active ? 'bg-success' : 'bg-danger'">{{
                    user.active ? 'Active' : 'Inactive'
                    }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Parking Spots Tab -->
      <div v-if="activeTab === 'parking-spots'" class="tab-pane">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Lot Name</th>
                <th>Spot</th>
                <th>Status</th>
                <th>Reserved By</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="spot in parkingSpots" :key="spot.id">
                <td>{{ spot.id }}</td>
                <td>{{ spot.parking_lot_name }}</td>
                <td>{{ spot.spot_number }}</td>
                <td>
                  <span class="badge" :class="spot.status === 'A' ? 'bg-success' : 'bg-warning'">{{
                    spot.status === 'A' ? 'Available' : 'Occupied'
                    }}</span>
                </td>
                <td>{{ spot.reserved_by ? spot.reserved_by.email : 'N/A' }}</td>
                <td>
                  {{
                    spot.reserved_by
                      ? new Date(spot.reserved_by.parking_timestamp).toLocaleString()
                      : 'N/A'
                  }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" :class="{ show: showCreateLotModal || showEditLotModal }" tabindex="-1"
      :style="{ display: showCreateLotModal || showEditLotModal ? 'block' : 'none' }">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ isEditMode ? 'Edit Parking Lot' : 'Create New Parking Lot' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="isEditMode ? updateParkingLot() : createParkingLot()">
              <div class="mb-3">
                <label for="lotName" class="form-label">Name</label>
                <input type="text" class="form-control" id="lotName" v-model="currentLot.name" required />
              </div>
              <div class="mb-3">
                <label for="lotAddress" class="form-label">Address</label>
                <input type="text" class="form-control" id="lotAddress" v-model="currentLot.address" required />
              </div>
              <div class="mb-3">
                <label for="lotPincode" class="form-label">Pincode</label>
                <input type="text" class="form-control" id="lotPincode" v-model="currentLot.pincode" required />
              </div>
              <div class="mb-3" v-if="!isEditMode">
                <label for="lotSpots" class="form-label">Number of Spots</label>
                <input type="number" class="form-control" id="lotSpots" v-model.number="currentLot.number_of_spots"
                  required min="1" />
              </div>
              <div class="mb-3">
                <label for="lotPrice" class="form-label">Price per Hour</label>
                <input type="number" class="form-control" id="lotPrice" v-model.number="currentLot.price" required
                  step="0.01" min="0" />
              </div>
              <button type="submit" class="btn btn-primary">
                {{ isEditMode ? 'Update' : 'Create' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade" :class="{ show: showCreateLotModal || showEditLotModal }"
      :style="{ display: showCreateLotModal || showEditLotModal ? 'block' : 'none' }"></div>
  </div>
</template>

<script>
import apiClient from '../../services/api'
import { useAuthStore } from '../../stores/auth'
import { Bar, Pie, Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement,
)

export default {
  name: 'AdminDashboard',
  components: { Bar, Pie, Line },
  data() {
    return {
      authStore: useAuthStore(),
      activeTab: 'summary',
      parkingLots: [],
      users: [],
      parkingSpots: [],
      summaryData: null,
      showCreateLotModal: false,
      showEditLotModal: false,
      isEditMode: false,
      currentLot: {
        id: null,
        name: '',
        address: '',
        pincode: '',
        number_of_spots: 0,
        price: 0.0,
      },
    }
  },
  computed: {
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
        },
      }
    },
    lineChartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
        },
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      }
    },
    dailyReservationsChartData() {
      if (!this.summaryData || !this.summaryData.daily_reservations) return null
      const sortedData = [...this.summaryData.daily_reservations].sort(
        (a, b) => new Date(a.date) - new Date(b.date),
      )
      const labels = sortedData.map((day) =>
        new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      )
      const data = sortedData.map((day) => day.count)
      return {
        labels,
        datasets: [
          {
            label: 'Daily Reservations',
            backgroundColor: 'rgba(106, 90, 205, 0.2)',
            borderColor: 'rgba(106, 90, 205, 1)',
            data,
          },
        ],
      }
    },
    spotDistributionChartData() {
      if (!this.summaryData) return null
      return {
        labels: ['Available', 'Occupied'],
        datasets: [
          {
            backgroundColor: ['#32CD32', '#FF6347'],
            data: [this.summaryData.available_spots, this.summaryData.occupied_spots],
          },
        ],
      }
    },
  },
  async created() {
    await this.fetchData()
  },
  async created() {
    await this.fetchData()
  },
  methods: {
    async fetchData() {
      this.fetchParkingLots()
      this.fetchUsers()
      this.fetchParkingSpots()
      this.fetchSummaryData()
    },
    async fetchParkingLots() {
      try {
        const response = await apiClient.get('/admin/parking-lots')
        this.parkingLots = response.data
      } catch (error) {
        console.error('Error fetching parking lots:', error)
      }
    },
    async fetchUsers() {
      try {
        const response = await apiClient.get('/admin/users')
        this.users = response.data
      } catch (error) {
        console.error('Error fetching users:', error)
      }
    },
    async fetchParkingSpots() {
      try {
        const response = await apiClient.get('/admin/parking-spots')
        this.parkingSpots = response.data
      } catch (error) {
        console.error('Error fetching parking spots:', error)
      }
    },
    async fetchSummaryData() {
      try {
        const response = await apiClient.get('/admin/summary-charts')
        this.summaryData = response.data
      } catch (error) {
        console.error('Error fetching summary data:', error)
      }
    },
    async createParkingLot() {
      try {
        await apiClient.post('/admin/parking-lots', this.currentLot)
        this.closeModal()
        this.fetchData()
        toast.success('Parking lot created successfully!')
      } catch (error) {
        console.error('Error creating parking lot:', error)
        toast.error('Failed to create parking lot.')
      }
    },
    editParkingLot(lot) {
      this.isEditMode = true
      this.currentLot = { ...lot }
      this.showEditLotModal = true
    },
    async updateParkingLot() {
      try {
        await apiClient.put(`/admin/parking-lots/${this.currentLot.id}`, this.currentLot)
        this.closeModal()
        this.fetchData()
        toast.success('Parking lot updated successfully!')
      } catch (error) {
        console.error('Error updating parking lot:', error)
        toast.error('Failed to update parking lot.')
      }
    },
    async deleteParkingLot(lotId) {
      if (confirm('Are you sure?')) {
        try {
          await apiClient.delete(`/admin/parking-lots/${lotId}`)
          this.fetchData()
          toast.success('Parking lot deleted successfully!')
        } catch (error) {
          console.error('Error deleting parking lot:', error)
          toast.error(error.response?.data?.message || 'Failed to delete parking lot.')
        }
      }
    },
    closeModal() {
      this.showCreateLotModal = false
      this.showEditLotModal = false
      this.isEditMode = false
      this.currentLot = {
        id: null,
        name: '',
        address: '',
        pincode: '',
        number_of_spots: 0,
        price: 0.0,
      }
    },
    viewParkingLotDetails(lotId) {
      this.$router.push({ name: 'admin-parking-lot-details', params: { lotId } })
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

.admin-dashboard {
  padding: 2rem;
  background: linear-gradient(120deg, #f0f2f5, #e6eaf0);
  min-height: 100vh;
  width: 100%;
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
</style>
