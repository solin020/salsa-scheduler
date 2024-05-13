<template>
    <div>
        <div v-if="my">
            <div v-if="edit_mode">
                <v-btn @click="edit_mode=false">View this test prototype</v-btn>
                <AddTestPrototype :my="my"/>
            </div>
            <div v-else>
                <div>
                    <v-btn @click="edit_mode=true">Edit this test prototype</v-btn>
                </div>
                <div>
                    <v-btn @click="simulate_test()">Open test simulation window</v-btn>
                </div>
                <div v-if="test_ready">
                    <Popup>
                        <template #open>
                            <v-btn>Begin test</v-btn>
                        </template>
                        <template #content>
                            <div v-if="current_stimulus" class="j_phone_sim">
                                <h2>Phone Test Simulation</h2>
                                <ViewAudio :my="(current_stimulus as AudioType)" :advance_stimulus="advance_stimulus" v-if="current_stimulus.type==='audio'"/>
                                <ViewImage :my="(current_stimulus as ImageType)" :advance_stimulus="advance_stimulus" v-else-if="current_stimulus.type==='image'"/>
                                <ViewVideo :my="(current_stimulus as VideoType)" :advance_stimulus="advance_stimulus" v-else-if="current_stimulus.type==='video'"/>
                                <ViewRecording :my="(current_stimulus as RecordingType)"
                                    :advance_stimulus="advance_stimulus"
                                    v-else-if="current_stimulus.type==='recording'"
                                    :upload_files="upload_files"/>
                                <ViewEma :my="(current_stimulus as EmaType)"
                                    :advance_stimulus="advance_stimulus"
                                    v-else-if="current_stimulus.type==='ema'"
                                    :upload_files="upload_files"/>
                            </div>
                            <div v-else>
                                <j-btn :click="upload_test_results" :arg0="undefined">Submit test results</j-btn>
                            </div>
                        </template>
                    </Popup>
                </div>
            </div>
        </div>
        <div v-else>
            <v-progress-circular indeterminate/>
        </div>
    </div>
</template>
<script setup lang="ts">
import ViewEma from '@/components/TestPrototype/View/ViewEma.vue'
import ViewRecording from '@/components/TestPrototype/View/ViewRecording.vue'
import ViewAudio from '@/components/TestPrototype/View/ViewAudio.vue'
import ViewImage from '@/components/TestPrototype/View/ViewImage.vue'
import ViewVideo from '@/components/TestPrototype/View/ViewVideo.vue'
import AddTestPrototype from '../Add/AddTestPrototype.vue'
import {type Ema as EmaType, type Image as ImageType, type Audio as AudioType, 
        type Video as VideoType, type Recording as RecordingType, type TestPrototype as TestPrototypeType,
    type Stimulus as StimType} from '@/types'
import {ref, type Ref, inject, computed, type ComputedRef}from 'vue'
import { project_key } from '@/injectkeys'
import { DefaultService } from '@/client'
import upload_message_response from '@/pgp'
import Popup from '@/components/Popup.vue'
import JBtn from '@/components/JBtn.vue'

console.log('test prototype setup')
const active_idx = ref(0)
function advance_stimulus(){
    if(my.value){
        if (active_idx.value + 1 >= my.value.stimuli.length){
            active_idx.value=-1
        } else{
            active_idx.value++
        }
    }
}

function upload_test_results(_:undefined){
    // @ts-expect-error
    return upload_message_response(upload_files.value, 'testsubject', my.value.id).then( () =>{
        test_ready.value=false
    })

}


interface Props{
    id: string
}
const props = defineProps<Props>()
const project = inject(project_key)!
const my:Ref<TestPrototypeType|null> = ref(null)

const upload_files: Ref<File[]> = ref([])
const current_stimulus:ComputedRef<StimType|undefined> = computed(() =>{
    if(my.value){
        return my.value.stimuli[active_idx.value]
    }
})
const edit_mode = ref(false)
//This exceedingly nasty code loads all of the test prototype's files into the browser
DefaultService.getTestPrototypeFilesSalsaServerGetTestPrototypeFilesGet(props.id).then((pathlist) => {
        const full_pathlist = pathlist.map(
            filepath => ('/salsa/server/get-test-prototype-file?' + (new URLSearchParams({
                id:props.id,
                filepath: filepath
            })).toString())
        )
        const metadatapath = full_pathlist.filter(s => s.endsWith('metadata.json'))[0]
        let tp: TestPrototypeType
        fetch(metadatapath).then( r=> r.json()).then(s =>{
            tp = {id:props.id, stimuli:s}
            let filecount = 0
            for (let i=0; i<tp.stimuli.length;i++){
                const stim = tp.stimuli[i]
                if (['image', 'video', 'audio'].includes(stim.type)){
                    // @ts-expect-error
                    const this_stim: (ImageType|VideoType|AudioType) = stim
                    const filepath = full_pathlist.filter(s => s.endsWith(this_stim.uri))[0]
                    fetch(filepath).then(r => r.blob()).then( b=>{
                        console.log(filepath, 'filepath retrieved')
                        this_stim.file = [new File([b], this_stim.uri)]
                        filecount += 1
                        if(filecount===full_pathlist.length-1){
                            my.value = tp
                        }
                    })
                }
            }
        })
    }
)

const test_ready=ref(false)
function simulate_test(){
    active_idx.value = 0
    test_ready.value=true
}
</script>
<style>
.j_phone_sim{
    width: 380px;
    height:660px;
    border-bottom: solid black 10px;
    border-top: solid black 10px;
    border-left: solid black 3px;
    border-right: solid black 3px;
    border-radius: 30px;
    background-color: white;
    padding: 30px;
}
</style>
