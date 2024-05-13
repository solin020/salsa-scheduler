<template @schedulecalls="addParticipant(s, e, m, a, ev)">
    <JTabs :tabnames="['viewparticipants', 'addparticipant', 'addtestprototype', 'viewtestprototypes']">
        <template #header_viewparticipants> View participant dashboard</template>
        <template #content_viewparticipants> <Dashboard/></template>
        <template #header_addparticipant> Add a new participant</template>
        <template #content_addparticipant> 
            <v-text-field v-model="new_participant_id"
                        label="Participant's study id"/>
            <v-text-field v-model="new_participant_phone_number"
                        label="Participant's phone number"/>
            <j-btn :click="add_participant" :arg0="{}">Add participant</j-btn>
        </template>
        <template #header_addtestprototype> Add a new test prototype </template>
        <template #content_addtestprototype> <AddTestPrototype/> </template>
        <template #header_viewtestprototypes> View test prototypes </template>
        <template #content_viewtestprototypes><ViewTestPrototypes :test_prototypes="test_prototypes"/></template>
    </JTabs>
</template>
<script setup lang="ts">
import Dashboard from '@/components/Dashboard.vue'
import AddTestPrototype from '@/components/TestPrototype/Add/AddTestPrototype.vue'
import ViewTestPrototypes from './TestPrototype/View/ViewTestPrototypes.vue'
import JTabs from '@/components/JTabs.vue'
import JBtn from  '@/components/JBtn.vue'
import {DefaultService, type Participant as ParticipantType} from '../client';
import {ref, type Ref, provide} from 'vue'
import { reload_participants_key, project_key, 
    participant_list_key, test_prototypes_key } from '@/injectkeys';

interface Props{
    projectname: string
}
const props = defineProps<Props>()
const participants: Ref<ParticipantType[]> = ref([]) 
const tab: Ref<string> = ref("viewparticipants")
function reload_participants() {DefaultService.getParticipantSalsaServerApiGetParticipantsGet(props.projectname).then(
    p => participants.value=p
)}
reload_participants()
const test_prototypes: Ref<string[]> = ref([])
function reload_test_prototypes(){
    DefaultService.coordinatorGetTestPrototypesSalsaServerGetTestPrototypesGet(props.projectname).then(
        r => test_prototypes.value=r
    )
}
reload_test_prototypes()
provide(reload_participants_key, reload_participants)
provide(project_key, props.projectname)
provide(participant_list_key, participants)
provide(test_prototypes_key, test_prototypes)

const new_participant_id = ref("")
const new_participant_phone_number = ref("")
function add_participant():Promise<any>{
    return DefaultService.addParticipantSalsaServerApiAddParticipantPost(
        new_participant_id.value,
        props.projectname,
        new_participant_phone_number.value,
    ).then(() => reload_participants())
}

</script>