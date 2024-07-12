<template>
    <v-form v-model="form_valid">
        <v-card variant="outlined">
            <v-card-title>
                Schedule metadata
            </v-card-title>
            <v-card-text>
                <v-form>
                    <v-text-field 
                        style="width: 30vw;"
                        density="compact" v-model="my.schedule_id" label="Enter schedule prototype name"/>
                    <v-select 
                        style="width: 30vw;"
                    density="compact" :items="[twilio_nicknames]" label="Select twilio config nickname" v-model="my.twilio_info"/>
                </v-form>
            </v-card-text>
            <v-card>
                <v-card-title>
                    Schedule level defaults
                </v-card-title>
                <v-card-text>
                    <prototype-selection
                        :level="'base'"
                        :parent_phase="undefined"
                        :my="my"
                        :parent_schedule="undefined"
                    />
                    <timing-selection
                        :level="'base'"
                        :parent_phase="undefined"
                        :my="my"
                        :parent_schedule="undefined"
                    />
                </v-card-text>
            </v-card>
        </v-card>
        <v-card variant="outlined">
            <v-card-title>
                Schedule phases
            </v-card-title>
            <v-card-text>
                <v-expansion-panels>
                    <v-expansion-panel v-for="phase in my.phases" :title="`Phase ${phase.phase_id}`">
                        <v-container>
                            <v-row>
                                <v-col cols="12" lg="3">
                                    <v-text-field density="compact" v-model="phase.phase_id"/><br>
                                    <v-select :items="['daily', 'weekly']" v-model="phase.spec.cadence" label="Schedule by days or weeks" /><br>
                                    <v-card>
                                        <v-card-title>
                                            Phase level defaults
                                        </v-card-title>
                                        <v-card-text>
                                            <prototype-selection
                                                    :level="'phase'"
                                                    :parent_phase="undefined"
                                                    :my="phase"
                                                    :parent_schedule="my"
                                                />
                                            <timing-selection
                                                    :level="'phase'"
                                                    :parent_phase="undefined"
                                                    :my="phase.spec"
                                                    :parent_schedule="my"
                                                />
                                        </v-card-text>
                                    </v-card>
                                    <v-btn @click="add_test(phase.spec)">Add a new testdate</v-btn>
                                    <v-btn @click="delete_phase(phase)">Add a new testdate</v-btn>
                                </v-col>
                                <v-col cols="12" lg="9">
                                    <v-container >
                                        <v-row>
                                            <v-col v-for="test, i in phase.spec.tests" :key="i" cols="12" lg="3">
                                                <v-card variant="outlined">
                                                    <v-card-text>
                                                        <template v-if="phase.spec.cadence==='daily'">
                                                            Years after startdate: <v-number-input control-variant="stacked" density="compact"  :step="1" :min="0" v-model="phase.spec.tests[i].datetime.year"/><br>
                                                            Days after startdate: <v-number-input control-variant="stacked" density="compact"  :step="1" :min="0" v-model="phase.spec.tests[i].datetime.day"/><br>
                                                        </template>
                                                        <template v-else-if="phase.spec.cadence==='weekly'">
                                                            Weeks after startdate: <v-number-input control-variant="stacked" density="compact"  :step="1" :min="0" v-model="phase.spec.tests[i].datetime.week"/>
                                                            Weekday: <v-select
                                                                :items="[{
                                                                    title:'Sunday',
                                                                    value:0
                                                                },{
                                                                    title:'Monday',
                                                                    value:1
                                                                },{
                                                                    title:'Tuesday',
                                                                    value:2
                                                                },{
                                                                    title:'Wednesday',
                                                                    value:3
                                                                },{
                                                                    title:'Thursday',
                                                                    value:4
                                                                },{
                                                                    title:'Friday',
                                                                    value:5
                                                                },{
                                                                    title:'Saturday',
                                                                    value:6
                                                                },]"
                                                                item-title="title"
                                                                item-value="value"
                                                                v-model="phase.spec.tests[i].datetime.weekday"
                                                            /><br>
                                                        </template>

                                                        </v-card-text>
                                                </v-card>
                                                <prototype-selection 
                                                            :level="'entry'" 
                                                            :my="test"
                                                            :parent_phase="phase"
                                                            :parent_schedule="my"
                                                        />
                                                <timing-selection 
                                                    :level="'entry'" 
                                                    :my="test"
                                                    :parent_phase="phase"
                                                    :parent_schedule="my"
                                                />
                                            </v-col>
                                        </v-row>
                                    </v-container>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-expansion-panel>
                </v-expansion-panels>
            </v-card-text>
        </v-card>
        <v-card variant="outlined">
            <v-btn @click="add_phase">Add a new phase</v-btn>
        </v-card>
        <v-card variant="outlined">
            <v-card-title>
                Select sample start date below to view a preview of the schedule
            </v-card-title>
            <v-card-text>
                <date-picker 
                    v-model="sample_startdate" 
                    :attributes="preview_events"
                    :rows="4"
                    :columns="3"/>
            </v-card-text>
            <v-card-actions>
                <v-btn @click="generate_preview()">Generate preview schedule</v-btn>
            </v-card-actions>
        </v-card>
        <j-btn :click="upload_schedule" :arg0="undefined" >Upload schedule</j-btn>
    </v-form>
