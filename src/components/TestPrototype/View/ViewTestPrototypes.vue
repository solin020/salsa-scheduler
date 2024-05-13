<template>
    <v-select v-model="test_id" :items="test_prototypes" label="Select Test Prototype"/>
    <template v-for="tid in props.test_prototypes">
        <ViewTestPrototype  :id="test_id" v-if="test_id===tid"/>
    </template>
</template>
<script setup lang="ts">
import {ref, type Ref, inject} from 'vue'
import { project_key } from '@/injectkeys'
import ViewTestPrototype from './ViewTestPrototype.vue'
const project = inject(project_key)!
interface Props{
    test_prototypes: string[]
}
const props = defineProps<Props>()
const test_id = ref('')

</script>