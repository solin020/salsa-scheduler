<template>
    <h2>{{ props.my.label }}</h2>
    <span>{{ props.my.min }}</span>
    <v-slider
    thumb-label="always"
    :min="props.my.min"
    :max="props.my.max"
    v-model="response"
    />
    <span>{{ props.my.max }}</span>
    <v-btn @click="respond()">Submit</v-btn>
</template>
<script setup lang="ts">
import {type Slider} from '@/types'
import { ref } from 'vue';
interface Props {
    my:Slider
    advance_question:()=>void
    answers: {[name:string]:(string|string[]|number)}
}
const props = defineProps<Props>()
const response = ref(0)
function respond(){
    props.answers[props.my.id]=response.value
    props.advance_question()
}
</script>