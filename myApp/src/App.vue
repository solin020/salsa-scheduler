<template>
  <ion-app>
    <component :is="store.current_component"/>
  </ion-app>
</template>

<script setup lang="ts">
import { IonApp} from '@ionic/vue'
import { salsaStore } from './store'

const store = salsaStore()


</script>
