<script setup lang="ts">
import { useAuth0 } from '@auth0/auth0-vue'
import OrderTable from '@/components/OrderTable.vue'

const { user } = useAuth0()
const name = user.value?.name

</script>
<template>
  <h1>{{ name }}</h1>
  <div class="divider"></div>
  <OrderTable />
</template>
<style scoped></style>