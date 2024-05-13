<template>
    <VBtn @click="open_dialog"><slot name="open">Open</slot></VBtn>
    <dialog ref="dialogref">
        <template v-if="dialog_open">
            <VBtn @click="close_dialog"><slot name="close">Close</slot></VBtn>
            <slot name="content"></slot>
        </template>
    </dialog>
</template>
<script lang="ts" setup>
import {ref, type Ref} from "vue"
const dialogref: Ref<HTMLDialogElement|null> = ref(null)
const dialog_open = ref(false)
function open_dialog(){
    if (dialogref.value){
        dialog_open.value=true
        dialogref.value.showModal()
    }
}
function close_dialog(){
    if (dialogref.value){
        dialog_open.value=false
        dialogref.value.close()
    }
}
</script>