import { useState, useRef } from "react";

const mimeType = "audio/webm";

const AudioRecorder = () => {
    const [permission, setPermission] = useState(false);
    const [stream, setStream] = useState(null);
    const [recordingStatus, setRecordingStatus] = useState("inactive");
    const mediaRecorder = useRef(null);
    const [audioChunks, setAudioChunks] = useState([]);
    const [audio, setAudio] = useState(null);

    const getMicrophonePermission = async () => {
        if ("MediaRecorder" in window) {
            try {
                const streamData = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                    video: false,
                });
                setPermission(true);
                setStream(streamData);
            } catch (err) {
                alert(err.message);
            }
        } else {
            alert("The MediaRecorder API is not supported in your browser.");
        }
    };

    const startRecording = async () => {
        setRecordingStatus("recording");
        const media = new MediaRecorder(stream, { type: mimeType });
        mediaRecorder.current = media;
        mediaRecorder.current.start();
        let localAudioChunks = [];
        mediaRecorder.current.ondataavailable = (e) => {
            if (typeof e.data === "undefined") return;
            if (e.data.size === 0) return;
            localAudioChunks.push(e.data);
        };
        setAudioChunks(localAudioChunks);
    };

    const stopRecording = () => {
        mediaRecorder.current.stop();
        mediaRecorder.current.onstop = () => {
           const audioBlob = new Blob(audioChunks, { type: mimeType });
           const audioUrl = URL.createObjectURL(audioBlob);
           setAudio(audioUrl);
           setAudioChunks([]);
        };
    };

    return (
        <div>
            <div className="flex justify-center items-center border border-black rounded-full h-[2em] w-[2em] text-3xl">
                {!permission ? (
                    <button onClick={getMicrophonePermission} type="button">
                        Get Microphone
                    </button>
                ): null}
                {permission && recordingStatus == "inactive" ? (
                    <button onClick={startRecording} type="button">
                        <i className="fa-solid fa-microphone"></i>
                    </button>
                ): null}
                {recordingStatus == "recording" ? (
                    <button onClick={stopRecording} type="button">
                        <i className="fa-solid fa-microphone-slash"></i>
                    </button>
                ): null}
            </div>
            {audio ? (
                <div className="audio-container">
                <audio src={audio} controls></audio>
                <a download href={audio}>
                    Download Recording
                </a>
            </div>
            ) : null}
        </div>
    );
};
export default AudioRecorder;