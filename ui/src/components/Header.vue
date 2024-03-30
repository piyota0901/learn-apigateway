<script setup lang="ts">
import { useAuth0 } from '@auth0/auth0-vue'

const { isAuthenticated, logout, loginWithRedirect } = useAuth0()

const handleLogout = async () => {
  try {
    await logout();
  } catch (error) {
    console.error(error)
  }
}

const handleLogin = async () => {
  await loginWithRedirect({
    appState: { target: "/account" }
  });
}

</script>
<template>
  <header>
    <div class="navbar bg-neutral">
      <div class="navbar-start text-white">
        <router-link to="/">Coffee Mesh</router-link>
      </div>
      <div class="navbar-center hidden lg:flex">
        <ul className="menu menu-horizontal px-1 text-white">
          <li>
            <router-link to="/menu">Menu</router-link>
          </li>
          <li>
            <a>Item 2</a>
          </li>
          <li>
            <router-link to="/account">My Page</router-link>
          </li>
        </ul>
      </div>
      <div className="navbar-end">
        <span v-if="isAuthenticated" class="text-white">
          <button class="btn btn-square btn-ghost" @click="handleLogout">
            Logout
          </button>
        </span>
        <span v-else class="text-white">
          <button class="btn btn-square btn-ghost" @click="handleLogin">
            Login
          </button>
        </span>
      </div>
    </div>
  </header>
</template>
<style scoped></style>