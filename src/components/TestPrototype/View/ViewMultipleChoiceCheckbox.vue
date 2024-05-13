<template>
    <h2>{{ props.my.label }}</h2>
    <v-checkbox 
        v-for="option in props.my.options"
        v-model="response"
        :label="option"
        :value="option"
    />
    <v-btn @click="respond()">Answer</v-btn>
</template>
<script setup lang="ts">
import {type MultipleChoiceCheckbox} from '@/types'
import {ref, type Ref} from 'vue'
interface Props {
    my:MultipleChoiceCheckbox
    answers: {[name:string]:(string|string[]|number)}
    advance_question:()=>void
}
const props = defineProps<Props>()
const response: Ref<string[]> = ref([])
function respond(){
    props.answers[props.my.id] = response.value
    props.advance_question()
}
</script>