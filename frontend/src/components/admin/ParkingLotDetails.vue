<template>
  <div class="container mt-4">
    <nav aria-label="breadcrumb">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><router-link to="/admin/dashboard">Admin Dashboard</router-link></li>
        <li class="breadcrumb-item active" aria-current="page">{{ parkingLot.name }}</li>
      </ol>
    </nav>

    <h1 class="mb-4">Parking Lot: {{ parkingLot.name }}</h1>
    <div v-if="parkingLot">
      <p><strong>Address:</strong> {{ parkingLot.address }}</p>
      <p><strong>Pincode:</strong> {{ parkingLot.pincode }}</p>
      <p><strong>Price per Hour:</strong> ₹{{ parkingLot.price }}</p>
      <p><strong>Total Spots:</strong> {{ parkingLot.number_of_spots }}</p>
    </div>
    <div v-else>
      <p>Loading parking lot details...</p>
    </div>

    <h2 class="mt-5 mb-3">Parking Spots</h2>
    <div v-if="parkingSpots.length > 0" class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
      <div class="col" v-for="spot in parkingSpots" :key="spot.id">
        <div class="card h-100" :class="{ 'bg-success-subtle': spot.status === 'A', 'bg-danger-subtle': spot.status === 'O' }">
          <div class="card-body">
            <h5 class="card-title">Spot #{{ spot.spot_number }}</h5>
            <p class="card-text">Status: <strong>{{ spot.status === 'A' ? 'Available' : 'Occupied' }}</strong></p>
            <div v-if="spot.status === 'O' && spot.reserved_by">
              <p class="card-text">Reserved By: {{ spot.reserved_by.email }}</p>
              <p class="card-text">Parked Since: {{ new Date(spot.reserved_by.parking_timestamp).toLocaleString() }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <p v-else>No parking spots found for this lot.</p>
  </div>
</template>

<script>
import apiClient from '../../services/api';

export default {
  name: 'ParkingLotDetails',
  props: ['lotId'],
  data() {
    return {
      parkingLot: null,
      parkingSpots: []
    };
  },
  async created() {
    await this.fetchParkingLotDetails();
    await this.fetchParkingSpotsForLot();
  },
  methods: {
    async fetchParkingLotDetails() {
      try {
        const response = await apiClient.get(`/admin/parking-lots/${this.lotId}`);
        this.parkingLot = response.data;
      } catch (error) {
        console.error('Error fetching parking lot details:', error);
        // Handle error, e.g., redirect to 404 or show message
      }
    },
    async fetchParkingSpotsForLot() {
      try {
        const response = await apiClient.get(`/admin/parking-lots/${this.lotId}/spots`);
        this.parkingSpots = response.data;
      } catch (error) {
        console.error('Error fetching parking spots for lot:', error);
      }
    }
  }
};
</script>

<style scoped>
.card.bg-success-subtle {
  background-color: #d4edda !important; /* Light green */
}
.card.bg-danger-subtle {
  background-color: #f8d7da !important; /* Light red */
}
</style>
