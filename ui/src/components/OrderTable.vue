<script setup lang="ts">
import { useAuth0 } from '@auth0/auth0-vue'
import { ref, onBeforeMount } from 'vue'
import { Order } from '@/interfaces'
import axios from 'axios'
import OrderDetalDialog from '@/components/OrderDetailDialog.vue'

const { getAccessTokenSilently } = useAuth0()
const orders = ref<Order[]>([])

const getOrders = async () => {
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
  console.log(orders.value)
}

onBeforeMount(() => {
  getOrders()
})

const selectedOrder = ref<Order>();

const showModal = (order: Order) => {
  selectedOrder.value = order;
  const dialog = document.getElementById('order-detail') as HTMLDialogElement;
  dialog.showModal();
};

const dateToString = (date: Date) => {
  return `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`
}

</script>
<template>
  <div class="overflow-x-auto" id="order-table">
    <table class="table">
      <thead>
        <tr>
          <th>No</th>
          <th>注文日</th>
          <th>ステータス</th>
          <th>詳細</th>
        </tr>
      </thead>
      <template v-if="orders.length === 0">
        <div class="flex justify-center">
          <p>注文がありません</p>
        </div>
      </template>
      <template v-else v-for="order in orders" :key="order.id">
        <tbody>
          <tr>
            <th>{{ orders.indexOf(order) + 1 }}</th>
            <th>{{ dateToString(order.created) }}</th>
            <th>{{ order.status }}</th>
            <th>
              <button class="btn" @click="showModal(order)">詳細</button>
              <dialog class="modal" id="order-detail">
                <OrderDetalDialog :order="selectedOrder" />
              </dialog>
            </th>
          </tr>
        </tbody>
      </template>
    </table>
  </div>
</template>
<style scoped>
#order-table {
  width: 80%;
  margin: 0 auto;
}
</style>