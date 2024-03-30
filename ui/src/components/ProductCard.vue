<script setup lang="ts">
interface Product {
  product: string
  size: string
  price: number
  image: string
}

const products = [
  {
    "product": "Cappuccino",
    "size": "small",
    "price": 4.0,
    "image": "espresso.jpg"
  },
  {
    "product": "Espresso",
    "size": "medium",
    "price": 4.0,
    "image": "espresso.jpg"
  },
  {
    "product": "Latte",
    "size": "large",
    "price": 5.5,
    "image": "espresso.jpg"
  }
] as Product[]

const emit = defineEmits(["place-order"])

const getImageUrl = (fileName: string) => {
  return new URL(`../assets/images/${fileName}`, import.meta.url).href
}

const displayedProducts = products.map(product => {
  return {
    ...product,
    image: getImageUrl(product.image)
  }
})

const placeOrder = (product: Product) => {
  emit("place-order", product)
}

</script>
<template>
  <div class="flex flex-row justify-center">
    <div v-for="product in displayedProducts" :key="product.product" class="p-4">
      <div class="card w-96 h-96 bg-base-100 shadow-xl">
        <figure><img :src="product.image" alt="" /></figure>
        <div class="card-body">
          <h2 class="card-title">{{ product.product }}</h2>
          <p>価格: <strong class="text-lg">${{ product.price }}</strong></p>
          <div class="card-actions justify-end">
            <button class="btn btn-primary" @click="placeOrder(product)">注文する</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped></style>
