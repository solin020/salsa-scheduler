<template>
    <v-select 
            :items="schedule_prototype_ids" 
            v-model="current_schedule_prototype_id" 
            label="Select longitudinal study to review"
        />
    <template v-if="ready">
        <j-tabs :tabnames="['overview', 'participants']">
            <template #header_overview>
                Overview
            </template>
            <template #content_overview>
                <v-table class="j-dashboard-table">
                    <thead>
                        <tr>
                            <th style="max-width: 20em; min-width: 20em;" :colspan="td_span">
                                Number of participants: {{ participant_data.size }}
                                <br/>
                                Visits to date: {{ visit_counts.all_stimuli.whole_schedule.finished }}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td :colspan="td_span">
                                <details open>
                                    <summary>Summary</summary>
                                    <v-table>
                                        <phase-headers :phase_ids="phase_ids"/>
                                        <tbody>
                                            <tr>
                                                <th style="max-width: 20em; min-width: 20em;">Completed</th>
                                                <td>
                                                    {{visit_counts.all_stimuli.whole_schedule.good_quality}}
                                                    ({{ percent_render(visit_counts.all_stimuli.whole_schedule.fraction_good) }})
                                                </td>
                                                <td v-for="phase_stats of visit_counts.all_stimuli.phases.values()">
                                                    {{phase_stats.good_quality}} ({{ percent_render(phase_stats.fraction_good) }})
                                                </td>
                                            </tr>
                                            <tr>
                                                <th>Partially completed</th>
                                                <td>
                                                    {{visit_counts.all_stimuli.whole_schedule.low_quality}}
                                                    ({{ percent_render(visit_counts.all_stimuli.whole_schedule.fraction_bad) }})
                                                </td>
                                                <td v-for="phase_stats of visit_counts.all_stimuli.phases.values()">
                                                    {{phase_stats.low_quality}} ({{ percent_render(phase_stats.fraction_bad) }})
                                                </td>
                                            </tr>
                                            <tr>
                                                <th>Not completed</th>
                                                <td>
                                                    {{visit_counts.all_stimuli.whole_schedule.missed}}
                                                    ({{ percent_render(visit_counts.all_stimuli.whole_schedule.fraction_missed) }})
                                                </td>
                                                <td v-for="phase_stats of visit_counts.all_stimuli.phases.values()">
                                                    {{phase_stats.missed}} ({{ percent_render(phase_stats.fraction_missed) }})
                                                </td>
                                            </tr>
                                            <tr>
                                                <th>Not yet due</th>
                                                <td>
                                                    {{visit_counts.all_stimuli.whole_schedule.future}}
                                                </td>
                                                <td v-for="phase_stats of visit_counts.all_stimuli.phases.values()">
                                                    {{phase_stats.future}} 
                                                </td>
                                            </tr>
                                            <tr>
                                                <th>Dropouts</th>
                                                <td>
                                                    {{visit_counts.all_stimuli.whole_schedule.dropout}}
                                                </td>
                                                <td v-for="phase_stats of visit_counts.all_stimuli.phases.values()">
                                                    {{phase_stats.dropout}} 
                                                </td>
                                            </tr>
                                        </tbody>
                                    </v-table>
                                </details>
                            </td>
                        </tr>
                        <tr>
                            <td :colspan="td_span">
                                <details>
                                    <summary>Data by indivual stimuli</summary>
                                    <v-table>
                                        <phase-headers :phase_ids="phase_ids"/>
                                        <tbody>
                                            <template v-for="stim, i in unique_stimuli">
                                                <tr :class="{'border-top':i===0}"
                                                    >
                                                    <th style="max-width: 20em; min-width: 20em;"> {{ stim.id }} good quality </th>
                                                    <td>
                                                    {{percent_render(visit_counts.by_stim_type.get(stim.id)!.whole_schedule.good_quality)}}
                                                    ({{ percent_render(visit_counts.by_stim_type.get(stim.id)!.whole_schedule.fraction_good) }})
                                                    </td>
                                                    <td v-for="phase_stats in visit_counts.by_stim_type.get(stim.id)!.phases.values()">
                                                    {{phase_stats.good_quality}} ({{ percent_render(phase_stats.fraction_good) }})
                                                    </td>
                                                </tr>
                                                <tr :class="{'border-top':i===0}"
                                                    >
                                                    <th> {{ stim.id }} quality issues </th>
                                                    <td>
                                                    {{percent_render(visit_counts.by_stim_type.get(stim.id)!.whole_schedule.low_quality)}}
                                                    ({{ percent_render(visit_counts.by_stim_type.get(stim.id)!.whole_schedule.fraction_bad) }})
                                                    </td>
                                                    <td v-for="phase_stats in visit_counts.by_stim_type.get(stim.id)!.phases.values()">
                                                    {{phase_stats.low_quality}} ({{ percent_render(phase_stats.fraction_bad) }})
                                                    </td>
                                                </tr>
                                                <tr :class="{'border-top':i===0}"
                                                    >
                                                    <th> {{ stim.id }} missed </th>
                                                    <td>
                                                    {{percent_render(visit_counts.by_stim_type.get(stim.id)!.whole_schedule.missed)}}
                                                    ({{ percent_render(visit_counts.by_stim_type.get(stim.id)!.whole_schedule.fraction_missed) }})
                                                    </td>
                                                    <td v-for="phase_stats in visit_counts.by_stim_type.get(stim.id)!.phases.values()">
                                                    {{phase_stats.missed}} ({{ percent_render(phase_stats.fraction_missed) }})
                                                    </td>
                                                </tr>
                                            </template>
                                        </tbody>
                                    </v-table>
                                </details>
                            </td>
                        </tr>
                        <tr>
                            <td colspan=2>
                                <details>
                                    <summary>Self-initiated</summary>
                                    <v-table>
                                        <tbody>
                                            <tr v-for="stim, i in default_stimuli">
                                                <th style="max-width: 20em; min-width: 20em;"> Self initiated {{ stim.id }} </th>
                                                <td> {{ visit_counts.by_default_stim_type.get(stim.id)!.finished }}</td>
                                            </tr>
                                        </tbody>
                                    </v-table>
                                </details>
                            </td>
                        </tr>
                    </tbody>
                </v-table>
            </template>
            <template #header_participants>
                View by Participant
            </template>
            <template #content_participants>
                <v-table>
                    <thead>
                        <tr>
                            <th>Participant id</th>
                            <th></th>
                            <th v-for="phase in current_schedule_prototype.phases">
                                {{ phase.id }}
                            </th>
                            <th>
                                Tests taken outside of schedule
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="[participant_id, visit_data] in participant_data.entries()">
                            <th 
                                v-if="participant_has_data(participant_data, participant_id)"
                                @click="download_participant_data(participant_id)"
                                class="j-download"
                            >
                                {{participant_id}}⬇
                            </th>
                            <th 
                                v-else
                                class="j-download-empty"
                            >
                                {{participant_id}}⬇
                            </th>
                            <td>
                                <j-btn :click="dropout_participant" :arg0="participant_id">
                                    Dropout participant {{ participant_id }}
                                </j-btn>
                            </td>
                            <td v-for="phase in current_schedule_prototype.phases">
                                <ViewVisit 
                                    v-for="visit,i in sort_visits(visit_data.get(phase.id)||[])"
                                    :my="visit"
                                />
                            </td>
                            <td>
                                <ViewVisit 
                                    v-for="visit,i in sort_visits(visit_data.get(-1)||[])"
                                    :my="visit"
                                />
                            </td>
                        </tr>
                    </tbody>
                </v-table>
            </template>
        </j-tabs>
    </template>
    <v-progress-circular indeterminate v-else/>
    <v-dialog v-model="dialog_open">
        <v-card>
            <v-card-title>Download ready</v-card-title>
            <v-card-text><a :href="download_url" :download="download_name">{{ download_name }}</a></v-card-text>
            <v-card-actions>
                <v-btn @click="dialog_open=false">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <v-btn @click="download_csv_data" v-if="current_schedule_prototype_id">Download only csv survey data for study {{ current_schedule_prototype_id }}</v-btn>
    <v-btn @click="download_study_data" v-if="current_schedule_prototype_id">Download data for study {{ current_schedule_prototype_id }}</v-btn>
    <v-btn @click="download_project_data">Download all data for project {{ project }}</v-btn>
