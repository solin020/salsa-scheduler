import {defineStore} from 'pinia'
import {ref, type Ref, computed} from 'vue'
import { Filesystem, Directory, Encoding } from '@capacitor/filesystem'
import type {SchedulePrototype} from './types/schedule'
import type { TestPrototype } from './testprototype'
import JSZip from 'jszip'
import write_file from './write_file'
import { twilio_key } from '@/injectkeys'






function get_mime_type(name:string):string{
  if (name.endsWith('.txt') || name.endsWith('.json')){
    return 'text/plain'
  } else if (name.endsWith('.jpg') || name.endsWith('.jpeg')){
    return 'image/jpeg'
  } else if (name.endsWith('.png')){
    return 'image/png'
  } else if (name.endsWith('.wav')){
    return 'audio/wav'
  } else if (name.endsWith('.mp4')){
    return 'video/mp4'
  } else{
    return 'application/octet-stream'
  }
}


function get_embedded_schedule():SchedulePrototype<'device'>{
  return {
    twilio_info:undefined,
    phases: [],
    default_results: undefined,
    default_selection:{
      type:'fixed',
      //@ts-expect-error
      test_prototype_id: window.top.embed_test_prototype_id
    },
    participant_timezone:'America/Chicago',
    schedule_id:'',
    //@ts-expect-error
    participant_id: window.top.embed_coordinator_id,
    prototype_selection: undefined
  }
}


export const salsaStore = defineStore('salsa', () =>{
    //@ts-expect-error
    const salsaid = ref(window.top.embed_coordinator_id)
    const downloads: Ref<string[]> = ref([])
    const downloads_total = ref(0)
    const downloads_remaining = computed(()=>downloads.value.length)
    const current_component = ref('Login')
    const getting_schedule = ref(false)
    const downloading = ref(false)
    const unzipping = ref(false)
    const zips_total = ref(0)
    const zips_remaining = ref(0)
    const downloading_message = computed(()=>
      `Downloaded ${downloads_total.value - downloads_remaining.value}/${downloads_total.value} tests`
    )
    const unzipping_message = computed(()=>
      `Unzipped ${zips_total.value - zips_remaining.value}/${zips_total.value} files`
    )
    const zip_percent = computed(()=>{
      1- (zips_remaining.value / zips_total.value)
    })
    const download_percent = computed(()=>{
      1 - (downloads_remaining.value / downloads_total.value)
    })
    async function initial_salsaid(){
      try{
        const data = await Filesystem.readFile({
            path: 'salsaid.txt',
            directory: Directory.External,
            encoding: Encoding.UTF8
        })
        salsaid.value = data.data.toString()
        current_component.value='HomePage'
      } catch{}

    }
    initial_salsaid()
    const schedule: Ref<SchedulePrototype<'device'>|null> = ref(null)
    async function initial_schedule(){
      schedule.value = JSON.parse(
        (await Filesystem.readFile({
          path:'schedule.json',
          directory:Directory.External,
          encoding: Encoding.UTF8
        })).data.toString()
      )
    }
    initial_schedule()

    async function write_schedule(){
      await Filesystem.writeFile({
        path: 'schedule.json',
        data: JSON.stringify(schedule.value),
        directory: Directory.External,
        encoding: Encoding.UTF8
      })
    }
    async function get_schedule(id:string){
        getting_schedule.value = true
        const my_schedule: SchedulePrototype<'device'> = get_embedded_schedule()
        schedule.value = my_schedule
        getting_schedule.value = false
        await (Filesystem.mkdir({
          path:'testprototypes',
          directory:Directory.External, 
          recursive:true
        }).catch(()=>{}))
        
        await (Filesystem.mkdir({
          path:'awaiting-upload',
          directory:Directory.External, 
          recursive:true
        }).catch(()=>{}))

        await (Filesystem.mkdir({
          path:'finished-upload',
          directory:Directory.External, 
          recursive:true
        }).catch(()=>{}))
        downloading.value = true
        const awaiting_downloads:string[] = []
        if(my_schedule.default_selection){
          awaiting_downloads.push(my_schedule.default_selection.test_prototype_id)
        }
        for (const phase of my_schedule.phases){
          for (const test of phase.spec.tests){
            awaiting_downloads.push(test.prototype_selection.test_prototype_id)
          }
        }
        downloads.value = [...awaiting_downloads]
        downloads_total.value = awaiting_downloads.length
        for (const ts of awaiting_downloads){
          await save_test_prototype(ts)
          downloads.value.splice(downloads.value.indexOf(ts), 1)
        }
        await write_schedule()
        downloading.value = false
        downloads.value = []
      }

    async function set_salsaid(id:string){
        salsaid.value = id
        await get_schedule(id)
        await Filesystem.writeFile({
                path: 'salsaid.txt',
                data: id,
                directory: Directory.External,
                encoding: Encoding.UTF8
              })
    }
    async function save_test_prototype(id:string){
        console.log('got to save test prototype')
        const resp = await fetch(`https://rxinformatics.net/salsa/server/get-test-prototype?id=${id}`)
        console.log('hung on fetch?')
        const zip =  await resp.blob()
        unzipping.value = true
        const zipContent = await JSZip.loadAsync(zip)
        zips_total.value = Object.entries(zipContent.files).length
        zips_remaining.value = zips_total.value
        zipContent.forEach(async (relativePath: string, zipFile: JSZip.JSZipObject) => {
            if(zipFile.dir){
              zips_remaining.value -= 1
              // don't write directories the zip files downloaded are supposed to be flat
            } else{
              const bdata = await zipFile.async('blob')
              await write_file({
                  path: `testprototypes/${id}/${zipFile.name.split('/').pop()}`,
                  f: new File([bdata], zipFile.name, {type:get_mime_type(zipFile.name)})
              })
              zips_remaining.value -= 1
              if (zips_remaining.value<=0){
                unzipping.value = false
                if (downloads_remaining.value<=0){
                  current_component.value='HomePage'
                }
              }
            }
          }
        )
      
      }
    const sequence_no = ref(-1)
    const schedule_id = ref('')
    const test_prototype_id = ref('')
    const todays_test_prototype:Ref<TestPrototype|null> = ref(null)

    return {schedule, salsaid, set_salsaid, downloads,
      sequence_no, schedule_id, test_prototype_id,
      write_schedule, todays_test_prototype, current_component,
      downloads_total, downloads_remaining, download_percent,
      zips_remaining, zips_total, zip_percent, downloading_message,
      getting_schedule, downloading, unzipping, unzipping_message
    }
})