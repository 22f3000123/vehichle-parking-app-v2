<template>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>
    <p>Welcome, Admin!</p>

    <ul class="nav nav-tabs" id="adminTabs" role="tablist">
      <li class="nav-item" role="presentation">
        <button class="nav-link active" id="parking-lots-tab" data-bs-toggle="tab" data-bs-target="#parking-lots" type="button" role="tab" aria-controls="parking-lots" aria-selected="true">Parking Lots</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="users-tab" data-bs-toggle="tab" data-bs-target="#users" type="button" role="tab" aria-controls="users" aria-selected="false">Users</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="parking-spots-tab" data-bs-toggle="tab" data-bs-target="#parking-spots" type="button" role="tab" aria-controls="parking-spots" aria-selected="false">Parking Spots</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="summary-tab" data-bs-toggle="tab" data-bs-target="#summary" type="button" role="tab" aria-controls="summary" aria-selected="false">Summary</button>
      </li>
    </ul>

    <div class="tab-content" id="adminTabsContent">
      <!-- Parking Lots Tab -->
      <div class="tab-pane fade show active" id="parking-lots" role="tabpanel" aria-labelledby="parking-lots-tab">
        <h2 class="mt-4">Manage Parking Lots</h2>
        <button class="btn btn-primary mb-3" @click="showCreateLotModal = true">Create New Parking Lot</button>

        <div v-if="parkingLots.length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          <div class="col" v-for="lot in parkingLots" :key="lot.id">
            <div class="card h-100 shadow-sm">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title">{{ lot.name }}</h5>
                <p class="card-text mb-1"><strong>Address:</strong> {{ lot.address }}</p>
                <p class="card-text mb-1"><strong>Pincode:</strong> {{ lot.pincode }}</p>
                <p class="card-text mb-1"><strong>Spots:</strong> {{ lot.number_of_spots }}</p>
                <p class="card-text mb-3"><strong>Price:</strong> ${{ lot.price }}</p>
                <div class="mt-auto">
                  <button class="btn btn-sm btn-info me-2" @click="editParkingLot(lot)">Edit</button>
                  <button class="btn btn-sm btn-danger" @click="deleteParkingLot(lot.id)">Delete</button>
                  <button class="btn btn-sm btn-primary ms-2" @click="viewParkingLotDetails(lot.id)">View Details</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <p v-else>No parking lots found.</p>
      </div>

      <!-- Users Tab -->
      <div class="tab-pane fade" id="users" role="tabpanel" aria-labelledby="users-tab">
        <h2 class="mt-4">Registered Users</h2>
        <div v-if="users.length > 0">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Username</th>
                <th>Email</th>
                <th>Active</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.first_name }}</td>
                <td>{{ user.last_name }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.active ? 'Yes' : 'No' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else>No users found.</p>
      </div>

      <!-- Parking Spots Tab -->
      <div class="tab-pane fade" id="parking-spots" role="tabpanel" aria-labelledby="parking-spots-tab">
        <h2 class="mt-4">Parking Spot Status</h2>
        <div v-if="parkingSpots.length > 0">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Lot Name</th>
                <th>Spot Number</th>
                <th>Status</th>
                <th>Reserved By</th>
                <th>Parking Timestamp</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="spot in parkingSpots" :key="spot.id">
                <td>{{ spot.id }}</td>
                <td>{{ spot.parking_lot_name }}</td>
                <td>{{ spot.spot_number }}</td>
                <td>{{ spot.status === 'A' ? 'Available' : 'Occupied' }}</td>
                <td>{{ spot.reserved_by ? spot.reserved_by.email : 'N/A' }}</td>
                <td>{{ spot.reserved_by ? new Date(spot.reserved_by.parking_timestamp).toLocaleString() : 'N/A' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else>No parking spots found.</p>
      </div>

      <!-- Summary Tab -->
      <div class="tab-pane fade" id="summary" role="tabpanel" aria-labelledby="summary-tab">
        <h2 class="mt-4">Summary Charts</h2>
        <div v-if="summaryData">
          <p><strong>Total Parking Lots:</strong> {{ summaryData.total_parking_lots }}</p>
          <p><strong>Total Spots:</strong> {{ summaryData.total_spots }}</p>
          <p><strong>Available Spots:</strong> {{ summaryData.available_spots }}</p>
          <p><strong>Occupied Spots:</strong> {{ summaryData.occupied_spots }}</p>
          <p><strong>Total Reservations:</strong> {{ summaryData.total_reservations }}</p>

          <h3 class="mt-4">Parking Lot Occupancy Breakdown</h3>
          <ul class="list-group">
            <li class="list-group-item" v-for="lot in summaryData.parking_lot_occupancy" :key="lot.lot_id">
              <strong>{{ lot.lot_name }} (ID: {{ lot.lot_id }})</strong>: Total Spots: {{ lot.total_spots }}, Occupied: {{ lot.occupied_spots }}, Available: {{ lot.available_spots }}
            </li>
          </ul>

          <div class="chart-container mt-4">
            <h4 class="mb-3">Parking Lot Occupancy Chart</h4>
            <Bar
              v-if="parkingLotOccupancyChartData"
              :data="parkingLotOccupancyChartData"
              :options="chartOptions"
            />
          </div>
        </div>
        <p v-else>Loading summary data...</p>
      </div>
    </div>

    <!-- Create/Edit Parking Lot Modal -->
    <div class="modal fade" :class="{ 'show': showCreateLotModal || showEditLotModal }" tabindex="-1" aria-labelledby="parkingLotModalLabel" aria-hidden="true" :style="{ display: (showCreateLotModal || showEditLotModal) ? 'block' : 'none' }">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="parkingLotModalLabel">{{ isEditMode ? 'Edit Parking Lot' : 'Create New Parking Lot' }}</h5>
            <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="isEditMode ? updateParkingLot() : createParkingLot()">
              <div class="mb-3">
                <label for="lotName" class="form-label">Name</label>
                <input type="text" class="form-control" id="lotName" v-model="currentLot.name" required>
              </div>
              <div class="mb-3">
                <label for="lotAddress" class="form-label">Address</label>
                <input type="text" class="form-control" id="lotAddress" v-model="currentLot.address" required>
              </div>
              <div class="mb-3">
                <label for="lotPincode" class="form-label">Pincode</label>
                <input type="text" class="form-control" id="lotPincode" v-model="currentLot.pincode" required>
              </div>
              <div class="mb-3" v-if="!isEditMode">
                <label for="lotSpots" class="form-label">Number of Spots</label>
                <input type="number" class="form-control" id="lotSpots" v-model.number="currentLot.number_of_spots" required min="1">
              </div>
              <div class="mb-3">
                <label for="lotPrice" class="form-label">Price per Hour</label>
                <input type="number" class="form-control" id="lotPrice" v-model.number="currentLot.price" required step="0.01" min="0">
              </div>
              <button type="submit" class="btn btn-primary">{{ isEditMode ? 'Update' : 'Create' }}</button>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade" :class="{ 'show': showCreateLotModal || showEditLotModal }" :style="{ display: (showCreateLotModal || showEditLotModal) ? 'block' : 'none' }"></div>

  </div>
</template>

<script>
import apiClient from '../../services/api';
import { useAuthStore } from '../../stores/auth';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  name: 'AdminDashboard',
  components: { Bar },
  data() {
    return {
      authStore: useAuthStore(),
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
        price: 0.0
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false
      }
    };
  },
  computed: {
    parkingLotOccupancyChartData() {
      if (!this.summaryData || !this.summaryData.parking_lot_occupancy) {
        return null;
      }
      const labels = this.summaryData.parking_lot_occupancy.map(lot => lot.lot_name);
      const occupiedData = this.summaryData.parking_lot_occupancy.map(lot => lot.occupied_spots);
      const availableData = this.summaryData.parking_lot_occupancy.map(lot => lot.available_spots);

      return {
        labels: labels,
        datasets: [
          {
            label: 'Occupied Spots',
            backgroundColor: '#dc3545',
            data: occupiedData
          },
          {
            label: 'Available Spots',
            backgroundColor: '#28a745',
            data: availableData
          }
        ]
      };
    }
  },
  async created() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      await this.fetchParkingLots();
      await this.fetchUsers();
      await this.fetchParkingSpots();
      await this.fetchSummaryData();
    },
    async fetchParkingLots() {
      try {
        const response = await apiClient.get('/admin/parking-lots');
        this.parkingLots = response.data;
      } catch (error) {
        console.error('Error fetching parking lots:', error);
      }
    },
    async fetchUsers() {
      try {
        const response = await apiClient.get('/admin/users');
        this.users = response.data;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    async fetchParkingSpots() {
      try {
        const response = await apiClient.get('/admin/parking-spots');
        this.parkingSpots = response.data;
      } catch (error) {
        console.error('Error fetching parking spots:', error);
      }
    },
    async fetchSummaryData() {
      try {
        const response = await apiClient.get('/admin/summary-charts');
        this.summaryData = response.data;
      } catch (error) {
        console.error('Error fetching summary data:', error);
      }
    },
    async createParkingLot() {
      try {
        await apiClient.post('/admin/parking-lots', this.currentLot);
        this.closeModal();
        await this.fetchData(); // Refresh data
      } catch (error) {
        console.error('Error creating parking lot:', error);
      }
    },
    editParkingLot(lot) {
      this.isEditMode = true;
      this.currentLot = { ...lot }; // Copy lot data to currentLot
      this.showEditLotModal = true;
    },
    async updateParkingLot() {
      try {
        await apiClient.put(`/admin/parking-lots/${this.currentLot.id}`, this.currentLot);
        this.closeModal();
        await this.fetchData(); // Refresh data
      } catch (error) {
        console.error('Error updating parking lot:', error);
      }
    },
    async deleteParkingLot(lotId) {
      if (confirm('Are you sure you want to delete this parking lot?')) {
        try {
          await apiClient.delete(`/admin/parking-lots/${lotId}`);
          await this.fetchData(); // Refresh data
        } catch (error) {
          console.error('Error deleting parking lot:', error);
          alert(error.response.data.message || 'Failed to delete parking lot.');
        }
      }
    },
    closeModal() {
      this.showCreateLotModal = false;
      this.showEditLotModal = false;
      this.isEditMode = false;
      this.currentLot = { // Reset form
        id: null,
        name: '',
        address: '',
        pincode: '',
        number_of_spots: 0,
        price: 0.0
      };
    },
    viewParkingLotDetails(lotId) {
      this.$router.push({ name: 'admin-parking-lot-details', params: { lotId: lotId } });
    }
  }
};
</script>

<style scoped>
/* Add any specific styles for the admin dashboard here */
.modal.show {
  display: block;
}
.modal-backdrop.show {
  opacity: 0.5;
}
.chart-container {
  position: relative;
  height: 400px; /* Adjust height as needed */
  width: 100%;
}
</style>