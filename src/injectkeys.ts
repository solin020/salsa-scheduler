import {type InjectionKey, type Ref} from 'vue'
import {type Participant as ParticipantType, 
        type MessageSchedule,
        type MessageResponse as MessageResponseType,
} from '@/client'

export const participant_list_key = Symbol() as InjectionKey<Ref<ParticipantType[]>>
export const participant_key = Symbol() as InjectionKey<ParticipantType>
export const message_response_list_key = Symbol() as InjectionKey<Ref<MessageResponseType[]>>
export const message_response_key = Symbol() as InjectionKey<MessageResponseType>
export const scheduled_message_list_key = Symbol() as InjectionKey<Ref<MessageSchedule[]>>
export const scheduled_message_key = Symbol() as InjectionKey<MessageSchedule>
export const reload_participants_key = Symbol() as InjectionKey<Function>
export const reload_messages_key = Symbol() as InjectionKey<Function>
export const project_key = Symbol() as InjectionKey<string>
export const test_prototypes_key = Symbol() as InjectionKey<Ref<string[]>>
