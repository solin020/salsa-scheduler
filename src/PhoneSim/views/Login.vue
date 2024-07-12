<template>
    <ion-page>
        <ion-content>
            <ion-card style="width:80vw;
                        position:fixed;
                        left:0%;
                        top:30%;">
                <ion-card-header>
                    <ion-card-title>Login</ion-card-title>
                </ion-card-header>
                <ion-card-content>
                    <ion-text color="tertiary">
                        Enter the response code that your study coordinator gave to you.
                    </ion-text>
                    <ion-input placeholder="enter code here" v-model="enterid"/>
                    <ion-button v-if="enterid && !loading_begin" @click="set_salsaid">Submit</ion-button>
                    <ion-list v-if="loading_begin">
                        <ion-item v-if="store.getting_schedule">
                            <ion-text>Downloading schedule</ion-text>
                        </ion-item>
                        <ion-item v-if="store.downloading">
                            <ion-text>{{store.downloading_message}}</ion-text>
                        </ion-item>
                        <ion-item v-if="store.unzipping">
                            <ion-text>{{store.unzipping_message}}</ion-text>
                        </ion-item>
                    </ion-list>
                </ion-card-content>
            </ion-card>
        </ion-content>
    </ion-page>
</template>
<script lang="ts" setup>
import {IonPage, IonButton, IonContent, IonCardHeader, IonCardTitle, IonText, IonInput,
     IonList, IonItem, IonCardContent, IonCard
} from '@ionic/vue'
import {ref} from 'vue'
import { salsaStore } from '../store'


const store = salsaStore()

//@ts-expect-error
const enterid = ref(window.top.embed_coordinator_id)
const loading_begin = ref(false)

async function set_salsaid(){
    loading_begin.value = true
    try{
        await store.set_salsaid(enterid.value)
    } catch {
        store.current_component='Error'
    }
}

</script>