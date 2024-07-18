<template>
    <div>
        <h3>{{ my.id }}</h3>
        <div><input type="checkbox" v-model="props.my.autoplay"/>Start recording automatically?</div>
        <div> <input 
            type="number" v-model="props.my.duration"
            :disabled="!(props.my.hide_controls || props.my.hide_early || props.my.autoadvance)"
            /> Recording duration (seconds)</div>
        <div><input 
            type="checkbox" v-model="props.my.autoadvance"
            :disabled="props.my.hide_early"
            />Finish recording automatically after minimum recording duration has passed?</div>
        <div><input 
            type="checkbox" v-model="props.my.hide_early"
            :disabled="props.my.autoadvance"
            />Guarantee minimum recording duration?</div>
        <div> <input 
            type="checkbox" v-model="props.my.hide_controls"
            :disabled="!(props.my.autoadvance && props.my.autoplay)"
            />Hide controls?</div>
        <div>
            <input type="checkbox"
            @click="toggle_max_duration"
            />Specify max duration?
        </div>
        <div v-if="show_max_duration"> <input 
            type="number" v-model="props.my.max_duration"
            /> Recording max duration (seconds)</div>
    </div>
    <div class="j_divider"/>
    <h2>Recording</h2>
    <div class="j_phone_sim">
        <v-btn :disabled="true">Start Recording 🎙️</v-btn>
    </div>
    <div class="j_divider"/>
</template>
<script setup lang="ts">
import {type Recording} from '@/types'
import {ref,  type Ref } from 'vue';
interface Props {
    my:Recording
}

const props = defineProps<Props>()
const show_max_duration = ref(false)
function toggle_max_duration(){
    if (show_max_duration.value){
        show_max_duration.value = false
        props.my.max_duration=undefined
    } else{
        show_max_duration.value = true
        props.my.max_duration=180
    }
}
</script>
<style src="@/css/jview.css"/>