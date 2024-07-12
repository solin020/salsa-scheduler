<template>
  <layout>
    <template v-slot:content>
      <ion-card>
        <ion-card-header>
          <ion-card-title>{{ props.my.label }}</ion-card-title>
        </ion-card-header>
        <ion-card-content>
          <ion-list>
              <ion-item>
                <ion-textarea
                  placeholder="Type response here"
                  :auto-grow="true"
                  v-model="answer"
                />
              </ion-item>
          </ion-list>
        </ion-card-content>
      </ion-card>
    </template>
    <template v-slot:footer>
      <ion-button @click="submit_answer()">
        <ion-icon :icon="arrowForwardCircleOutline" size="large"/>
      </ion-button>
    </template>
  </layout>
</template>
<script setup lang="ts">
import {type Textbox as TextboxType} from '../../types'
import {IonItem, IonTextarea, IonList, IonIcon, IonButton,
  IonCardHeader, IonCardTitle, IonCard,IonCardContent
 } from '@ionic/vue'
import { arrowForwardCircleOutline } from 'ionicons/icons'
import {ref} from 'vue'
import Layout from './Layout.vue'

interface Props{
    my: TextboxType
    question_responses:{[key:string]:(number|string|string[]|null)}
    continue_ema:()=>void
}
const props = defineProps<Props>()
const answer = ref("")

function submit_answer(){
    props.question_responses[props.my.id]=answer.value
    props.continue_ema()
}
</script>