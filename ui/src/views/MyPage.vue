<script setup lang="ts">
import { useAuth0 } from '@auth0/auth0-vue'
import { ref } from 'vue'
import axios from 'axios'
import { Order } from '@/interfaces'
const { isAuthenticated, user, getAccessTokenSilently } = useAuth0()

const orders = ref<Order[]>([])

const getOters = async () => {
  const token = await getAccessTokenSilently()
  const response = await axios.get('http://localhost:8000/orders', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  if (Array.isArray(response.data.orders)) {
    response.data.orders.forEach((order: Order) => {
      order.created = new Date(order.created)
    })
    orders.value = response.data.orders
  } else {
    console.error("Unexpected response:", response.data)
  }
}

</script>
<template>
  <button class="btn btn-active btn-primary" @click="getOters">Get Others</button>
  <div className="overflow-x-auto">
    <table className="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Created</th>
          <th>Status</th>
        </tr>
      </thead>
      <template v-for="order in orders" :key="order.id">
        <tr>
          <td>{{ order.id }}</td>
          <td>{{ order.created }}</td>
          <td>{{ order.status }}</td>
        </tr>
      </template>
    </table>
  </div>
</template>
<style scoped></style>