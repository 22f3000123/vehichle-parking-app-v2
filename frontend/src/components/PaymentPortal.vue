<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Payment for Parking Spot</div>
          <div class="card-body">
            <div v-if="resId && parkingCost">
              <p>Payment for:</p>
              <p><strong>Parking Lot:</strong> {{ resId }}</p>
              <p><strong>Total Price</strong> {{ parkingCost }}</p>
              <p><strong>Total Time in HR</strong> {{ parkingTime.toFixed(2) }}</p>
              <hr />
            </div>
            <form @submit.prevent="processPayment">
              <div class="mb-3">
                <label for="cardNumber" class="form-label">Card Number</label>
                <input type="text" class="form-control" id="cardNumber" v-model="cardNumber"
                  placeholder="XXXX XXXX XXXX XXXX" required />
              </div>
              <div class="mb-3">
                <label for="cardName" class="form-label">Card Holder Name</label>
                <input type="text" class="form-control" id="cardName" v-model="cardName" placeholder="John Doe"
                  required />
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="expiryDate" class="form-label">Expiry Date</label>
                  <input type="text" class="form-control" id="expiryDate" v-model="expiryDate" placeholder="MM/YY"
                    required />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="cvv" class="form-label">CVV</label>
                  <input type="text" class="form-control" id="cvv" v-model="cvv" placeholder="123" required />
                </div>
              </div>
              <div class="mb-3">
                <label for="amount" class="form-label">Amount (for simulation)</label>
                <input type="number" class="form-control" id="amount" v-model.number="amount" step="0.01" min="0.01"
                  required />
              </div>
              <button type="submit" class="btn btn-primary">Pay Now</button>
              <button type="button" class="btn btn-secondary ms-2" @click="cancelPayment">
                Cancel
              </button>
            </form>
            <div v-if="paymentMessage" class="alert mt-3"
              :class="{ 'alert-success': paymentSuccess, 'alert-danger': !paymentSuccess }">
              {{ paymentMessage }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '../services/api'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export default {
  name: 'PaymentPortal',
  props: {
    resId: String,
    parkingCost: Number,
  },
  data() {
    return {
      cardNumber: '',
      cardName: '',
      expiryDate: '',
      cvv: '',
      amount: 0,
      paymentMessage: '',
      paymentSuccess: false,
      parkingTime: 0
    }
  },

  async created() {
    await this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        const response = await apiClient.get(`/user/payment-datails/${this.resId}`)
        this.parkingTime = response.data.res_time / 3600
      } catch (error) {
        console.error('Error fetching parking lots:', error)
      }
    },

    async processPayment() {
      this.paymentMessage = 'Processing your payment...'
      this.paymentSuccess = false

      try {
        const paymentResponse = await apiClient.post('/user/process-payment')

        if (paymentResponse.status === 200) {
          toast.success('Payment Successful!', {
            autoClose: 1000,
          })
        } else {
          this.paymentMessage = paymentResponse.data.message || 'Payment processing failed.'
          this.paymentSuccess = false
          toast.error(this.paymentMessage, {
            autoClose: 1000,
          })
        }
      } catch (error) {
        console.error('Payment failed:', error)
        this.paymentMessage = error.response?.data?.message || 'An error occurred during payment.'
        this.paymentSuccess = false
        toast.error(this.paymentMessage, {
          autoClose: 1000,
        })
      } finally {
        this.$router.push('/user/dashboard')
      }
    },
    cancelPayment() {
      this.$router.push('/user/dashboard')
    },
  },
}
</script>
