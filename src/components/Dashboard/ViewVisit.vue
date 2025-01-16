<template>
    <span 
        ref="parent_span"
        class="j-dot" 
        :style="style">
        {{ props.my.sequence_no>=0 ? props.my.sequence_no : ' ' }}
        <v-overlay
            location-strategy="static"
            activator="parent"
            v-model="details_open"
        >
            <v-card class="j-hovercard">
                <v-card-title>
                    Participant: {{props.my.results[0].participant_id}}  {{ 
                        props.my.sequence_no !== -1 ? `Visit # ${props.my.sequence_no}` : 'Self-initiated' }}
                </v-card-title>
                <v-card-subtitle v-if="formal_timestamp">
                    Scheduled at: {{ formal_timestamp.toLocaleString() }}
                </v-card-subtitle>
                <v-card-subtitle v-else>
                    Self administered
                </v-card-subtitle>
                <v-card-subtitle v-if="real_timestamp">
                    Completed at: {{ real_timestamp.toLocaleString() }}
                </v-card-subtitle>
                <v-card-subtitle v-else>
                    Not yet submitted
                </v-card-subtitle>
                <v-card-subtitle v-if="schedule_ids.length===1">
                    Schedule id: {{ schedule_ids[0] }}
                </v-card-subtitle>
                <template v-else-if="schedule_ids.length>1">
                    <v-card-subtitle style="color: red;">
                        DUPLICATED SUBMISSIONS
                    </v-card-subtitle>
                    <v-card-subtitle v-for="schedule_id in schedule_ids">
                        Schedule id: {{ schedule_id }}
                    </v-card-subtitle>
                </template>
                <v-card-subtitle>
                    Test prototype id: {{ test_prototype_id }}
                </v-card-subtitle>
                <v-card-subtitle v-if="schedule_ids.length===1">
                    <p>Randomization order:</p>
                    <p v-for="r in randomization_reports.get(schedule_ids[0])!">{{ r }}</p>
                </v-card-subtitle>
                <v-card-subtitle v-else-if="schedule_ids.length>1">
                    <template v-for="schedule_id in schedule_ids">
                        <p>Randomization order for {{ schedule_id }}:</p>
                        <p v-for="r in randomization_reports.get(schedule_id)!">{{ r }}</p>
                    </template>
                </v-card-subtitle>
                <v-list>
                    <v-list-subheader>Tasks</v-list-subheader>
                    <v-list-item v-for="sr in props.my.results" variant="outlined">
                        <template v-if="[3,2,4].includes(sr.quality)">
                            <v-card>
                                <v-card-title>
                                    {{ sr.stimulus_id }}
                                </v-card-title>
                                <v-card-subtitle v-if="schedule_ids.length>1">
                                    Schedule id: {{ sr.schedule_id }}
                                </v-card-subtitle>
                                <v-card-text>
                                    <ViewEma :my="sr"
                                        :files="stimulus_map.get(sr.schedule_id!)!.get(sr.stimulus_id)!"
                                        v-if="stimuli_map.get(sr.stimulus_id)?.type==='ema'"
                                    />
                                    <ViewRecording :my="sr"
                                        :files="stimulus_map.get(sr.schedule_id!)!.get(sr.stimulus_id)!"
                                        :transcript="transcripts.get(sr.schedule_id!)!.get(sr.stimulus_id)"
                                        v-else-if="stimuli_map.get(sr.stimulus_id)?.type==='recording'"
                                    />
                                </v-card-text>
                            </v-card>
                        </template>
                        <template v-else-if="sr.quality===1">
                            <v-card>
                                <v-card-title>
                                    {{ sr.stimulus_id }}
                                </v-card-title>
                                <v-card-text>
                                    Past due
                                </v-card-text>
                            </v-card>
                        </template>
                        <template v-else-if="sr.quality===99">
                            <v-card>
                                <v-card-title>
                                    {{ sr.stimulus_id }}
                                </v-card-title>
                                <v-card-text>
                                    Sent within the last 2 days but not yet completed
                                </v-card-text>
                            </v-card>
                        </template>
                        <template v-else-if="sr.quality===0">
                            <v-card>
                                <v-card-title>
                                    {{ sr.stimulus_id }}
                                </v-card-title>
                                <v-card-text>
                                    Not yet due
                                </v-card-text>
                            </v-card>
                        </template>
                        <template v-else-if="sr.quality===100">
                            <v-card>
                                <v-card-title>
                                    {{ sr.stimulus_id }}
                                </v-card-title>
                                <v-card-text>
                                    Participant Dropped out
                                </v-card-text>
                            </v-card>
                        </template>
                    </v-list-item>
                    <template v-if="schedule_ids.length>1">

                    </template>
                    <v-list-item v-for="schedule_id in schedule_ids">
                        <v-btn @click="download_data(schedule_id)" >Download data for {{schedule_id}}</v-btn>
                    </v-list-item>
                </v-list>
                <v-card-actions>
                    <v-btn @click="download_data(schedule_ids[0])" v-if="schedule_ids.length===1">Download data</v-btn>
                    <v-btn @click.stop="close()">Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-overlay>
    </span>
    <v-dialog v-model=dialog_open>
        <v-card>
            <v-card-title>Download ready</v-card-title>
            <v-card-text><a :href="download_url" :download="download_name">{{ download_name }}</a></v-card-text>
            <v-card-actions>
                <v-btn @click="dialog_open=false">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script setup lang=ts>
