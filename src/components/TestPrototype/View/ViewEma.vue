<template>
    <ViewSlider 
        :my="(current_question as SliderType)" 
        v-if="current_question.type==='slider'"
        :answers="answers"
        :advance_question="advance_question"/>
    <ViewTextbox 
        :my="(current_question as TextboxType)" 
        v-else-if="current_question.type==='textbox'"
        :answers="answers"
        :advance_question="advance_question"/>
    <ViewSingleChoiceRadio 
        :my="(current_question as SingleChoiceRadioType)" 
        v-else-if="current_question.type==='single-choice-radio'"
        :answers="answers"
        :advance_question="advance_question"/>
    <ViewSingleChoiceDropdown 
        :my="(current_question as SingleChoiceDropdownType)" 
        v-else-if="current_question.type==='single-choice-dropdown'"
        :answers="answers"
        :advance_question="advance_question"/>
    <ViewMultipleChoiceCheckbox 
        :my="(current_question as MultipleChoiceCheckboxType)" 
        v-else-if="current_question.type==='multiple-choice-checkbox'"
        :answers="answers"
        :advance_question="advance_question"/>
</template>
<script setup lang="ts">
import {type Ema, 
        type Slider as SliderType,
        type Textbox as TextboxType,
        type SingleChoiceRadio as SingleChoiceRadioType,
        type SingleChoiceDropdown as SingleChoiceDropdownType,
        type MultipleChoiceCheckbox as MultipleChoiceCheckboxType} from '@/types'
import ViewSlider from './ViewSlider.vue';
import ViewSingleChoiceDropdown from './ViewSingleChoiceDropdown.vue';
import ViewSingleChoiceRadio from './ViewSingleChoiceRadio.vue';
import ViewMultipleChoiceCheckbox from './ViewMultipleChoiceCheckbox.vue';
import ViewTextbox from './ViewTextbox.vue';
import {ref, computed, type ComputedRef, type Ref} from 'vue'

type Question = (SliderType|TextboxType|SingleChoiceRadioType|SingleChoiceDropdownType|MultipleChoiceCheckboxType)

interface Props {
    my:Ema
    advance_stimulus:()=>void
    upload_files:File[]
}
const answers: Ref<{[name:string]:(string|string[]|number)}> = ref({})
const props = defineProps<Props>()
const question_number = ref(0)
function advance_question(){
    if (question_number.value + 1 >= props.my.form.length){
        props.upload_files.push(new File([JSON.stringify(answers.value)], `${props.my.id}.json`))
        props.advance_stimulus()
    } else{
        question_number.value++
    }
}
const current_question:ComputedRef<Question> = computed(() =>{

    return props.my.form[question_number.value]
})
</script>