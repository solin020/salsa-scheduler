<template>
    <h2>{{ props.my.label }}</h2>
    <v-text-field :label="props.my.label" v-model="response"/>
    <v-btn @click="respond()">Submit</v-btn>
</template>
<script setup lang="ts">
import {type Textbox} from '@/types'
import { ref } from 'vue';
interface Props {
    my:Textbox
    advance_question:()=>void
    answers: {[name:string]:(string|string[]|number)}
}
const props = defineProps<Props>()
const response = ref("")
function respond(){
    props.answers[props.my.id]=response.value
    props.advance_question()
}
</script>
