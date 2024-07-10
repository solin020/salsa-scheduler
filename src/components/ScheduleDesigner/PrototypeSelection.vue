<template>
    <v-card>
        <v-card-title>
            <span v-if="!toggleable">Test prototype</span>
            <!--@vue-ignore-->
            <v-btn v-if="toggleable" @click="props.my.prototype_selection = {type:'per-patient', group:'', replace_after_sampling:false}">
                Specify default test for {{ name }}?
            </v-btn>
            <!--@vue-ignore-->
            <v-btn  v-if="toggleable" @click="props.my.prototype_selection=undefined">
                Remove default test for {{ name }}?
            </v-btn>
        </v-card-title>
        <v-card-text v-if="props.my.prototype_selection">
            <v-select :items="[...(props.level!=='base'?[{
                title:'Inherit',
                value:'inherit'
            }]:[]),{
                title:'Specific test prototype',
                value:'fixed'
            },{
                title:'Random prototype per patient',
                value:'per-patient'
            },{
                title:'Random prototype shared across all patients',
                value:'same-across-patients'
            }]" v-model="props.my.prototype_selection.type" :rules="[validate]"/>
            <template v-if="props.my.prototype_selection.type==='fixed'">
                <v-select :items="test_prototype_ids" v-model="props.my.prototype_selection.test_prototype_id" label="Test prototype id"/>
            </template>
            <template v-if="props.my.prototype_selection.type === 'per-patient' || props.my.prototype_selection.type === 'same-across-patients'">
                <v-select :items="groups" v-model="props.my.prototype_selection.group" label="Group to randomly draw from"/>
                <v-checkbox v-model="props.my.prototype_selection.replace_after_sampling" label="Sample with replacement?" :disabled="props.level==='entry'"/>
            </template>
        </v-card-text>
    </v-card>
</template>
<script setup lang='ts' generic="Level extends ('entry'|'phase'|'base')">
import type {TestPrototypeChoice, SchedulePrototype} from '../../types/schedule'
import {inject, computed, ref, type Ref} from 'vue'
import { test_prototypes_key, groups_key } from '@/injectkeys';



interface Props{
    my: (Level extends 'base'? SchedulePrototype<'website'> : 
        Level extends 'phase' ? SchedulePrototype<'website'>['phases'][number] :
        SchedulePrototype<'website'>['phases'][number]['spec']['tests'][number]
    )    
    parent_phase: Level extends 'entry' ? SchedulePrototype<'website'>['phases'][number] : undefined
    parent_schedule: Level extends ('phase'|'entry') ? SchedulePrototype<'website'> : undefined
    level : Level
}
const props = defineProps<Props>()
const toggleable = (props.level!=='entry') ? true : false

const test_prototypes = inject(test_prototypes_key)!
const groups = inject(groups_key)!
const test_prototype_ids = computed(()=>test_prototypes.value.map(tp=>tp.id))




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
            return !!(props.parent_schedule?.prototype_selection || props?.parent_phase?.prototype_selection) || 
            'There must be a test prototype defined in the schedule or parent phase for this test to inherit its timing from'
        } else if (props.level === 'phase') {
            return !!(props.parent_schedule?.prototype_selection) || 
            'There must be a test prototype defined in the schedule for this phase to inherit its timing from'
        } 
    }
    return true
}

</script>