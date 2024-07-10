<template>
    <v-select :items="[
        {name:'Pacific Time', abbr:'America/Los_Angeles'},
        {name:'Arizona Time', abbr:'America/Phoenix'},
        {name:'Mountain Time', abbr:'America/Denver'},
        {name:'Central Time', abbr:'America/Chicago'},
        {name:'Eastern Time', abbr:'America/New_York'},
        {name:'Hawaii Time', abbr:'Pacific/Honolulu'},
        {name:'Alaska Time', abbr:'America/Anchorage'},
        {name:'Aleutian Time', abbr:'America/Adak'},
        {name:'Puerto Rico/Virgin Islands Time', abbr:'America/Puerto_Rico'},
        {name:'Guam/Mariana Time', abbr:'Pacific/Guam'},
        {name:'American Samoa Time', abbr:'Pacific/Samoa'},
    ]"
    label="Select timezone"
    item-title="name"
    item-value="abbr"
    v-model="props.tz"/>
</template>
<script setup lang="ts">
import { type Timezone } from '@/types/schedule'
interface Props{
    tz:Timezone
}
const props = defineProps<Props>()



</script>