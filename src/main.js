import './style.css'
import { createApp } from 'vue'
import { plugin, defaultConfig } from '@formkit/vue'
import App from './App.vue' // import the main app component
import myConfig from './../formkit.config.js'

// import with an @ symbol are resolved by vite to ./src directory

// Create the app
const app = createApp(App)

// register plugins

app.use(plugin, defaultConfig(myConfig)) // formkit instead of vueform 

// you "mount the app starting at the #app element"
app.mount('#app')
