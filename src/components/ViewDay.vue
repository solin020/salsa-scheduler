<template>
        <h1>Info for {{my_participant.id}} on {{day.toLocaleString()}}</h1>
	    <ul>
            <li v-for="sm in today_sml">
                <ScheduledMessage :my_scheduled_message="sm"></ScheduledMessage>
            </li>
            <li v-for="mr in message_response_list">
                <Popup>
                    <template #open>
                        <span>View message response</span>
                    </template>
                    <template #content>
                        <MessageResponse :my_message_response="mr"></MessageResponse>
                    </template>
                </Popup>
            </li>
	    </ul>
</template>
<script lang="ts" setup>
import {inject, computed} from 'vue'
import MessageResponse from '@/components/MessageResponse.vue'
import ScheduledMessage from '@/components/ScheduledMessage.vue'
import Popup from '@/components/Popup.vue'
import {scheduled_message_list_key,message_response_list_key,participant_key} from '@/injectkeys'
import {type MessageResponse as MessageResponseType, type MessageSchedule as ScheduledMessageType} from '@/client'

const scheduled_message_list = inject(scheduled_message_list_key)!
const message_response_list = inject(message_response_list_key)!
const my_participant = inject(participant_key)!

interface Props{
    day: Date
}
const props = defineProps<Props>()

const today_sml = computed<ScheduledMessageType[]>(() => {
    return scheduled_message_list.value.filter(
        sm => (props.day.toLocaleDateString() === new Date(sm.time).toLocaleDateString())
    )
})

const today_mrl = computed<MessageResponseType[]>(() => {
    return message_response_list.value.filter(
        mr => (props.day.toLocaleDateString() === new Date(mr.timestamp).toLocaleDateString())
    )
})


</script>