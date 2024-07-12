<template>
    <ion-page>
        <ion-content>
            <ion-text color="warning">
                <p>Unable to download tests due to internet connectivity issues.</p>
                <p>Consider logging into wifi, finding an area with better mobile reception,
                    or making sure that your phone is not in airplane mode.
                </p>
            </ion-text>
            <ion-item>
                <ion-button @click="go_to_login()" size="large">Press to retry downloading tests</ion-button>
            </ion-item>
        </ion-content>
    </ion-page>
</template>
<script setup lang="ts">
import {IonPage, IonContent, IonButton, IonText, IonItem} from '@ionic/vue'
import { salsaStore } from '../store'

const store = salsaStore()

function go_to_login(){
    store.current_component='Login'
}

</script>