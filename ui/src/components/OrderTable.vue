<script setup lang="ts">
import { useAuth0 } from '@auth0/auth0-vue'
import { ref, onBeforeMount } from 'vue'
import { Order } from '@/interfaces'
import axios from 'axios'

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
}

onBeforeMount(() => {
  getOrders()
})

const showModal = () => {
  const dialog = document.getElementById('order-details') as HTMLDialogElement;
  dialog.showModal();
}

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
            <th>{{ orders.indexOf(order) }}</th>
            <th>{{ dateToString(order.created) }}</th>
            <th>{{ order.status }}</th>
            <th>
              <button class="btn" @click="showModal">詳細</button>
              <dialog id="order-details" class="modal">
                <div class="modal-box">
                  <h2 class="font-bold ">注文詳細</h2>
                  <div class="divider"></div>
                  <div v-for="item in order.order" :key="order.order.indexOf(item)">
                    <p>商品名: {{ item.product }}</p>
                    <p>サイズ: {{ item.size }}</p>
                    <p>数量: {{ item.quantity }}</p>
                  </div>
                  <div class="modal-action">
                    <form method="dialog">
                      <button class="btn">Close</button>
                    </form>
                  </div>
                </div>
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