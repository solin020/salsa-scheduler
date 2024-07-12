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
                            <ion-radio-group v-model="answer" >
                                <ion-radio v-for="option in props.my.options" :value="option">
                                    {{ option }}
                                </ion-radio>
                            </ion-radio-group>
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
import {type SingleChoiceRadio as SingleChoiceRadioType} from '../../types'
import { IonRadioGroup, IonRadio, IonButton, IonList, IonItem, IonIcon, 
    IonCardHeader, IonCardTitle, IonCardContent, IonCard } from '@ionic/vue'
import {ref} from 'vue'
import { arrowForwardCircleOutline } from 'ionicons/icons'
import Layout from './Layout.vue'

interface Props{
    my: SingleChoiceRadioType
    question_responses:{[key:string]:(number|string|string[]|null)}
    continue_ema:()=>void
}
const props = defineProps<Props>()
const answer = ref("")

function submit_answer(){
    props.question_responses[props.my.id] = answer.value
    props.continue_ema()
}



</script>