</template>
<script setup lang=ts>

import {inject, ref, type Ref, computed, watch, provide} from 'vue'
import { 
    schedule_prototype_list_key, project_key, test_prototypes_key, response_stimuli_key,
    close_all_key
 } from '@/injectkeys'
import type {SchedulePrototype, ResponseStimulus, TestPrototypeChoice} from '@/types/schedule'
import ViewVisit from './ViewVisit.vue'
import JTabs from '../JTabs.vue'
import JBtn from '../JBtn.vue'
import PhaseHeaders from './PhaseHeaders.vue'
import { get_unique_stimuli, count_visits, participant_has_data } from './dashboard_logic'
import type { StimulusResult, Visit } from '@/types/schedule'



const ready = ref(false)


const schedule_prototypes = inject(schedule_prototype_list_key)!
const test_prototypes = inject(test_prototypes_key)!
const project = inject(project_key)!

const schedule_prototype_ids = computed(()=>
    schedule_prototypes.value.map(s => s.schedule_id)
)
const current_schedule_prototype_id = ref(schedule_prototypes.value[0].schedule_id)
const current_schedule_prototype = computed(()=>
    schedule_prototypes.value.filter(s => s.schedule_id === current_schedule_prototype_id.value)[0]
)
const phase_ids = computed(()=>current_schedule_prototype.value.phases.map(p => p.id))

