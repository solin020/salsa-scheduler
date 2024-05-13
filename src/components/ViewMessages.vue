<template>
    <dialog ref="dialogref">
        <VBtn @click="close_dialog">Close Day Viewer</VBtn>
        <ViewDay :day="day_viewed"></ViewDay>
    </dialog>
    <Calendar :attributes="attributes" @dayclick="view_day">
    </Calendar>
</template>
<script lang="ts" setup>
import {Calendar} from 'v-calendar'
import ViewDay from './ViewDay.vue'
import {computed, inject, ref, type Ref} from 'vue'
import {scheduled_message_list_key, message_response_list_key} from '@/injectkeys'
const scheduled_message_list = inject(scheduled_message_list_key)!
const message_response_list = inject(message_response_list_key)!

const day_viewed: Ref<Date> = ref(new Date())

const dialogref: Ref<HTMLDialogElement|null> = ref(null)


const attributes = computed<any[]>(() =>{
    const scl: any[] =  scheduled_message_list.value.map(
        c => ({
            key:c.schedule_id,
            dot:{
                color:'red'
            },
            dates:new Date(c.time),
            customData:{...c, call_type:'future'},
            popover:true,
        })
    ).reverse()
    const pcl: any[]  = message_response_list.value.map(
        c =>  ({
            key:c.schedule_id,
            dot:{
                color:'blue'
            },
            dates:new Date(c.timestamp),
            customData:{...c, id:c.schedule_id, call_type:'past'},
            popover:true,
        })
    ).reverse()
    return pcl.concat(scl)
    }
)
function view_day(e: any){
    day_viewed.value = e.date
    if (dialogref.value){
        dialogref.value.showModal()
    }
}
function close_dialog(){
    if (dialogref.value){
        dialogref.value.close()
    }
}

</script>