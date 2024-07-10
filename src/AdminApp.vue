<template>
    <v-app>
        <v-app-bar>
            <v-app-bar-title>Salsa 2 Adminstrator interface for {{ email }}</v-app-bar-title>
        </v-app-bar>
        <v-main>
            <j-tabs :tabnames="['admins', 'coordinators']">
                <template #header_admins> View admins </template>
                <template #content_admins>
                    <j-list :items="admins">
                        <template #preamble>
                            <h2>Admins::</h2>
                        </template>
                        <template #renderer="{item:admin}">
                            <v-card>
                                <v-card-title>{{admin.id}}</v-card-title>
                                <v-card-actions>
                                    <j-btn :click="delete_admin" :arg0="{admin:admin.id}">Revoke admin privileges from {{admin.id}}</j-btn>
                                </v-card-actions>
                            </v-card>
                        </template>
                        <template #postamble>
                            <v-card>
                                <v-card-title>Add a new admin</v-card-title>
                                <v-card-text>
                                    <v-text-field :rules="[id_regex_test]" v-model="new_admin" label="admin email"/>
                                </v-card-text>
                                <v-card-actions>
                                    <j-btn :click="add_admin" :arg0="undefined">Add admin</j-btn>
                                </v-card-actions>
                            </v-card>
                        </template>
                    </j-list>
                </template>
                <template #header_coordinators> View coordinators </template>
                <template #content_coordinators>
                    <j-list :items="coordinators">
                        <template #preamble>
                            Coordinators:
                        </template>
                        <template #renderer="{item:coordinator}">
                            <v-card>
                                <v-card-title>{{ coordinator.id }}</v-card-title>
                                <v-card-text>
                                    <v-text-field :rules="[id_regex_test]" v-model="existing_coordinator_project"/>
                                    <j-btn :click="add_existing_coordinator" :arg0="{id:coordinator.id}">Add {{ coordinator.id }} to new project</j-btn>
                                </v-card-text>
                                <v-card-actions>
                                    <j-btn v-for="project in coordinator.projects" :click="delete_coordinator" :arg0="{id:coordinator.id, project}">
                                        Remove coordinator from project {{ project }}
                                    </j-btn>
                                </v-card-actions>
                            </v-card>
                        </template>
                        <template #postamble>
                            <v-card>
                                <v-card-title>Add a new coordinator</v-card-title>
                                <v-card-text>
                                    <v-text-field :rules="[id_regex_test]" label="New Coordinator email" v-model="new_coordinator_id"/>
                                    <br/>
                                    <v-text-field :rules="[id_regex_test]" label="Project name"  v-model="new_coordinator_project"/>
                                </v-card-text>
                                <v-card-actions>
                                    <j-btn :click="add_coordinator" :arg0="{}">Add coordinator to new project</j-btn>
                                </v-card-actions>
                            </v-card>
                        </template>
                    </j-list>
                </template>
            </j-tabs>
        </v-main>
    </v-app>
</template>
<script lang="ts" setup>
import {DefaultService, type Coordinator, type Annotator, type Participant} from './client'
import {ref, type Ref} from 'vue'
import JBtn from './components/JBtn.vue'
import JTabs from './components/JTabs.vue'
import JList from './components/JList.vue'
import { id_regex_test } from './regexes'

const admins: Ref<{id:string}[]> = ref([])
const coordinators: Ref<Coordinator[]> = ref([])
const projects: Ref<string[]> = ref([])
const new_admin = ref("")
const new_coordinator_id = ref("")
const new_coordinator_project = ref("")
const existing_coordinator_project = ref("")

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
        r => admins.value=r.map(id => ({id}))
    )
}
reload_admins()

function add_admin(arg0:undefined){
    const response = fetch('/salsa/server/api/add-admin?' + 
        new URLSearchParams({id:new_admin.value}),
        {method:'POST'}
    )
    response.then(() => reload_admins())
    return response
}

function delete_admin(arg0:{admin:string}){
    const response = fetch(
        '/salsa/server/api/delete-admin?' + 
        new URLSearchParams({...arg0}),
        {method: 'DELETE'}
    )
    response.then(() => reload_admins())
    return response
}

function reload_coordinators(){
    DefaultService.getCoordinatorsSalsaServerApiGetCoordinatorsGet().then(
        r => coordinators.value=r
    )
}
reload_coordinators()

function add_coordinator(){
    const response = fetch(
        '/salsa/server/api/add-coordinator?' + 
        new URLSearchParams({
            id:new_coordinator_id.value,
            project:new_coordinator_project.value
        }),
        {method:'POST'}
    )
    response.then(
        () => reload_coordinators()
    )
    return response
}

function add_existing_coordinator(arg0:{id:string}){
    let response = fetch('/salsa/server/api/add-coordinator?' + 
        new URLSearchParams({...arg0}),
        {method:'POST'}
    )
    response.then(() => reload_coordinators())
    return response
}

function delete_coordinator(arg0:{id:string, project:string}){
    const response = fetch('/salsa/server/api/delete-coordinator?' + 
        new URLSearchParams({...arg0}), 
        {method:'DELETE'}
    )
    response.then(
        () => reload_coordinators()
    )
    return response
}
</script>
<style>

</style>