const data: Ref<StimulusResult<'parsed'>[]> = ref([])
async function get_data(){
    ready.value=false
    const data_unparsed: StimulusResult<'unparsed'>[]  = (await (await fetch('/salsa/server/api/get-dashboard-data?' + new URLSearchParams({
        project, schedule_prototype_id:current_schedule_prototype.value.schedule_id
    }))).json()) 
    console.log('dunparsed', data_unparsed)
    data.value = data_unparsed.map(dr => ({
        ...dr,
        formal_timestamp: dr.formal_timestamp? new Date(dr.formal_timestamp):undefined,
        real_timestamp: dr.real_timestamp? new Date(dr.real_timestamp):undefined
    }))
    ready.value=true
}
get_data()
watch(current_schedule_prototype, ()=>{
    if (current_schedule_prototype.value.schedule_id){
        get_data()
    }
})


const unique_stimuli = computed(()=>
    get_unique_stimuli(test_prototypes.value, current_schedule_prototype.value)
)


const default_stimuli = computed(()=>{
    const x = current_schedule_prototype.value.default_selection
    if (x){
        if (x.type==='fixed'){
            return test_prototypes.value.filter( tp =>
            tp.id === x.test_prototype_id
            )[0].response_stimuli
        } else if (x.type==='random' || x.type==='choose'){
            const retval: Map<string,{
                id: string;
                    type: "recording" | "ema";
            }> = new Map()
            test_prototypes.value.filter( tp =>
                x.test_prototype_ids.includes(tp.id)
            ).forEach(ttp => ttp.response_stimuli.forEach(rr => retval.set(rr.id, rr)))
            return Array.from(retval.values())
        } else{
            return []
        }
    } else{
        return []
    }
})
const all_stimuli = computed(()=>
    new Map([...unique_stimuli.value, ...default_stimuli.value].map(
        s => [s.id, s]
    ))
)
provide(response_stimuli_key, all_stimuli)

const visit_stats = computed(()=>
    count_visits(data.value, unique_stimuli.value, default_stimuli.value, current_schedule_prototype.value)
)
const visit_counts = computed(()=>visit_stats.value[0])
const participant_data = computed(()=>visit_stats.value[1])
const td_span = computed(()=>visit_counts.value.all_stimuli.phases.size + 2)



function percent_render(frac: number){
    if (isNaN(frac)){
        return 'N/A'
    }
    return (frac * 100).toFixed(2) + '%'
}

const dialog_open = ref(false)
const download_url = ref('')
const download_name = ref('')

function sort_visits(vv:Visit[]){
    return vv.sort((v1,v2) => v1.sequence_no - v2.sequence_no)
}

async function download_participant_data(participant_id:string){
    const resp =  (await (
        await fetch(`/salsa/server/get-participant-zip?${new URLSearchParams({participant_id})}`)
    ).blob())
    download_url.value = URL.createObjectURL(resp)
    download_name.value = `${participant_id}.zip`
    dialog_open.value=true
}

async function download_csv_data(){
    const resp =  (await (
        await fetch(`/salsa/server/get-schedule-csv?${new URLSearchParams({
            project,
            schedule_prototype_id: current_schedule_prototype_id.value
        })}`)
    ).blob())
    download_url.value = URL.createObjectURL(resp)
    download_name.value = `${current_schedule_prototype_id.value}.zip`
    dialog_open.value=true
}

async function download_study_data(){
    const resp =  (await (
        await fetch(`/salsa/server/get-study-zip?${new URLSearchParams({
            project,
            schedule_prototype_id: current_schedule_prototype_id.value
        })}`)
    ).blob())
    download_url.value = URL.createObjectURL(resp)
    download_name.value = `${current_schedule_prototype_id.value}.zip`
    dialog_open.value=true
}

async function download_project_data(){
    const resp =  (await (
        await fetch(`/salsa/server/get-project-zip?${new URLSearchParams({project})}`)
    ).blob())
    download_url.value = URL.createObjectURL(resp)
    download_name.value = `${project}.zip`
    dialog_open.value=true
}

async function dropout_participant(id: string): Promise<Response>{
    const proceed = confirm(`Are you sure you want to drop out participant ${id}`)
    //@ts-expect-error
    if (!proceed){return}
    const retval =  fetch('/salsa/server/api/drop-participant?' + new URLSearchParams({id}),{method:'PATCH'})
    retval.then(r => {
        if (r.status===200){
            alert(`Participant ${id} dropped out succesfully! Please reload webpage`)
        }
    })
    return retval
}



</script>
<style>
.blank_row_before {
    border-top:10px solid #FFFFFF;
}
.j-dashboard-table th
.j-dashboard-table td  {
    text-align: left;
}
.j-download{
    color: blue;
    text-decoration: underline;
    cursor:pointer;
}
.j-download-empty{
    color: grey;
    text-decoration: underline;
}

</style>