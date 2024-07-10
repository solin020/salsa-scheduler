<template>
    <div class="j_mediadisplay">
        <div class="j_mediainput">
            <div v-if="!props.my.hide_early">Move on from image automatically after a certain number of seconds?<input type="checkbox" v-model="props.my.autoadvance"/></div>
            <div v-if="!props.my.autoadvance">Prevent participant from moving on past image for a certain number of seconds?<input type="checkbox" v-model="props.my.hide_early"/></div>
            <div v-if="props.my.autoadvance || props.my.hide_early">Image display duration: <input type="number" v-model="props.my.duration"/> seconds</div>
        </div>
        <div class="j_media">
            <img :src="imagesrc"/>
        </div>
    </div>
</template>
<script setup lang="ts">
import {type Image as ImageType} from '@/types'
import { ref, type Ref, computed } from 'vue';
interface Props {
    my:ImageType
}
const props = defineProps<Props>()
function submit_file(e:Event){
    // @ts-expect-error
    const file: File = e.target.files[0]
    props.my.file = [file]
    props.my.uri = file.name
}
const imagesrc = computed<string>(() =>{
    if (props.my.file.length>0){
        return URL.createObjectURL(props.my.file[0])
    } else {
        return ''
    }
  }
)
const no_file = computed(() => props.my.file.length===0)

</script>
<style src='@/css/mediadisplay.css'/>