<template>
    <v-list>
        <v-list-item v-for="[original_file, file_url] in file_urls">
            <template v-if="original_file.endsWith('.wav') || original_file.endsWith('.adts')">
                Listen to {{ original_file.split('=').pop() }}:
                <br/>
                <span>&#9;</span><audio  :src="file_url" controls style="display: inline-block;"/>
            </template>

            <Popup v-else class="j-generic-popup">
                <template #content>
                    <iframe  :src="file_url"/>
                </template>
                <template #open>
                    View {{ original_file.split('=').pop() }}
                </template>
            </Popup>
        </v-list-item>
        <v-list-item v-if="props.transcript">
            <details>
                <summary>View transcript</summary>
                <template v-for="word, i in props.transcript.word_segments">
                    <span :style="calculate_span_style(word.score)">
                        <v-tooltip activator="parent" location="top" origin="overlap">
                            Confidence: {{word.score}}
                        </v-tooltip>
                        {{word.word}} &nbsp;
                    </span>
                    <br v-if="i%15===0"/>
                </template>
            </details>
        </v-list-item>
    </v-list>
</template>
<script setup lang=ts>
import {computed, ref, type Ref} from 'vue'
import type { StimulusResult } from '@/types/schedule'
import { get_src } from './dashboard_logic';
import type { Transcript } from '@/types'
import Popup from '../Popup.vue'

interface Props{
    my: StimulusResult<'parsed'>
    files: string[]
    transcript?: Transcript
}
const props = defineProps<Props>()

const file_urls = computed(()=>
    props.files.map(fl => [fl, get_src(props.my.schedule_id!, fl)])
)

function calculate_span_style(score:number) {
    return {
        
        'background-color': `oklab(from red 1 ${0.4 - (0.8*score)} 0.4)`
    }
}



</script>