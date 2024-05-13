<template>
    <VCard>
        <VCardTitle>Response from {{ my_participant.id }} at {{ new Date(my_message_response.timestamp).toLocaleString() }}</VCardTitle>
        <VCardSubtitle>
            <p>Phone number: {{ my_participant.phone_number }}</p>
            <p>Schedule id: {{ my_message_response.schedule_id }}</p>
            <p>Metadata: {{ my_message_response.miscellaneous }} </p>
        </VCardSubtitle>
        <VCardText>
            <VList>
                <VListItem v-for="f in file_list" :key="f" :title="f">
                    <audio v-if="f.endsWith('.wav')"
                    :src="f"
                    controls>
                    </audio>
                    <iframe v-else
                    :src="f">
                    </iframe>
                </VListItem>
            </VList>
        </VCardText>
    </VCard>
</template>
<script lang="ts" setup>
import {inject, ref, type Ref} from 'vue'
import {type MessageResponse as MessageResponseType, DefaultService} from '@/client'
import { participant_key } from '@/injectkeys';
interface Props{
    my_message_response: MessageResponseType,
}
const props = defineProps<Props>()
const my_participant = inject(participant_key)!

const file_list: Ref<string[]> = ref([])
function list_files(){
    DefaultService.getMessageResponseFilesSalsaServerGetMessageResponseFilesGet(
        props.my_message_response.schedule_id
    ).then(
        r => file_list.value = r.map(
            filepath => ('/salsa/server/get-message-response-file?' + (new URLSearchParams({
                schedule_id:props.my_message_response.schedule_id,
                filepath: filepath
            })).toString()))
    )
}
list_files()
</script>