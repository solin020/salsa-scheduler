import  {type Ema}  from "@/types/models/Ema"
import  {type Audio}  from "@/types/models/Audio"
import  {type Video}  from "@/types/models/Video"
import  {type Image}  from "@/types/models/Image"
import  {type Recording}  from "@/types/models/Recording"
import  {type VideoRecording}  from "@/types/models/VideoRecording"
import  {type PictureCapture}  from "@/types/models/PictureCapture"

export type Stimulus = (Ema|Audio|Video|Image|Recording|VideoRecording|PictureCapture)
export type TestPrototype = {
    id: string
    stimuli: Stimulus[]
}