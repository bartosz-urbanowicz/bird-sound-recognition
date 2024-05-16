import { useState, useRef, useEffect } from "react";

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

    useEffect(() => {
        getMicrophonePermission()
    }, [])

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
           setRecordingStatus("inactive")
        };
    };

    return (
        <div className="flex justify-center items-center flex-col">
            <h2 className="text-xl">Tap to record</h2>
            <div className={`flex justify-center items-center border border-black rounded-full h-[2em] w-[2em] text-3xl m-[1em] ${
                recordingStatus == "recording" ? "blob" : null
            }`}>
                {recordingStatus == "inactive" ? (
                    <button onClick={startRecording} type="button">
                        <i className="fa-solid fa-microphone"></i>
                    </button>
                ): null}
                {recordingStatus == "recording" ? (
                    <button onClick={stopRecording} type="button">
                        <i className="fa-solid fa-stop"></i>
                    </button>
                ): null}
            </div>
            <div>
                <form action="">
                    <input type="file"/>
                    <button type="submit">Upload</button>
                </form>
            </div>
            {audio ? (
                <div className="audio-container flex items-center justify-center">
                    <audio src={audio} controls></audio>
                    <a download href={audio}>
                    <i class="fa-solid fa-download m-[0.5em]"></i>
                    </a>
                </div>
            ) : null}
        </div>
    );
};
export default AudioRecorder;