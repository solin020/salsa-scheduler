export namespace DialogTree{
    type Dialog = Destination[]
    type Destination = (
        Branch|
        State|
        Goodbye|
        LlmState|
        LlmAsk
    )
    type Response = {tag:'response'}
    type Backprompt = {tag:'backprompt'}
    type Context = {tag:'context', key:string}
    type Code = {tag:'code', python:string}
    type Text = {tag:'text', text:string}
    
    type Goodbye = {
        tag:'goodbye',
        statement:Stateable
        destinationname:string,
        nextdestinationname:string,
        historyname:string,
    }
    type State = {
        tag:'state', 
        destinationname:string,
        nextdestinationname:string,
        statement:Stateable,
        historyname:string,
    
    }
    
    export type Stateable = (Context|Text|Code|ChatMl)[]
    export type Promptable = (Context|Text|Code|Backprompt|Response|ChatMl)[]
    
    type ChatMl = {
        tag:'ChatMl',
        role:('user'|'assistant'|'system'),
        content:(Context|Text|Code)[]
    }
    
    
    type Jump = {
        tag:'jump',
        subtag:'plainjump',
        answer:string,
        nextdestination:string
    } | {
        tag:'jump',
        subtag:'codejump',
        python:Code
    }
    
    type Branch = {
        tag:'branch',
        destinationname:string,
        nextdestinationname:string,
        historyname:string,
        userquestion:Stateable,
        onerror:Promptable,
        parseanswer:Promptable,
        jumps:Jump[]
    }
    type LlmState = {
        tag:'llm-state',
        destinationname:string,
        nextdestinationname:string,
        historyname:string,
        statement:Promptable
    }
    type LlmAsk = {
        tag:'llm-ask'
        destinationname:string,
        nextdestinationname:string,
        historyname:string,
        userquestion: Stateable,
        parseanswer:Promptable
    }
}

