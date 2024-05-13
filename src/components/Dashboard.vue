<template>
    <v-window v-model="window_state">
        <v-window-item value="return">
            <p v-if="participants" v-for="p in participants" >
                <a @click="participant_view(p)" style="
                color:blue;  text-decoration: underline;
                ">
                    View participant {{ p.id }}
                </a>
            </p>
        </v-window-item>
        <v-window-item value="view_participant">
            <v-btn @click="return_view">Return to overview of all participants</v-btn>
            <Participant v-if="participant_state" :my="participant_state"/>
        </v-window-item>
    </v-window>
</template>
<script setup lang="ts">
import Participant from '@/components/Participant.vue'
import {type Participant as ParticipantType} from '@/client'
import { participant_list_key } from '@/injectkeys';
import { inject, ref, type Ref } from 'vue';
const participants = inject(participant_list_key)
const window_state = ref("return")
const participant_state: Ref<ParticipantType|null> = ref(null)
function return_view(){
    window_state.value="return"
}
function participant_view(p:ParticipantType){
    participant_state.value=p
    window_state.value="view_participant"
}
</script>