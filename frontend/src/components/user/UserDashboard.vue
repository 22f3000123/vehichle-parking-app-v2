<template>
  <div class="user-dashboard">
    <h1>User Dashboard</h1>
    <p>Welcome, {{ authStore.user?.name }}!</p>
    <ul class="nav nav-tabs" id="userTabs" role="tablist">
      <li class="nav-item" role="presentation">
        <button class="nav-link active" id="parking-lots-tab" data-bs-toggle="tab" data-bs-target="#parking-lots"
          type="button" role="tab" aria-controls="parking-lots" aria-selected="true">
          Parking Lots
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="my-reservations-tab" data-bs-toggle="tab" data-bs-target="#my-reservations"
          type="button" role="tab" aria-controls="my-reservations" aria-selected="false">
          My Reservations
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="summary-tab" data-bs-toggle="tab" data-bs-target="#summary" type="button"
          role="tab" aria-controls="summary" aria-selected="false">
          Summary
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="export-tab" data-bs-toggle="tab" data-bs-target="#export" type="button" role="tab"
          aria-controls="export" aria-selected="false">
          Export Data
        </button>
      </li>
    </ul>

    <div class="tab-content" id="userTabsContent">
      <!-- Parking Lots Tab -->
      <div class="tab-pane fade show active" id="parking-lots" role="tabpanel" aria-labelledby="parking-lots-tab">
        <h2 class="mt-4">Available Parking Lots</h2>
        <div v-if="parkingLots.length > 0">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Address</th>
                <th>Pincode</th>
                <th>Available Spots</th>
                <th>Price per Hour</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="lot in parkingLots" :key="lot.id">
                <td>{{ lot.id }}</td>
                <td>{{ lot.name }}</td>
                <td>{{ lot.address }}</td>
                <td>{{ lot.pincode }}</td>
                <td>{{ lot.number_of_spots }}</td>
                <td>{{ lot.price }}</td>
                <td>
                  <button :disabled="isReserved" class="btn btn-sm btn-success" @click="bookSpot(lot)">
                    Book Spot
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else>No parking lots available.</p>
      </div>

      <!-- My Reservations Tab -->
      <div class="tab-pane fade" id="my-reservations" role="tabpanel" aria-labelledby="my-reservations-tab">
        <h2 class="mt-4">My Parking Reservations</h2>
        <div v-if="userReservations.length > 0">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Reservation ID</th>
                <th>Spot ID</th>
                <th>Parking Lot</th>
                <th>Parking Time</th>
                <th>Leaving Time</th>
                <th>Cost</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="res in userReservations" :key="res.id">
                <td>{{ res.id }}</td>
                <td>{{ res.spot_id }}</td>
                <td>{{ res.parking_lot_name }}</td>
                <td>{{ new Date(res.parking_timestamp).toLocaleString() }}</td>
                <td>
                  {{
                    res.leaving_timestamp ? new Date(res.leaving_timestamp).toLocaleString() : 'N/A'
                  }}
                </td>
                <td>{{ res.parking_cost ? res.parking_cost.toFixed(2) : 'N/A' }}</td>
                <td>
                  <button v-if="!res.leaving_timestamp" class="btn btn-sm btn-warning"
                    @click="releaseParkingSpot(res.id)">
                    Release Spot
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else>You have no parking reservations.</p>
      </div>

      <!-- Summary Tab -->
      <div class="tab-pane fade" id="summary" role="tabpanel" aria-labelledby="summary-tab">
        <h2 class="mt-4 mb-4">My Parking Summary</h2>
        
        <div v-if="summaryData" class="row g-4">
          <!-- Stats Cards -->
          <div class="col-md-6 col-lg-4">
            <div class="card bg-primary text-white h-100">
              <div class="card-body">
                <h5 class="card-title">Current Booking</h5>
                <h2 class="display-5">{{ summaryData.current_booking ? 'Active' : 'None' }}</h2>
              </div>
            </div>
          </div>
          
          <div class="col-md-6 col-lg-4">
            <div class="card bg-info text-white h-100">
              <div class="card-body">
                <h5 class="card-title">Total Amount Spent</h5>
                <h2 class="display-5">₹{{ (summaryData.total_amount_spent || 0).toFixed(2) }}</h2>
              </div>
            </div>
          </div>
          
          <div class="col-md-6 col-lg-4">
            <div class="card bg-success text-white h-100">
              <div class="card-body">
                <h5 class="card-title">Total Hours Parked</h5>
                <h2 class="display-5">{{ summaryData.total_hours_parked || 0 }}</h2>
              </div>
            </div>
          </div>
          
          <!-- Detailed Stats -->
          <div class="col-md-6">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title mb-4">Parking Statistics</h5>
                <div class="list-group list-group-flush">
                  <div class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Total Hours Parked</span>
                    <span class="badge bg-primary rounded-pill">{{ summaryData.total_hours_parked || 0 }} hrs</span>
                  </div>
                  <div class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Average Booking Duration</span>
                    <span class="badge bg-success rounded-pill">{{ summaryData.average_booking_duration || 0 }} hrs</span>
                  </div>
                  <div class="list-group-item">
                    <div class="fw-bold">Favorite Parking Lot</div>
                    <div class="text-muted">{{ summaryData.favorite_parking_lot || 'No parking history' }}</div>
                  </div>
                  <div v-if="summaryData.last_booking" class="list-group-item">
                    <div class="fw-bold">Last Booking</div>
                    <div class="text-muted">{{ new Date(summaryData.last_booking).toLocaleString() }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Chart -->
          <div class="col-md-6">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title mb-4">Booking Overview</h5>
                <div style="height: 250px;">
                  <Bar v-if="userSummaryChartData" :data="userSummaryChartData" :options="chartOptions" />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-3">Loading summary data...</p>
        </div>
      </div>

      <!-- Export Data Tab -->
      <div class="tab-pane fade" id="export" role="tabpanel" aria-labelledby="export-tab">
        <h2 class="mt-4">Export Parking Data</h2>
        <p>Click the button below to export your parking details as a CSV file.</p>
        <button class="btn btn-primary" @click="exportCsv">Export to CSV</button>
        <p v-if="exportMessage" class="mt-3">{{ exportMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '../../services/api'
import { useAuthStore } from '../../stores/auth'
import { Bar } from 'vue-chartjs'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'UserDashboard',
  components: { Bar },
  data() {
    return {
      authStore: useAuthStore(),
      parkingLots: [],
      userReservations: [],
      summaryData: null,
      exportMessage: '',
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1
            }
          }
        }
      },
    }
  },
  computed: {
    userSummaryChartData() {
      if (!this.summaryData) return null;
      
      return {
        labels: ['Total Hours Parked', 'Avg. Duration'],
        datasets: [
          {
            label: 'Hours',
            backgroundColor: ['#4e73df', '#1cc88a'],
            data: [
              this.summaryData.total_hours_parked || 0,
              this.summaryData.average_booking_duration || 0
            ],
            borderWidth: 1
          }
        ]
      };
    },

    isReserved() {
      return this.userReservations.some((reservation) => reservation.leaving_timestamp === null)
    },
  },
  async created() {
    await this.fetchData()
  },
  methods: {
    async fetchData() {
      await this.fetchParkingLots()
      await this.fetchUserReservations()
      await this.fetchSummaryData()
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

        console.log(response.data)

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
        const bookingResponse = await apiClient.post(`/user/parking-lots/${lot.id}/book`)
        if (bookingResponse.status === 201) {
          this.bookingMessage = `Payment successful and spot booked! Spot ID: ${bookingResponse.data.spot_id}`
          this.bookingSucess = true

          toast.success(this.bookingMessage, {
            autoClose: 1000,
          })

          await this.fetchData()
        } else {
          this.bookingMessage = bookingResponse.data.message || 'Failed to book spot after payment.'
          this.bookingSucess = false
        }
      } catch (error) {
        console.error('Booking failed:', error)
        this.bookingMessage = error.response?.data?.message || 'An error occurred during payment.'
        this.bookingSucess = false

        toast.error(this.bookingMessage, {
          autoClose: 1000,
        })
      }
    },
    async releaseParkingSpot(reservationId) {
      try {
        const response = await apiClient.post(`/user/reservations/${reservationId}/release`)
        alert(response.data.message + `\nParking Cost: ₹${response.data.parking_cost.toFixed(2)}`)

        this.$router.push({
          name: 'payment',
          params: {
            resId: reservationId,
            parkingCost: response.data.parking_cost.toFixed(2),
          },
        })
      } catch (error) {
        console.error('Error releasing spot:', error)
        alert(error.response?.data?.message || 'Failed to release parking spot.')
      }
    },
    async exportCsv() {
      try {
        this.exportMessage = 'Initiating CSV export...'
        const response = await apiClient.post('/user/export-parking-details')
        this.exportMessage = response.data.message
      } catch (error) {
        console.error('Error exporting CSV:', error)
        this.exportMessage = error.response?.data?.message || 'Failed to initiate CSV export.'
      }
    },
  },
}
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
  /* Adjust height as needed */
  width: 100%;
}
</style>
