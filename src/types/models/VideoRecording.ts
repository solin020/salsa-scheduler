export type VideoRecording = {
    type: 'video-recording';
    id: string;
    autoadvance: boolean;
    duration: (number | null);
};