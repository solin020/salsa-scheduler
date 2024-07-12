<template>
    <layout>
      <template v-slot:content>
        <ion-card>
          <ion-card-header>
            <ion-card-title>Click arrow below to begin your test</ion-card-title>
          </ion-card-header>
          <ion-card-content>
            <ion-text>Logged in as {{ store.salsaid }}</ion-text>
          </ion-card-content>
        </ion-card>
      </template>
      <template v-slot:footer>
        <ion-button  @click="begin()"><ion-icon :icon="caretForwardCircleOutline" size="large"/></ion-button>
      </template>
    </layout>
</template>

<script setup lang="ts">
import { IonText, IonButton, IonIcon, IonCard, IonCardHeader, IonCardContent,IonCardTitle} from '@ionic/vue'
import {caretForwardCircleOutline} from 'ionicons/icons'
import { Filesystem, Directory, Encoding } from '@capacitor/filesystem'
import Layout from './Layout.vue'
import { salsaStore } from '../store'
import type { SchedulePrototype } from '@/types/schedule'

const store = salsaStore()


async function begin(){
  try {
    const now = new Date().getTime()
    const entries: SchedulePrototype<'device'>['phases'][number]['spec']['tests'] = []
    for (const phase of store.schedule!.phases){
      for (const test of phase.spec.tests){
        entries.push(test)
      }
    }
    find_date:{
      for (const ts of entries){
        const [date_s, time_s, timezone_s] = ts.formal_timestamp.split(' ')
        let [year_i, month_i, day_i] = date_s.split('/').map(d=>parseInt(d))
        month_i = month_i-1
        const [hour_i, minute_i] = time_s.split(':').map(t=>parseInt(t))
        const ts_start = new Date(year_i, month_i, day_i, hour_i, minute_i).getTime()
        const diff = now-ts_start
        //Tests may be taken up to two days late 
        if (diff > 0 && diff < (86400*1000*2) && !(ts.attempted)){
          store.test_prototype_id=ts.prototype_selection.test_prototype_id
          store.sequence_no = ts.sequence_no
          ts.attempted = true
          await store.write_schedule()
          break find_date
        }
      }
      if (store.schedule!.default_selection){
        store.test_prototype_id = (store.schedule!).default_selection.test_prototype_id
        store.sequence_no = -1
      } else {
        throw 'no test scheduled for today'
      }

    }
    store.schedule_id = crypto.randomUUID()


    const metadata = await Filesystem.readFile({
      path: `testprototypes/${store.test_prototype_id}/metadata.json`,
      directory: Directory.External,
      encoding: Encoding.UTF8
    })
    const stimuli = JSON.parse(metadata.data.toString())
    store.todays_test_prototype = {
      stimuli,
      id:store.test_prototype_id
    }
    store.current_component='TestPrototype'
  } catch (error){
    if (error === 'no test scheduled for today'){
      alert('No test scheduled for today.')
    } else{
      alert('An internal error occurred')
    }
  }
  
}

</script>


