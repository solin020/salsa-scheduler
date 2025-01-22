<template>
<span 
        ref="parent_span"
        :style="{
            'background-color':'white',
            'border': '2px solid black',
            'font-size': '24pt'
        }">
        🔎
            <v-overlay
                location-strategy="static"
                activator="parent"
                v-model="details_open"
            >
                <v-card class="j-schedulecard">
                    <v-card-title>Overview for {{ props.participant_id }}</v-card-title>
                    <v-card-subtitle>                            
                        <v-btn @click.stop="close()">Close</v-btn>
                    </v-card-subtitle>
                    <v-table class="j-dashboard-table">
                        <thead>
                            <th>Stimulus</th>
                            <th v-for="pid in phase_ids">{{ pid }}</th>
                        </thead>
                        <tbody>
                            <tr v-for="us in unique_stimuli">
                                <td>{{ us.id }}: </td>
                                <td v-for="pid in phase_ids">
                                    <template v-for="visit in sort_visits(visit_data.get(pid)!)">
                                        <span
                                        class="j-dot" 
                                        :style="calculate_style(us.id, visit.results)"

                                        >{{visit.sequence_no}}</span>
                                    </template>
                                </td>
                            </tr>
                        </tbody>
                    </v-table>
                </v-card>
            </v-overlay>
    </span>
</template>
<script setup lang="ts">
import {ref, inject} from 'vue'
import { unique_stimuli_key, phase_ids_key } from '@/injectkeys'
import type { Visit } from '@/types/schedule'
const details_open = ref(false)
const props = defineProps<{
    participant_id:string
    visit_data: Map<string | -1, Visit[]>
}>()
function close(){
    details_open.value=false
}
const unique_stimuli = inject(unique_stimuli_key)!
const phase_ids = inject(phase_ids_key)!
function sort_visits(vv:Visit[]){
    return vv.sort((v1,v2) => v1.sequence_no - v2.sequence_no)
}
function calculate_style(us:string, results: Visit['results']){
    const res = results.filter(r=>r.stimulus_id===us)
    if (res.length > 1){
        return {
            'background': `repeating-linear-gradient(
                            to bottom,
                            yellow,
                            red 2em,
                            red)`,
            'color':'black'
        }
    } else if (res.length<1){
        return {
            'background-color':'darkgrey',
            'color':'white'
        }
    } else{
        switch(res[0].quality){
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
            case 98 : return {
                'background-color':'lightblue',
                'color': 'black'
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
    }
    
}

</script>