</template>
<script setup lang="ts">
import type {PhaseSpec, SchedulePrototype} from 'src/types/schedule'
import {VNumberInput} from 'vuetify/labs/components'
import {DatePicker } from 'v-calendar'
import PrototypeSelection from './PrototypeSelection.vue'
import TimingSelection from './TimingSelection.vue'
import {ref, type Ref, computed, inject} from 'vue'
import { prepare_schedule_for_participant,
    prepare_schedule_for_upload,
 } from './schedule_logic'
import { test_prototypes_key, groups_key, twilio_key, project_key } from '@/injectkeys'
import JBtn from '../JBtn.vue'

const test_prototypes = inject(test_prototypes_key)!
const test_prototype_ids = computed(()=>test_prototypes.value.map(tp=>tp.id))
const twilios = inject(twilio_key)!
const twilio_nicknames = computed(()=>twilios.value.map(t=>t.nickname))
const project = inject(project_key)!

const sample_startdate = ref(new Date())

const form_valid = ref(false)





const my: Ref<SchedulePrototype<'website'>> = ref({
    schedule_id:'',
    phases:[],
    twilio_info:'',
    participant_timezone:undefined,
    allow_unscheduled:true,
    default_results:undefined,
    prototype_selection:undefined,
    participant_id:undefined
})



const preview_schedule: Ref<SchedulePrototype<'device'>|undefined> = ref() 
const preview_events = computed(()=>{
    if (preview_schedule.value){
        const retval: {popover:{label:string}, dates:Date, highlight:{style:{backgroundColor:string}}}[] = []
        for (const phase of preview_schedule.value.phases){
            for (const test of phase.spec.tests){
                console.log(phase.spec.tests)
                const [date_s, time_s, ] = test.formal_timestamp.split(' ')
                const [hour_i, minute_i] = time_s.split(':').map(s => parseInt(s))
                const [year_i, month_i, day_i] = date_s.split('/').map(s => parseInt(s))
                const calendar_date = new Date(year_i, month_i-1, day_i, hour_i, minute_i)
                retval.push({
                    highlight: {
                        style:{
                            backgroundColor:test_prototype_color_map[test.prototype_selection.test_prototype_id]
                        }
                    } ,
                    dates:calendar_date,
                    popover:{label:`${calendar_date.toLocaleTimeString(navigator.language, {hour12:true, hour: '2-digit', minute:'2-digit'})} - ${test.prototype_selection.test_prototype_id}`},
                })
            }
        } 
        console.log('events', retval)
        return retval
    }
})