import ViewEma from './ViewEma.vue'
import ViewRecording from './ViewRecording.vue'
import {ref, computed, inject, type Ref, watch} from 'vue'
import { response_stimuli_key, close_all_key, test_prototypes_key } from '@/injectkeys'
import type { Visit } from '@/types/schedule'
import type { Transcript } from '@/types'
import { get_src } from './dashboard_logic';


interface Props{
    my:Visit
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'open'): void
  (e: 'close'): void
}>()
const dialog_open = ref(false)

const stimuli_map = inject(response_stimuli_key)!
const test_prototypes = inject(test_prototypes_key)!
const details_open = ref(false)






function close(){
    details_open.value=false
}

const style = computed(()=>{
    switch(props.my.quality!){
        case 3 : return {
            'background-color':'seagreen',
            'color':'white'
        }
        case 2 : return {
            'background-color':'gold',
            'color':'black'
        }
        case 1 : return {
            'background-color':'maroon',
            'color':'white'
        }
        case 0 : return {
            'background-color':'white',
            'border': '2px solid black'
        }
        case 99 : return {
            'background-color':'blue',
            'color': 'white'
        }
        case 100 : return {
            'background-color':'darkgrey',
            'color':'white'
        }
        case 4 : return {
            'background': `repeating-linear-gradient(
                            to bottom,
                            yellow,
                            red 2em,
                            red)`,
            'color':'black'
        }
    }
})



const participant_id = computed(()=>{
    return props.my.results[0].participant_id
})

const test_prototype_id = computed(()=>{
    return props.my.results[0].test_prototype_id
})

const formal_timestamp = computed(()=>
    props.my.results[0].formal_timestamp
)
const real_timestamp = computed(()=>{
    const retval = []
    for (const sr of props.my.results){
        if(sr.real_timestamp){
            retval.push(sr.real_timestamp)
        }
    }
    retval.sort()
    if (retval.length>0){
        return retval.pop()
    } else{
        return undefined
    }
})

const schedule_ids = computed(()=>{
    const retval: Set<string> = new Set()
    for (const sr of props.my.results){
        if (sr.schedule_id){
            retval.add(sr.schedule_id)
        }
    }
    return Array.from(retval)
})

const file_urls: Ref<Map<string, string[]>> = ref(new Map())
const transcripts: Ref<Map<string, Map<string,Transcript>>> = ref(new Map())




watch(details_open, ()=>{
    if (file_urls.value.size===0){
        get_visit_files()
    }
})

function get_visit_files(){
    for(const schedule_id of schedule_ids.value){
        fetch(`/salsa/server/get-visit-files?${new URLSearchParams({schedule_id:schedule_id})}`).then( r=>
        r.json()
        ).then( s=>
            file_urls.value.set(schedule_id, s)
        )
        fetch(`/salsa/server/get-visit-transcriptions?${new URLSearchParams({schedule_id:schedule_id})}`).then( r=>
        r.json() as Promise<{stimulus_id:string, transcript:Transcript}[]>
        ).then( s=>
            transcripts.value.set(schedule_id, new Map(s.map(({stimulus_id, transcript}) => [stimulus_id, transcript])))
        )
    }
}

const randomization_reports: Ref<Map<string, string[]>> = ref(new Map())

const stimulus_map = computed(()=>{
    const final_retval = new Map<string, Map<string,string[]>>()
    file_urls.value.forEach((urls, schedule_id) =>{
        const retval = new Map<string, string[]>()
        final_retval.set(schedule_id, retval)
        urls.forEach( fl =>{
            console.log('fl', fl)
            const stimulus_id = fl.split('=').pop()?.split('.')[0]! //extracts stimulus id from url
            if (stimulus_id === 'randomization_report'){
                fetch(get_src(schedule_id, fl)).then( r=>
                    (r.json() as Promise<number[]>)
                ).then( ns =>{
                    const this_test_prototype_stimids = test_prototypes.value.filter(
                        tp => tp.id===props.my.results[0].test_prototype_id)[0].stimulus_ids
                    randomization_reports.value.set(schedule_id, ns.map(nss => this_test_prototype_stimids[nss]))
                })
            }
            else if (retval.has(stimulus_id)){
                retval.get(stimulus_id)?.push(fl)
            } else{
                retval.set(stimulus_id, [fl])
            }
        })
    })
    return final_retval
})

const parent_span=ref()

const download_url = ref('')
const download_name = ref('')

async function download_data(schedule_id:string){
    const retval = await(
        await fetch(`/salsa/server/get-visit-zip?${new URLSearchParams({schedule_id})}`)
    ).blob()
    download_url.value = URL.createObjectURL(retval)
    download_name.value = `${participant_id.value}|${schedule_id}.zip`
    dialog_open.value=true
}

</script>
<style>
.j-dot{
    height: 25px;
    width: 25px;
    border-radius: 50%;
    display: inline-block;
    text-align: center;
    &:hover{
        box-shadow: 0 10px 10px rgb(0 0 0 / 0.4);
    }
}
.j-hovercard{
    width: 600px;
    height:75vh;
    overflow-y: scroll;

}
.j-hiddencard{
    display: none;
}
</style>