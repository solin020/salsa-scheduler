<template>
    <v-app>
        <v-app-bar>
            <v-app-bar-title>Salsa 2 Adminstrator interface for {{ email }}</v-app-bar-title>
        </v-app-bar>
        <v-main>
            <v-tabs v-model="tab">
                <v-tab value="rw-admins">View admins</v-tab>
                <v-tab value="rw-coordinators">View coordinator project assignments</v-tab>
            </v-tabs>
            <v-window v-model="tab">
                <v-window-item value="rw-admins" :transition="false" :reverse-transition="false">
                    <p v-for="admin in admins">{{ admin }}<j-btn :click="delete_admin" :arg0="{admin}">Delete admin</j-btn></p>
                    <j-btn :click="add_admin" :arg0="{}">Add admin</j-btn>
                    <v-text-field v-model="new_admin" label="admin email"/>
                </v-window-item>
                <v-window-item value="rw-coordinators" :transition="false" :reverse-transition="false">
                    <v-card>
                        <ul>
                            <li v-for="coordinator in coordinators">
                                <h2>{{ coordinator.id }}</h2>
                                <ul>
                                    <li v-for="project in coordinator.projects">
                                        {{ project }}<j-btn :click="delete_coordinator" :arg0="{id:coordinator.id, project}">Remove coordinator from this project</j-btn>
                                    </li>
                                </ul>
                            </li>
                            <li>
                                <j-btn :click="add_coordinator" :arg0="{}">Assign coordinator to project</j-btn>
                                <v-text-field label="Coordinator email" v-model="new_coordinator_id"/>
                                <v-text-field label="Project name"  v-model="new_coordinator_project"/>
                            </li>
                        </ul>
                    </v-card>
                </v-window-item>
            </v-window>
        </v-main>
    </v-app>
</template>
<script lang="ts" setup>
import {DefaultService, type Coordinator, type Annotator, type Participant} from './client'
import {ref, type Ref} from 'vue'
import JBtn from './components/JBtn.vue'
import JTabs from './components/JTabs.vue'
const admins: Ref<string[]> = ref([])
const coordinators: Ref<Coordinator[]> = ref([])
const projects: Ref<string[]> = ref([])
const tab = ref("rw-admins")
const new_admin = ref("")
const new_coordinator_id = ref("")
const new_coordinator_project = ref("")
const email = ref("")
DefaultService.getYourEmailSalsaServerApiGetYourEmailGet().then(
    r => email.value = r
)

function reload_projects(){
    DefaultService.adminGetProjectsSalsaServerApiAdminGetProjectsGet().then(
        r => projects.value=r
    )
}
reload_projects()

function reload_admins(){
    DefaultService.getAdminsSalsaServerApiGetAdminsGet().then(
        r => admins.value=r
    )
}
reload_admins()

function add_admin(){
    return DefaultService.addAdminSalsaServerApiAddAdminPost(new_admin.value).then(
        () => reload_admins()
    )
}

function delete_admin(arg0:{admin:string}){
    return DefaultService.deleteAdminSalsaServerApiDeleteAdminPost(arg0.admin).then(
        () => reload_admins()
    )
}

function reload_coordinators(){
    DefaultService.getCoordinatorsSalsaServerApiGetCoordinatorsGet().then(
        r => coordinators.value=r
    )
}
reload_coordinators()

function add_coordinator(){
    return DefaultService.addCoordinatorSalsaServerApiAddCoordinatorPost(new_coordinator_id.value, new_coordinator_project.value).then(
        () => reload_coordinators()
    )
}

function delete_coordinator(arg0:{id:string, project:string}){
    return DefaultService.deleteCoordinatorSalsaServerApiDeleteCoordinatorPost(arg0.id, arg0.project).then(
        () => reload_coordinators()
    )
}
</script>
