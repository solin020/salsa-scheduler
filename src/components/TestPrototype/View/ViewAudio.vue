<template>
    <audio :src="audiosrc" controls v-if="!props.my.autoadvance"/>
    <audio :src="audiosrc" autoplay v-else-if="props.my.autoadvance"/>
    <v-btn v-if="!props.my.autoadvance" @click="props.advance_stimulus()">Continue</v-btn>
</template>
<script setup lang="ts">
import {type Audio as AudioType} from '@/types'
import { ref, type Ref, computed } from 'vue';
interface Props {
    my:AudioType
    advance_stimulus:()=>void
}
const props = defineProps<Props>()
const audiosrc = computed<string>(() =>{
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