import { createApp } from 'vue'
import App from './CoordinatorApp.vue'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import VCalendar from 'v-calendar'
import 'v-calendar/style.css'
import '@/css/main.css'
const vuetify = createVuetify({
  components,
  directives
})
createApp(App).use(vuetify).use(VCalendar, {}).mount('#app')
