<script setup lang="ts">
import { defineProps } from 'vue';
import { Order } from '@/interfaces'

const props = defineProps({
  order: {
    type: Object as () => Order | null,
    default: null,
  },
});
console.log(props.order)
</script>

<template>
  <div class="modal-box">
    <h2 class="font-bold ">注文詳細</h2>
    <div class="divider"></div>
    <div v-for="(item, index) in props.order?.order" :key="index">
      <p>商品名: {{ item.product }}</p>
      <p>サイズ: {{ item.size }}</p>
      <p>数量: {{ item.quantity }}</p>
    </div>
    <div class="modal-action">
      <form method="dialog">
        <button class="btn" @click="$emit('close')">Close</button>
      </form>
    </div>
  </div>
</template>
