<template>
    <div>
        <div>Start recording automatically?<input type="checkbox" v-model="props.my.autoplay"/></div>
        <div v-if="props.my.hide_controls || props.my.hide_early || props.my.autoadvance">Minimum recording duration: <input type="number" v-model="props.my.duration"/> seconds</div>
        <div v-if="!props.my.hide_early">Finish recording automatically?<input type="checkbox" v-model="props.my.autoadvance"/></div>
        <div v-if="!props.my.autoadvance">Guarantee minimum recording duration?<input type="checkbox" v-model="props.my.hide_early"/></div>
    </div>
    <div class="j_divider"/>
    <h2>Recording</h2>
    <v-btn :disabled="true">Start Recording 🎙️</v-btn>
    <div class="j_divider"/>
</template>
<script setup lang="ts">
import {type Recording} from '@/types'
import {ref,  type Ref } from 'vue';
interface Props {
    my:Recording
}

const props = defineProps<Props>()
</script>
<style src="@/css/jview.css"/>