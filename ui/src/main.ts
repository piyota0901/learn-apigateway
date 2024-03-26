import { createApp } from 'vue'
import router from './router'
import './style.css'
import App from '@/App.vue'
import { createAuth0 } from '@auth0/auth0-vue'

createApp(App)
.use(router)
.use(
  createAuth0({
    domain: import.meta.env.VITE_AUTH0_DOMAIN,
    clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
    authorizationParams: {
      redirect_uri: window.location.origin,
      audience: 'http://127.0.0.1:8000/orders'
    }
  })
)
.mount('#app')
