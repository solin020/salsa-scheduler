<template>
    <img :src="imagesrc"
            style="max-width:100%;"/>
    <v-btn v-if="!props.my.autoadvance" @click="props.advance_stimulus()">Continue</v-btn>
</template>
<script setup lang="ts">
import {type Image as ImageType} from '@/types'
import { ref, type Ref, computed } from 'vue';
interface Props {
    my:ImageType
    advance_stimulus:()=>void
}

const props = defineProps<Props>()
const imagesrc = computed<string>(() =>{
    if (props.my.file.length>0){
        return URL.createObjectURL(props.my.file[0])
    } else {
        return ''
    }
  }
)
if(props.my.autoadvance && props.my.duration){
    setTimeout(props.advance_stimulus, props.my.duration*1000)
}
</script>