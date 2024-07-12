<template>
    <ion-page>
        <ion-header>
            <ion-toolbar>
                <ion-button @click="go_home()">
                    <ion-icon :icon="homeOutline" size="large"/>
                </ion-button>
                <ion-button @click="go_uploads()">
                    <ion-icon :icon="cloudUploadOutline" size="large"/>
                </ion-button>
                <ion-button id="open-modal">
                    <ion-icon :icon="keyOutline" size="large"/>
                </ion-button>
            </ion-toolbar>
        </ion-header>
        <ion-content>
            <slot name="content"/>
            <ion-modal ref="modal" trigger="open-modal" >
                <ion-card style="width:80vw;
                        position:fixed;
                        left:0;
                        top:30%;">
                    <ion-card-header>
                        <ion-card-title>
                            Reset salsa?
                        </ion-card-title>
                    </ion-card-header>
                    <ion-card-content class="ion-padding">
                        <ion-text color="warning">
                            This resets the salsa application and your response code.
                            Only continue if instructed to do so by your test coordinator.
                        </ion-text>
                    </ion-card-content>
                    <ion-toolbar>
                        <ion-buttons slot="start">
                            <ion-button @click="cancel()">Cancel</ion-button>
                        </ion-buttons>
                        <ion-buttons slot="end">
                            <ion-button :strong="true" @click="reset()">Reset</ion-button>
                        </ion-buttons>
                    </ion-toolbar>
                </ion-card>
            </ion-modal>
        </ion-content>
        <ion-footer class="j_footer">
            <slot name="footer"/>
        </ion-footer>
    </ion-page>
</template>
<script setup lang="ts">
import {IonPage, IonHeader, IonContent, IonTitle, 
    IonButton, IonIcon, IonFooter, IonToolbar, IonModal, IonButtons,
    IonText, IonCard, IonCardHeader, IonCardContent,
    IonCardTitle} from '@ionic/vue'
import { homeOutline, cloudUploadOutline, keyOutline } from 'ionicons/icons'
import { salsaStore } from '../store'

import {ref} from 'vue'

const store = salsaStore()


const modal = ref()

const cancel = () => modal.value.$el.dismiss(null, 'cancel')

const reset = () => {
    modal.value.$el.dismiss(null, 'cancel')
    store.current_component='Login'
}

function go_home(){
    store.current_component='HomePage'
}
function go_uploads(){
    store.current_component='Uploads'
}

</script>
<style>
.j_footer{
    text-align: center;
    padding-bottom:30px;
}
</style>