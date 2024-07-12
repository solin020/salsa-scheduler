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
                            <ion-range
                                :min="props.my.min"
                                :max="props.my.max"
                                :ticks="true"
                                :snaps="true"
                                v-model="answer"
                                label-placement="stacked"
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
import {type Slider as SliderType} from '../../types'
import { IonRange, IonList, IonItem, IonButton, IonIcon,
    IonCardHeader, IonCardTitle, IonCard, IonCardContent
 } from '@ionic/vue'
import { arrowForwardCircleOutline } from 'ionicons/icons'
import {ref} from 'vue'
import Layout from './Layout.vue'

interface Props{
    my: SliderType
    question_responses:{[key:string]:(number|string|string[]|null)}
    continue_ema:()=>void
}
const props = defineProps<Props>()
const answer = ref(0)
function submit_answer(){
    props.question_responses[props.my.id]=answer.value
    props.continue_ema()
}
</script>