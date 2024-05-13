<template>
    <h2>{{ props.my.label }}</h2>
    <fieldset>
        <div v-for="option in props.my.options">
            <input type="radio" :value="option" v-model="response" :name="props.my.id"/>
            <span>{{ option }}</span>
        </div>
    </fieldset>
    <v-btn @click="respond()">Submit</v-btn>
</template>
<script setup lang="ts">
import {type SingleChoiceRadio} from '@/types'
import {ref} from 'vue'
interface Props {
    my:SingleChoiceRadio
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