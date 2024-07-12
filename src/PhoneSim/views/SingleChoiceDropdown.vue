<template>
    <layout>
        <template v-slot:content>
            <ion-card>
                <ion-card-header>
                    <ion-card-title>{{ props.my.label }}</ion-card-title>
                </ion-card-header>
                <ion-list>
                    <ion-item>
                        <ion-select  v-model="answer">
                            <ion-select-option v-for="option in props.my.options" :value="option">
                                {{ option }}
                            </ion-select-option>
                        </ion-select>
                    </ion-item>
                </ion-list>
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
import {type SingleChoiceDropdown as SingleChoiceDropdownType} from '../../types'
import { IonList, IonItem, IonButton, IonSelect, IonSelectOption, IonIcon,
    IonCardHeader, IonCardTitle, IonCardContent, IonCard
 } from '@ionic/vue'
import { arrowForwardCircleOutline } from 'ionicons/icons'
import {ref} from 'vue'
import Layout from './Layout.vue'

interface Props{
    my: SingleChoiceDropdownType
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