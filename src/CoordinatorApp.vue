<template>
    <v-app>
        <v-app-bar>
            <v-app-bar-title>Salsa 2 Coordinator Interface for {{ email }}</v-app-bar-title>
        </v-app-bar>
        <v-main>
            <v-select style="display:inline-block; width:30rem;" label="Choose project" :items="projects" v-model="current_project"/>
            <CoordinatorProject :projectname="current_project" v-if="current_project"/>
        </v-main>
    </v-app>
</template>
<script lang="ts" setup>
import {DefaultService} from '@/client'
import CoordinatorProject from '@/components/CoordinatorProject.vue'
import {ref, type Ref} from 'vue'
const projects: Ref<string[]> = ref([])
const current_project = ref("")
const email = ref("")
DefaultService.getYourEmailSalsaServerApiGetYourEmailGet().then(
    r => email.value = r
)
DefaultService.coordinatorGetProjectsSalsaServerApiCoordinatorGetProjectsGet().then(
    p => projects.value = p
)
</script>
