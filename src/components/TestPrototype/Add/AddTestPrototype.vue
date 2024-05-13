<template>
    <v-text-field v-model="my.id" label="Enter test prototype's name"/>
    <j-list :items="my.stimuli" :mime_methods="upload_mime_methods">
        <template #preamble>
            <h2>Stimuli:</h2>
        </template>
        <template #renderer="{item:stim}">
            <div class="j_icont">
                <div class="j_imain">
                    <AddImage :my="stim" v-if="stim.type==='image'"/>
                    <AddVideo :my="stim" v-else-if="stim.type==='video'"/>
                    <AddRecording :my="stim" v-else-if="stim.type==='recording'"/>
                    <AddEma :my="stim" v-else-if="stim.type==='ema'"/>
                    <AddAudio :my="stim" v-if="stim.type==='audio'"/>
                </div>
                <div class="j_idelete">
                    <v-btn @click="delete_stim(stim)">Delete stimulus {{ stim.id }}</v-btn>
                </div>
            </div>
        </template>
        <template #postamble>
            <span>
                <v-text-field label="Stimulus id" v-model="stimid"/>
                <v-select v-model="StimulusType" label="Stimulus type" :items="['audio', 'video', 'image', 'recording', 'ema']"/>
                <v-btn @click="add_stim()" :disabled="button_active">Add stimulus ➕</v-btn> 
                <j-btn :click="submit_test_prototype" :arg0="null" :disabled="not_has_stimuli">Upload test prototype</j-btn>
            </span>
        </template>
    </j-list>
</template>
<script setup lang="ts">
import AddEma from '@/components/TestPrototype/Add/AddEma.vue'
import AddRecording from '@/components/TestPrototype/Add/AddRecording.vue'
import AddAudio from '@/components/TestPrototype/Add/AddAudio.vue'
import AddImage from '@/components/TestPrototype/Add/AddImage.vue'
import AddVideo from '@/components/TestPrototype/Add/AddVideo.vue'
import {type Ema as EmaType, type Image as ImageType, type Audio as AudioType, 
        type Video as VideoType, type Recording as RecordingType, type TestPrototype as TestPrototypeType,
        type VideoRecording as VideoRecordingType, type PictureCapture as PictureCaptureType,
        type Stimulus as StimulusType} from '@/types'
import JList from '@/components/JList.vue'
import JBtn from '@/components/JBtn.vue'
import {ref, type Ref, inject, computed, type ComputedRef, reactive}from 'vue'
import { project_key } from '@/injectkeys'
import { files } from 'jszip'
import { mapToStyles } from '@popperjs/core/lib/modifiers/computeStyles'

interface Props {
    my?:TestPrototypeType
}
const props = defineProps<Props>()

let my:TestPrototypeType = reactive({id:'', stimuli:[]})
if (props.my){
    my = props.my
}

const project = inject(project_key)!
function delete_stim(stim:StimulusType){
    my.stimuli.splice(my.stimuli.indexOf(stim), 1)
}
const stimid = ref("")
const StimulusType = ref("")
function add_stim(){
    const type = StimulusType.value
    const id = stimid.value
    const uri = ''
    const autoadvance = false
    const duration = 0
    const file: File[] = []
    if (type==='audio'){
        my.stimuli.push({
            type,
            id,
            uri,
            autoadvance,
            duration,
            file
        })
    }
    else if (type==='video'){
        my.stimuli.push({
            type,
            id,
            uri,
            autoadvance,
            duration,
            file
        })
    }
    else if (type==='image'){
        my.stimuli.push({
            type,
            id,
            uri,
            autoadvance,
            duration,
            file
        })
    }
    else if (type==='ema'){
        my.stimuli.push({
            type,
            id,
            form:[]
        })
    }
    else if (type==='recording'){
        my.stimuli.push({
            type,
            id,
            autoadvance,
            duration,
        })
    }
    stimid.value = ''
}
function accept_image(f:File, idx:number){
    const new_stimulus:ImageType = {
        id: f.name,
        type:'image',
        uri:f.name,
        file:[f],
        autoadvance:false,
        duration:0
    }
    if (idx===-1){
        my.stimuli.push(new_stimulus)
    } else{
        my.stimuli
        my.stimuli.splice(idx,0, new_stimulus)
    }
}
function accept_video(f:File, idx:number){
    const new_stimulus:VideoType = {
        id: f.name,
        type:'video',
        uri:f.name,
        file:[f],
        autoadvance:false,
        duration:0
    }
    if (idx===-1){
        my.stimuli.push(new_stimulus)
    } else{
        my.stimuli
        my.stimuli.splice(idx,0, new_stimulus)
    }
}
function accept_audio(f:File, idx:number){
    const new_stimulus:AudioType = {
        id: f.name,
        type:'audio',
        uri:f.name,
        file:[f],
        autoadvance:false,
        duration:0
    }
    if (idx===-1){
        my.stimuli.push(new_stimulus)
    } else{
        my.stimuli
        my.stimuli.splice(idx,0, new_stimulus)
    }
}
const upload_mime_methods = new Map()
upload_mime_methods.set('image/png', accept_image)
upload_mime_methods.set('image/jpeg', accept_image)
upload_mime_methods.set('audio/wav', accept_audio)
upload_mime_methods.set('video/mp4', accept_video)







const button_active = computed(()=>{
    if (stimid.value.length>0 && StimulusType.value.length>0){
        return false
    } else {
        return true
    }
})
const not_has_stimuli = computed(() => ! (my.stimuli.length>0))


function submit_test_prototype(){
    const fdata = new FormData()
    const json_obj = []
    for (let s of my.stimuli){
        if (s.type === 'image' || s.type === 'video' || s.type === 'audio'){
            fdata.append(s.file[0].name, s.file[0])
            const {file:_, ...pushval} = s
            json_obj.push(pushval)
        } else {
            json_obj.push(s)
        }
    }
    fdata.append('metadata.json', JSON.stringify(json_obj))
    return fetch('/salsa/server/add-test-prototype?' + new URLSearchParams({
        project: project,
        id: my.id
    }), {
        method:'POST',
        body:fdata
    })
}

</script>
<style src="@/css/jview.css"/>
<style>
.ipt{
    background-color: white;
    border: solid black;
}
.btn {
    background-color: grey;
    &:hover{
        border: inset 3px black;
    }
}
</style>