function add_test(spec: PhaseSpec<'website'>){
    if (spec.cadence === 'daily'){
        const t = spec.tests[spec.tests.length-1]
        if (t) {
            spec.tests.push({
                datetime:{
                    year: t.datetime.year,
                    day: t.datetime.day+1
                },
                timing: {...t.timing},
                prototype_selection:{...t.prototype_selection},
                sequence_no:undefined
            })
        }else{
            spec.tests.push({
                datetime:{
                    year: 0,
                    day: 1
                },
                timing: {
                    type:'inherit'
                },
                prototype_selection:{type:'inherit'},
                sequence_no:undefined
            })
        }
    } else if (spec.cadence === 'weekly'){
        const t = spec.tests[spec.tests.length-1]
        if (t) {
            spec.tests.push({
                datetime:{
                    week: t.datetime.week+1,
                    weekday: t.datetime.weekday
                },
                prototype_selection:{...t.prototype_selection},
                timing: {...t.timing},
                sequence_no:undefined
            })
        }else{
            spec.tests.push({
                datetime:{
                    week: 1,
                    weekday: 1
                },
                timing: {
                    type:'inherit'            
                },
                prototype_selection:{type:'inherit'},
                sequence_no:undefined
            })
        }
    }
}


function add_phase(){
    my.value.phases.push({
        phase_id: 'new phase',
        prototype_selection:undefined,
        spec: {
            cadence: 'daily',
            tests:[]
        }
    })
}

function delete_phase(p:SchedulePrototype<'website'>['phases'][number]){
    for (let i = 0; i<my.value.phases.length; i++){
        if (my.value.phases[i].phase_id === p.phase_id){
            my.value.phases.splice(i, 1)
            break
        }
    }
}



function rainbow(numOfSteps:number, step:number) {
    // This function generates vibrant, "evenly spaced" colours (i.e. no clustering). This is ideal for creating easily distinguishable vibrant markers in Google Maps and other apps.
    // Adam Cole, 2011-Sept-14
    // HSV to RBG adapted from: http://mjijackson.com/2008/02/rgb-to-hsl-and-rgb-to-hsv-color-model-conversion-algorithms-in-javascript
    let [r, g, b] = [0,0,0]
    let h = step / numOfSteps
    let i = ~~(h * 6)
    let f = h * 6 - i
    let q = 1 - f
    switch(i % 6){
        case 0: r = 1; g = f; b = 0; break
        case 1: r = q; g = 1; b = 0; break
        case 2: r = 0; g = 1; b = f; break
        case 3: r = 0; g = q; b = 1; break
        case 4: r = f; g = 0; b = 1; break
        case 5: r = 1; g = 0; b = q; break
    }
    let c = "#" + ("00" + (~ ~(r * 255)).toString(16)).slice(-2) + ("00" + (~ ~(g * 255)).toString(16)).slice(-2) + ("00" + (~ ~(b * 255)).toString(16)).slice(-2)
    return (c)
}

const test_prototype_color_map = Object.fromEntries(test_prototype_ids.value.map( (tpid,i) => [tpid, rainbow(test_prototype_ids.value.length, i)]))

function generate_preview(){
    console.log(my)
    const intermediate = prepare_schedule_for_upload(
            my.value,
            test_prototypes
        )
    console.log('intermediate', intermediate)
    preview_schedule.value=prepare_schedule_for_participant(
        intermediate, test_prototypes, sample_startdate.value, 'test_participant', 'America/Chicago'
    )
    console.log(preview_schedule.value)
}

function upload_schedule(){
    const body = prepare_schedule_for_upload(
        my.value, 
        test_prototypes
    )
    const retval = fetch('/salsa/server/api/add-schedule?' + new URLSearchParams({
            id: my.value.schedule_id,
            project: project
        }),
        {
            method:'POST',
            body:JSON.stringify(body)
        }
    )
    return retval
}

</script>