<template>
    <v-card>
        <v-card-title>
            <span v-if="!toggleable">Test time of day </span>
            <!--@vue-ignore-->
            <v-btn v-if="toggleable" @click="props.my.timing = {type:'fixed',hour:9,minute:0}">
                Specify default  timing for  {{ name }}?
            </v-btn>
            <!--@vue-ignore-->
            <v-btn  v-if="toggleable" @click="props.my.timing=undefined">
                Remove default timing for {{ name }}?
            </v-btn>
        </v-card-title>
        <v-card-text v-if="props.my.timing">
            <v-select :items="[...(props.level!=='base'?[{
                title:'Inherit',
                value:'inherit'
            }]:[]),{
                title:'Specific time',
                value:'fixed'
            },{
                title:'Random time per patient',
                value:'per-patient'
            },{
                title:'Random time across schedule',
                value:'same-across-patients'
            }]" v-model="props.my.timing.type" :rules="[validate]"/>
            <template v-if="props.my.timing.type==='fixed'">
                <label>Scheduled time</label>
                <!--@vue-ignore-->
                <input type="time" @input="(e) => [props.my.timing.hour, props.my.timing.minute] = parse_time(e)"/>
            </template>
            <template v-if="['per-patient','same-across-patients'].includes(props.my.timing.type)">
                <label>Earliest random time</label>
                <!--@vue-ignore-->
                <input type="time" @input="(e) => [props.my.timing.min_hour, props.my.timing.min_minute] = parse_time(e)"/>
                <label>Latest random time</label>
                <!--@vue-ignore-->
                <input type="time" @input="(e) => [props.my.timing.max_hour, props.my.timing.max_minute] = parse_time(e)"/>
            </template>
        </v-card-text>
    </v-card>
</template>
<script setup lang='ts' generic="Level extends ('entry'|'phase'|'base')">
import type {Timing, SchedulePrototype} from '../../types/schedule'
import {ref, type Ref} from 'vue'

interface Props{
    my: (Level extends 'base'? SchedulePrototype<'website'> : 
        Level extends 'phase' ? SchedulePrototype<'website'>['phases'][number]['spec'] :
        SchedulePrototype<'website'>['phases'][number]['spec']['tests'][number]
    )
    parent_phase: Level extends 'entry' ? SchedulePrototype<'website'>['phases'][number] : undefined
    parent_schedule: Level extends ('phase'|'entry') ? SchedulePrototype<'website'> : undefined
    level : Level
}
const props = defineProps<Props>()
const toggleable = (props.level!=='entry') ? true : false



const name = ((level)=>{
    switch (level){
        case 'entry': return 'Test'
        case 'phase': return 'Phase'
        case 'base': return 'Schedule'
    }
})(props.level)

function validate(type:string){
    if (type === 'inherit'){
        if (props.level === 'entry'){
            return !!(props.parent_schedule?.timing || props.parent_phase?.spec?.timing) || 
            'There must be a timing defined in the schedule or parent phase for this test to inherit its timing from'
        } else if (props.level === 'phase') {
            return !!(props.parent_schedule?.timing) || 
            'There must be a timing defined in the schedule for this phase to inherit its timing from'
        } 
    }
    return true
}

function parse_time(e:Event){
    const [hour, minute] = ((e.target! as HTMLInputElement).value.split(':')).map(s => parseInt(s))
    return [hour, minute]
}

</script>