<template>
    <div>
        <div>Enable automatic recording?<input type="checkbox" v-model="props.my.autoadvance"/></div>
        <div v-if="props.my.autoadvance">Automatic recording duration: <input type="number" v-model="props.my.duration"/> seconds</div>
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