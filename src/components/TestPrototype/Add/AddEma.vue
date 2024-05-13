<template>
    <j-list :items="props.my.form" :mimetypes="[]">
        <template #preamble>
            <h2>Questions:</h2>
        </template>
        <template #renderer="{item:current_question}">
            <div class="j_icont">
                <div class="j_imain">
                    <AddSlider
                        :my="current_question"
                        v-if="current_question.type==='slider'"/>
                    <AddTextbox
                        :my="current_question"
                        v-else-if="current_question.type==='textbox'"/>
                    <AddSingleChoiceRadio
                        :my="current_question"
                        v-else-if="current_question.type==='single-choice-radio'"/>
                    <AddSingleChoiceDropdown
                        :my="current_question"
                        v-else-if="current_question.type==='single-choice-dropdown'"/>
                    <AddMultipleChoiceCheckbox
                        :my="current_question"
                        v-else-if="current_question.type==='multiple-choice-checkbox'"/>
                </div>
                <div class="j_idelete">
                    <v-btn @click="delete_question(current_question)">Delete Question {{ current_question.id}}</v-btn>
                </div>
            </div>
        </template>
        <template #postamble>
            <span>
                <v-text-field label="Question id" v-model="questionid"/>
                <v-select v-model="questiontype" label="Question type" :items="[
                    'textbox', 'slider', 'single-choice-radio', 'single-choice-dropdown', 'multiple-choice-checkbox'
                    ]"/>
                <v-btn @click="add_question()" :disabled="button_active">Add question ➕</v-btn> 
            </span>
        </template>
    </j-list>
</template>
<script setup lang="ts">
import {type Ema, 
        type QuestionType,
        type Slider as SliderType,
        type Textbox as TextboxType,
        type SingleChoiceRadio as SingleChoiceRadioType,
        type SingleChoiceDropdown as SingleChoiceDropdownType,
        type MultipleChoiceCheckbox as MultipleChoiceCheckboxType} from '@/types'
import AddSlider from './AddSlider.vue';
import AddSingleChoiceDropdown from './AddSingleChoiceDropdown.vue';
import AddSingleChoiceRadio from './AddSingleChoiceRadio.vue';
import AddMultipleChoiceCheckbox from './AddMultipleChoiceCheckbox.vue';
import AddTextbox from './AddTextbox.vue';
import JList from '@/components/JList.vue';
import {ref, type Ref, computed, type ComputedRef} from 'vue'

interface Props {
    my:Ema
}
const props = defineProps<Props>()
const questiontype = ref("")
const questionid = ref("")
function add_question(){
    const type = questiontype.value
    const id = questionid.value
    const options: string[] = []
    const label = ''
    const min = 0;
    const max = 100;
    if (type==='textbox'){
        props.my.form.push({
            type,
            id,
            label,
        })
    }
    else if (type==='slider'){
        props.my.form.push({
            type,
            id,
            label,
            min,
            max
        })
    }
    else if (type==='single-choice-dropdown'){
        props.my.form.push({
            type,
            id,
            label,
            options
        })
    }
    else if (type==='multiple-choice-checkbox'){
        props.my.form.push({
            type,
            id,
            label,
            options
        })
    }
    else if (type==='single-choice-radio'){
        props.my.form.push({
            type,
            id,
            label,
            options
        })
    }
    questionid.value=''
}
function delete_question(q:QuestionType){
    props.my.form.splice(props.my.form.indexOf(q),1)
}
const button_active: ComputedRef<boolean> = computed(()=>{
    if (questionid.value.length>0 && questiontype.value.length>0){
        return false
    } else {
        return true
    }
})
</script>
<style>
.j_question_grid{
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
    row-gap: 20px;
    overflow: hidden;
}
.j_edit_area{
    grid-row: 1 / 2;
    background-color:white;
}
.j_user_area{
    grid-row: 2 / 3;
    background-color: white;
    border: 5px inset black;


}
</style>