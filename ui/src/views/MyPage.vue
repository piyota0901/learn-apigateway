<script setup lang="ts">
import { useAuth0 } from '@auth0/auth0-vue'
import { ref } from 'vue'
import axios from 'axios'

const { isAuthenticated, user, getAccessTokenSilently } = useAuth0()

const orders = ref([])

const getOters = async () => {
  const token = await getAccessTokenSilently()
  console.log("token", token)
  const response = await axios.get('http://localhost:8000/orders', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  orders.value = response.data
  console.log(response.data)
}

</script>
<template>
  <button class="btn btn-active btn-primary" @click="getOters">Get Others</button>
  <code>
      <pre>{{ orders }}</pre>
    </code>
</template>
<style scoped></style>