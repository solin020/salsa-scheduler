<template>
    <layout>
        <template v-slot:content>
            <ion-card>
                <ion-card-header>
                    <ion-card-title>Uploads</ion-card-title>
                </ion-card-header>
                <ion-card-content>
                    <ion-list>
                        <ion-item v-if="uploading_flag">
                            <ion-progress-bar :value="progress" ></ion-progress-bar>
                            <ion-text color="secondary">{{ upload_message }} uploads complete</ion-text>
                        </ion-item>
                        <ion-item v-else>
                            <ion-text>{{ initial_message}}</ion-text>
                        </ion-item>
                        <ion-item v-for="u in uploads">
                            <ion-text>{{ u.name }} {{ u.date.toLocaleDateString() }}</ion-text>
                        </ion-item>
                    </ion-list>
                </ion-card-content>
            </ion-card>
        </template>
        <template v-slot:footer>
            <ion-button @click="upload()" size="large" v-if="!uploading_flag">Press to upload test results</ion-button>
        </template>
    </layout>
</template>
<script setup lang="ts">
import {IonButton, IonList, IonText,IonCard, IonCardContent,IonCardHeader, 
    IonCardTitle, IonProgressBar, IonItem} from '@ionic/vue'
import Layout from './Layout.vue'
import {Filesystem, Directory, Encoding} from '@capacitor/filesystem'
import {ref, type Ref, computed} from 'vue'
import { salsaStore } from '../store'

console.log('Uploads setup called')

const uploading_flag = ref(false)
const store = salsaStore()

interface UploadType{
    name:string
    date:Date
}

const uploads: Ref<UploadType[]> = ref([])
const uploads_total = ref(0)
const initial_message = computed(()=>`${uploads_total.value} files waiting to be uploaded` )
const uploads_remaining = computed(()=>uploads.value.length)
const progress = computed(()=>(uploads_total.value-uploads_remaining.value)/uploads_total.value)
const upload_message = computed(()=>`${(uploads_total.value-uploads_remaining.value)}/${uploads_total.value}`)

async function update_uploads(){
    const pushval: UploadType[] = []
    for (const {name} of (await Filesystem.readdir({
        directory:Directory.External, path:'awaiting-upload'
    })).files){
        const [ , , , , timestamp, true_name] = name.split('|')
        pushval.push({
            name:true_name.split('.')[0],
            date: new Date(timestamp)
        })
    }
    uploads.value = pushval
}

update_uploads().then( () =>
    uploads_total.value = uploads.value.length
)


async function upload(){
    uploading_flag.value = true
    await update_uploads()
    uploads_total.value = uploads.value.length
    for (const {name} of (await Filesystem.readdir({
        directory:Directory.External, path:'awaiting-upload'
    })).files){
        const [schedule_id, response_code, test_prototype_id, sequence_no, timestamp, true_name] = name.split('|')
        const armor_string = (await Filesystem.readFile({
                directory:Directory.External,
                path: `awaiting-upload/${name}`,
                encoding: Encoding.UTF8
            })).data as string
        const armor_blob = new Blob([armor_string], {type:'text/plain'})
        const fd = new FormData()
        fd.append(`${true_name}`, armor_blob, `${true_name}`)
        const response = await fetch('https://rxinformatics.net/salsa/server/api/upload-response-file?' + 
            new URLSearchParams({
                subject_id:response_code,
                schedule_id, 
                test_prototype_id,
                timestamp,
                sequence_no
            }), {
                body:fd,
                method:'POST'
            }
        )
        if (response.status===200){
            Filesystem.rename({
                from: `awaiting-upload/${name}`,
                to: `finished-upload/${name}`,
                directory: Directory.External,
                toDirectory: Directory.External
            })
        }
        await update_uploads()
    }
    store.current_component = 'HomePage'
}
</script>