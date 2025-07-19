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
        <h2 class="mt-4">My Parking Summary</h2>
        <div v-if="summaryData">
          <p><strong>Total Bookings:</strong> {{ summaryData.total_bookings }}</p>
          <p>
            <strong>Total Amount Spent:</strong>
            {{
              summaryData.total_amount_spent ? summaryData.total_amount_spent.toFixed(2) : '0.00'
            }}
          </p>
          <p>
            <strong>Most Used Parking Lot:</strong> {{ summaryData.most_used_parking_lot || 'N/A' }}
          </p>

          <div class="chart-container mt-4">
            <h4 class="mb-3">Parking Activity Summary</h4>
            <Bar v-if="userSummaryChartData" :data="userSummaryChartData" :options="chartOptions" />
          </div>
        </div>
        <p v-else>Loading summary data...</p>
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
      },
    }
  },
  computed: {
    userSummaryChartData() {
      if (!this.summaryData) {
        return null
      }
      return {
        labels: ['Total Bookings', 'Total Amount Spent'],
        datasets: [
          {
            label: 'Value',
            backgroundColor: ['#007bff', '#28a745'],
            data: [this.summaryData.total_bookings, this.summaryData.total_amount_spent],
          },
        ],
      }
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
        alert(response.data.message + `\nParking Cost: ${response.data.parking_cost.toFixed(2)}`)

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
