<template>
  <layout>
    <template v-slot:content>
      <ion-card>
        <ion-card-header>
          <ion-card-title>{{ props.my.id }}</ion-card-title>
        </ion-card-header>
        <ion-card-content>
          <ion-list>
            <ion-item>
              <ion-icon :icon="micCircleOutline" :style="{color:active_color}"/>
            </ion-item>
            <ion-item>
              <template v-if="!is_recording">
                <ion-icon :icon="radioButtonOffOutline" style="color:black;" size="large"/>
              </template>
              <template v-else>
                <ion-icon :icon="radioButtonOnOutline" style="color:red;" size="large"/>
                <ion-text size="large">{{seconds_elapsed}}</ion-text>
              </template>
            </ion-item>
          </ion-list>
        </ion-card-content>
      </ion-card>
    </template>
    <template v-slot:footer>
            <ion-button v-if="!is_recording && !props.my.autoplay" @click="audio_start()" size="large">
                  Begin Recording
            </ion-button>
            <ion-button v-else-if="finished && !props.my.hide_controls" @click="audio_stop()" size="large">
                  Stop Recording
            </ion-button>
    </template>
  </layout>
</template>
<script setup lang="ts">
import { type Recording as RecordingType} from '../../types'
import {ref, computed} from 'vue'
import {save_encrypt_message_response} from '../encryption/pgp'
import { VoiceRecorder} from 'capacitor-voice-recorder'
import { IonList, IonItem, IonButton, IonIcon,
  IonCardHeader, IonCardTitle, IonText, IonCard, IonCardContent
} from '@ionic/vue'
import {micCircleOutline, radioButtonOffOutline, radioButtonOnOutline, arrowForwardCircleOutline} from 'ionicons/icons'
import mime from 'mime'
import Layout from './Layout.vue'
import { salsaStore } from '../store'


const store = salsaStore()

const recording_permission = ref(false)
VoiceRecorder.hasAudioRecordingPermission().then(v => recording_permission.value=v.value)

interface Props{
    my:RecordingType
    uploads: {[key:string]:Buffer}
    advance_stimulus:()=>void
}


const props = defineProps<Props>()
const seconds_elapsed = ref(0)
const finished = computed(()=>{
  if (props.my.duration && (props.my.hide_early || props.my.autoadvance)){
    return seconds_elapsed.value >= props.my.duration
  } else {
    return true
  }
})

const q = ref<ReturnType<typeof setTimeout>>()

function timer_countup(){
  q.value = setTimeout(
    () =>{
      if(is_recording.value){
        seconds_elapsed.value += 1
        if (finished.value && props.my.autoadvance){
          clearTimeout(q.value)
          advance()
        }
        timer_countup()
      }
    }
    ,1000)
}

function advance(){
  audio_stop()
}

const is_recording=ref(false)

async function audio_start(){
  if (!recording_permission.value){
    await VoiceRecorder.requestAudioRecordingPermission()
  }
  VoiceRecorder.startRecording()
  timer_countup()
  active_color.value="red"
  is_recording.value=true
}



const active_color=ref("black")

function audio_stop(){
  VoiceRecorder.stopRecording().then( async r =>{
    await save_encrypt_message_response({
      name: `${props.my.id}.${mime.getExtension(r.value.mimeType)}`,
      body: Uint8Array.from(atob(r.value.recordDataBase64), c => c.charCodeAt(0)),
      format:'binary'
    }, store.schedule_id, store.salsaid, store.test_prototype_id, store.sequence_no)
  })
  active_color.value="black"
  is_recording.value=false
  props.advance_stimulus()
}
if (props.my.autoplay){
  audio_start()
}
</script>