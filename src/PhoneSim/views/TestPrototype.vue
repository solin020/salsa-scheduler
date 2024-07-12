<template>
    <template v-if="current_stimulus">
        <Audio v-if="current_stimulus.type==='audio'" 
            :my="current_stimulus as AudioType" 
            :uploads="uploads"
            :advance_stimulus="advance_stimulus"
            :key="current_stimulus.id"
        />
        <Video v-if="current_stimulus.type==='video'" 
            :my="current_stimulus as VideoType" 
            :uploads="uploads"
            :advance_stimulus="advance_stimulus"
            :key="current_stimulus.id"
        />
        <Image v-if="current_stimulus.type==='image'" 
            :my="current_stimulus as ImageType" 
            :uploads="uploads"
            :advance_stimulus="advance_stimulus"
            :key="current_stimulus.id"
        />
        <Ema v-if="current_stimulus.type==='ema'" 
            :my="current_stimulus as EmaType" 
            :uploads="uploads"
            :advance_stimulus="advance_stimulus"
            :key="current_stimulus.id"
        />
        <Recording v-if="current_stimulus.type==='recording'" 
            :my="current_stimulus as RecordingType" 
            :uploads="uploads"
            :advance_stimulus="advance_stimulus"
            :key="current_stimulus.id"
        />
    </template>

</template>
<script setup lang="ts">
import Ema from './Ema.vue'
import Recording from './Recording.vue'
import Image from './Image.vue'
import Video from './Video.vue'
import Audio from './Audio.vue'
import type {Audio as AudioType, Video as VideoType, Image as ImageType, Recording as RecordingType, Ema as EmaType} from '../../types'
import {computed, ref, type Ref} from 'vue'
import { salsaStore } from '../store'

const store = salsaStore()




const stimulus_number = ref(0)
const current_stimulus = computed(() => store.todays_test_prototype!.stimuli[stimulus_number.value])
const uploads: Ref<{[key:string]:Buffer}> = ref({})

function advance_stimulus(){
    if (stimulus_number.value < (store.todays_test_prototype!.stimuli.length - 1)){
        stimulus_number.value++
        console.log('stimulus advanced')
    } else{
        console.log('test prototype done')
        store.current_component='Uploads'
    }
}

</script>