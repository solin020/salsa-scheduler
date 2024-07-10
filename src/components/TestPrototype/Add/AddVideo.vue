<template>
    <div class="j_mediadisplay">
        <div class="j_mediainput">
            <div v-if="no_file"><input type="file" @input="submit_file($event)" class="j_mediainput" accept="video/mp4"/></div>
            <div>Automatically play video?<input type="checkbox" v-model="props.my.autoplay"/></div>
            <div>Automatically move on when video is done?<input type="checkbox" v-model="props.my.autoadvance"/></div>
            <div>Prevent participant from moving on before video is done playing?<input type="checkbox" v-model="props.my.hide_early"/></div>
            <div v-if="props.my.autoplay">Prevent participant from accessing video controls?
                <input type="checkbox" v-model="props.my.hide_controls"/>
            </div>
        </div>
        <div class="j_media">
            <video :src="videosrc" controls/>
        </div>
    </div>
</template>
<script setup lang="ts">
import {type Video as VideoType} from '@/types'
import { ref, type Ref, computed } from 'vue';
interface Props {
    my:VideoType
}

function submit_file(e:Event){
    // @ts-expect-error
    const file: File = e.target.files[0]
    props.my.file = [file]
    props.my.uri = file.name
}

const props = defineProps<Props>()
const videosrc = computed<string>(() =>{
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