<template>
    <div class="j_question_grid">
        <div class="j_edit_area">
            <h2>Editing Question {{ props.my.id }}</h2>
            <div class="j_divider"/>
            <v-text-field type="text" v-model="props.my.label" label="User visible label for question"/>
            <v-text-field type="text" v-model="option" label="Write a new choice for an answer"/>
            <v-btn @click="props.my.options.push(option)">Add a new choice</v-btn>
        </div>
        <div class="j_user_area">
            <h2>What the user sees</h2>
            <v-select :label="props.my.label" :items="props.my.options"/>
            <v-btn :disabled="true">Continue</v-btn>
        </div>
    </div>
</template>
<script setup lang="ts">
import {type SingleChoiceDropdown} from '@/types'
import {ref} from 'vue'
interface Props {
    my:SingleChoiceDropdown
}
const props = defineProps<Props>()
const option = ref("")
</script>