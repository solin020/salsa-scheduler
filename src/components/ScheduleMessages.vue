<template>
  <v-app>
    <v-app-bar>
      <h1>Create testing schedule for {{my_participant.id}}</h1>
    </v-app-bar>
    <v-main>
      <h2>Use prototype {{ prototype_choice }}</h2>
      <v-container>
        <v-radio-group v-model="prototype_choice">
          <v-radio v-for="p in test_prototypes" :key="p" :value="p" :label="p"
                   on-icon="mdi-radiobox-marked"
                   off-icon="mdi-radiobox-blank"></v-radio>
        </v-radio-group>
      </v-container>
      <date-picker  mode="date" v-model.range="range" :columns="4" :rows="3">
          <template #footer>
              <v-sheet style="width:35vw;">
              <p>Select the begin and end date of the testing period, and specify what times of day
                testing notifications should be sent out.
              </p>
              </v-sheet>
          </template>
      </date-picker>
      <v-list lines="one">
        <v-list-item v-for ="(time, n) in times_array" :key="n" :title="`${n+1}${nth(n+1)} Message time`">
          <v-text-field label="Choose message time" type="time" v-model="times_array[n]" />
        </v-list-item>
        <v-btn @click="add_time">Add another message time</v-btn>
        <v-btn @click="remove_time">Remove message time</v-btn>
      </v-list>
      <j-btn :click="scheduleMessages" :arg0="{}">Create schedule</j-btn>
      <j-btn :click="cancelMessages" :arg0="{}">Delete all scheduled messages for this participant</j-btn>
    </v-main>
  </v-app>
</template>
<script setup lang="ts">
import {DatePicker} from 'v-calendar'
import JBtn from './JBtn.vue'
import {ref, type Ref, inject, computed} from 'vue'
import {participant_key, reload_messages_key, test_prototypes_key, project_key} from '@/injectkeys'
import { type ApiMessageSchedule, type Participant as ParticipantType, DefaultService } from '../client'

const emit = defineEmits(['reloadparticipant'])

const my_participant = inject(participant_key)!
const reload_messages = inject(reload_messages_key)!
const test_prototypes = inject(test_prototypes_key)!
const prototype_choice = ref("")
const project = inject(project_key)!

function nth(n: number){return["st","nd","rd"][((n+90)%100-10)%10-1]||"th"}

function add_time(){
  times_array.value.push("20:00")
}
function remove_time(){
  times_array.value.pop()
}


let today = new Date()
today.setHours(0,0,0)
let begin_date = new Date()
let end_date = new Date()
begin_date.setDate(today.getDate()+1)
begin_date.setHours(0,0,0)
end_date.setDate(today.getDate()+14)
end_date.setHours(0,0,0)
const range = ref({
    start: begin_date,
    end: end_date,
});
let times_array = ref(["08:00", "13:00", "18:00"])

function scheduleMessages(){
  const schedule: ApiMessageSchedule = {
    participant: my_participant,
    project: project,
    start_date: range.value.start.toISOString(),
    end_date: range.value.end.toISOString(),
    prototype_id: prototype_choice.value,
    times: times_array.value.map(x =>[
        parseInt(x.split(":")[0]),
        parseInt(x.split(":")[1]),
      ])
  }
  return DefaultService.coordinatorScheduleMessagesSalsaServerApiScheduleMessagesPost(schedule).then(
    r => reload_messages()
  )
}
function cancelMessages(){
  const yes = confirm("Are you sure you want to cancel all calls for this participant?")
  if (yes){
    return DefaultService.coordinatorDeleteMessageSalsaServerApiDeleteMessagePost(my_participant.id).then(
      r => reload_messages()
    )
  } else{
    return new Promise(()=>{})
  }
}
console.log('prototypes', test_prototypes)

</script>