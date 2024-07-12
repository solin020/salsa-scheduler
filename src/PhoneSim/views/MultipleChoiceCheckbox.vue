<template>
    <layout>
        <template v-slot:content>
            <ion-card>
                <ion-card-header>
                    <ion-card-title>{{ props.my.label }}</ion-card-title>
                </ion-card-header>
                <ion-card-content>
                    <ion-list>
                        <ion-item v-for="option in props.my.options">
                            <ion-checkbox label-placement="start" @ion-change="toggle_choice(option)">{{ option }}</ion-checkbox>
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
import {type MultipleChoiceCheckbox as MultipleChoiceCheckboxType} from '../../types'
import { IonCheckbox, IonItem, IonList, IonButton, IonIcon, 
    IonCardHeader, IonCardTitle, IonCardContent, IonCard} from '@ionic/vue'
import { arrowForwardCircleOutline } from 'ionicons/icons'
import {ref, type Ref} from 'vue'
import Layout from './Layout.vue'

interface Props{
    my: MultipleChoiceCheckboxType
    question_responses:{[key:string]:(number|string|string[]|null)}
    continue_ema:()=>void
}
const props = defineProps<Props>()
const answers: Ref<string[]> = ref([])

function submit_answer(){
    props.question_responses[props.my.id] = answers.value
    props.continue_ema()
}

function toggle_choice(option:string){
    const ans = answers.value
    if (ans.includes(option)){
        ans.splice(ans.indexOf(option), 1)
    } else {
        ans.push(option)
    }
}

</script>