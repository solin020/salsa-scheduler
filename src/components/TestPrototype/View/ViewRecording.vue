<template>
    <template v-if="!props.my.autoadvance">
        <v-btn 
            v-if="!props.my.autoadvance" 
            ref="buttonref">{{ message }}</v-btn>
    </template>
    <div v-else>
        <v-btn >Recording in progress</v-btn>
        <h1 v-if="seconds_remaining">Seconds remaining: {{ seconds_remaining }}</h1>
    </div>
</template>
<script setup lang="ts">
import {type Recording} from '@/types'
import {ref,  type Ref } from 'vue';
interface Props {
    my:Recording
    upload_files: File[]
    advance_stimulus:()=>void
}
const buttonref: Ref<HTMLElement|null> = ref(null) 
const message = ref("Enable Recording")
const seconds_remaining: Ref<null|number> = ref(null)

navigator.mediaDevices.getUserMedia({audio:true}).then(stream =>{
    const rec = new MediaRecorder(stream)
    const chunks:Blob[] = []
    rec.ondataavailable = (e) => {
        chunks.push(e.data)
    }
    function finish(){
        rec.stop()
        props.upload_files.push(
            new File([
                new Blob(chunks, { type: "audio/ogg; codecs=opus" })
            ], `${props.my.id}.ogg`)
        )
        props.advance_stimulus()
    }
    if (props.my.autoadvance && props.my.duration){
        rec.start(1000)
        seconds_remaining.value = props.my.duration
        function decrement(){
            if(seconds_remaining.value){
                if (seconds_remaining.value>0){
                    seconds_remaining.value--
                    setTimeout(decrement, 1000)
                } else{
                    seconds_remaining.value=null
                }
            }

        }
        setTimeout(finish, props.my.duration*1000)
        setTimeout(decrement, 1000)
    } else {
        message.value="Click to start recording"
        if (buttonref.value){
            buttonref.value.onclick = () => {
                rec.start()
                message.value="Click to stop recording"
                if(buttonref.value){
                    buttonref.value.onclick = finish
                }
            }
        }
    }
})
const props = defineProps<Props>()
</script>