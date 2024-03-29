<script setup lang="ts">
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
</script>
<template>
  <Header />
  <router-view></router-view>
  <Footer />
</template>
<style scoped>
/* Headerを先頭で固定したい */
header {
  position: sticky;
  top: 0;
  z-index: 1000;
}

/* Footerを最下部で固定したい */
footer {
  position: fixed;
  bottom: 0;
  width: 100%;
}
</style>
