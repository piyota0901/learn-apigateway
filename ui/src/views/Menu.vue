<script setup lang="ts">
import { ref, watch } from 'vue';
import { useAuth0 } from '@auth0/auth0-vue';
import ProductCard from '@/components/ProductCard.vue';
import { OrderItem } from '@/interfaces';
import axios from 'axios';

interface Product {
  product: string
  size: string
  price: number
  image: string
}

const { getAccessTokenSilently } = useAuth0();
const orders = ref({
  order: [] as OrderItem[]
});
const price = ref(0);

const handlePlaceOrder = (product: Product) => {
  orders.value.order.push({
    product: product.product,
    size: product.size,
    quantity: 1
  });
  price.value += product.price;
}

const placeOrder = async () => {
  const token = await getAccessTokenSilently();
  console.log(token)
  await axios.post('http://localhost:8000/orders',
    orders.value,
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );
  orders.value.order = [];
  price.value = 0;
}

watch(orders.value.order, (newOrder) => {
  console.log(newOrder);
});

</script>
<template>
  <div class="menu">
    <ProductCard @place-order="handlePlaceOrder" />
    <div class="divider"></div>
    <div class="order text-right">
      <div class="stats">
        <div class="stat">
          <div class="stat-title">合計金額</div>
          <div class="stat-value">${{ price }}</div>
        </div>
      </div>
    </div>
    <div class="text-right">
      <button class="btn btn-primary w-36" @click="placeOrder">注文する</button>
    </div>
  </div>
</template>
<style scoped>
/* Add valid CSS rules here */
</style>
