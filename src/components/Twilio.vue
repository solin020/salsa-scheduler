<template>
    <v-card>
        <v-card-title>Twilio info</v-card-title>
        <v-container>
            <v-row no-gutters>
                <v-col :cols="12" :lg="2">
                    <v-text-field label="Twilio information nickname" v-model="new_tw_nickname"/>
                </v-col>
                <v-col :cols="12" :lg="2">
                    <v-text-field label="Account sid" v-model="new_tw_account_sid"/>
                </v-col>
                <v-col :cols="12" :lg="2">
                    <v-text-field label="Auth token" v-model="new_tw_auth_token"/>
                </v-col>
                <v-col :cols="12" :lg="2">
                    <v-text-field label="Phone number" v-model="new_tw_phone_number"/>
                </v-col>
                <v-col :cols="12" :lg="2">
                    <j-btn :click="upload_new" :arg0="undefined">Upload new twilio information</j-btn>
                </v-col>
            </v-row>
            <v-row v-for = "tw, idx in twilio_infos" no-gutters>
                <v-col :cols="12" :lg="2">
                    <template v-if="active_idx===idx">
                        <v-text-field label="Twilio information nickname" v-model="tw.nickname"/>
                    </template>
                    <template v-else>
                        {{tw.nickname}}
                    </template>
                </v-col>
                <v-col :cols="12" :lg="2">
                    <template v-if="active_idx===idx">
                        <v-text-field label="Account sid" v-model="tw.account_sid"/>
                    </template>
                    <template v-else>
                        {{tw.account_sid}}
                    </template>
                </v-col>
                <v-col :cols="12" :lg="2">
                    <template v-if="active_idx===idx">
                        <v-text-field label="Auth token" v-model="tw.auth_token"/>
                    </template>
                    <template v-else>
                        {{tw.auth_token}}
                    </template>
                </v-col>
                <v-col :cols="12" :lg="2">
                    <template v-if="active_idx===idx">
                        <v-text-field label="Phone number" v-model="tw.phone_number"/>
                    </template>
                    <template v-else>
                        {{tw.phone_number}}
                    </template>
                </v-col>
                <v-col :cols="12" :lg="2" v-if="active_idx===idx">
                    <j-btn :click="upload_existing" :arg0="tw">Update twilio information</j-btn>
                </v-col>
                <v-col :cols="12" :lg="2">
                    <template v-if="active_idx===idx">
                        <v-btn @click="active_idx=undefined">Undo</v-btn>
                    </template>
                    <template v-else>
                        <v-btn @click="active_idx=idx">Edit?</v-btn>
                    </template>
                </v-col>
            </v-row>
        </v-container>
    </v-card>
</template>
<script setup lang="ts">
import {inject, ref, type Ref} from 'vue'
import { twilio_key, project_key, reload_twilio_key } from '@/injectkeys'
import type { TwilioInfo } from '@/types'
import JBtn from './JBtn.vue'

const twilio_infos = inject(twilio_key)!
const project = inject(project_key)!
const reload_twilio = inject(reload_twilio_key)!
const new_tw_nickname = ref("")
const new_tw_account_sid = ref("")
const new_tw_auth_token = ref("")
const new_tw_phone_number = ref("")
const active_idx: Ref<number|undefined> = ref()

function upload_new(){
    return upload_to_twilio(new_tw_nickname.value, new_tw_account_sid.value, new_tw_auth_token.value, new_tw_phone_number.value)
}
function upload_existing(tw: TwilioInfo){
    return upload_to_twilio(tw.nickname, tw.account_sid, tw.auth_token, tw.phone_number)

}

function upload_to_twilio(nickname:string, account_sid:string, auth_token:string, phone_number:string){
    const retval = fetch('/salsa/server/api/add-twilio-info?' + 
        new URLSearchParams({project, nickname, account_sid, auth_token, phone_number}),
        {method:'POST'}
    )
    retval.then((r) => r.status === 200? reload_twilio() : undefined)
    return retval
}


</script>