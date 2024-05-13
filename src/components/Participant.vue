<template>
    <v-card>
        <Popup>
            <template #content>
                <ScheduleMessages></ScheduleMessages>
            </template>
            <template #open>
                <span>Make an SMS schedule for {{ my.id }}</span>
            </template>
        </Popup>
        <Popup>
            <template #content>
                <ViewMessages></ViewMessages>
            </template>
            <template #open>
                <span>View past and scheduled SMS from {{ my.id }}</span>
            </template>
        </Popup>
        <j-btn :click="delete_participant" :arg0="{}">Delete participant {{ my.id }}</j-btn>
    </v-card>
</template>
<script lang="ts" setup>
import {ref, type Ref, provide, inject} from "vue"
import Popup from "./Popup.vue"
import JBtn from "./JBtn.vue"
import ScheduleMessages from "./ScheduleMessages.vue"
import ViewMessages from "./ViewMessages.vue"
import {type Participant as ParticipantType, DefaultService, 
        type MessageSchedule, type MessageResponse} from '../client'
import {scheduled_message_list_key, message_response_list_key, reload_messages_key,
        participant_key,
reload_participants_key} from '@/injectkeys'

interface Props {
    my: ParticipantType
}
const props = defineProps<Props>()

const scheduled_message_list:Ref<MessageSchedule[]> = ref([]);
const message_response_list:Ref<MessageResponse[]> = ref([])

function reload_messages(){
    DefaultService.coordinatorGetMessagesSalsaServerApiGetMessagesAndResponsesPost(props.my.id).then(
        (r) => {
            scheduled_message_list.value = r[0]
            message_response_list.value = r[1]
        }
    )
}
reload_messages()
provide(participant_key, props.my)
provide(scheduled_message_list_key, scheduled_message_list)
provide(message_response_list_key, message_response_list)
provide(reload_messages_key, reload_messages)
const reload_participants = inject(reload_participants_key)!
function delete_participant(){
    return DefaultService.deleteParticipantSalsaServerApiDeleteParticipantPost(props.my.id).then(
        r => reload_participants()
    )
}



</script>