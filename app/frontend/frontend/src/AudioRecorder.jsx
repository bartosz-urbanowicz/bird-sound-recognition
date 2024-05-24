import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const mimeType = "audio/wav";

const AudioRecorder = ({ onAudioRecorded }) => {
    const navigate = useNavigate()
    const [stream, setStream] = useState(null);
    const [recordingStatus, setRecordingStatus] = useState("inactive");
    const mediaRecorder = useRef(null);
    const [audioChunks, setAudioChunks] = useState([]);

    const getMicrophonePermission = async () => {
        if ("MediaRecorder" in window) {
            try {
                const streamData = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                });
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
        const media = new MediaRecorder(stream);
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
           console.log(audioBlob)
           const audioUrl = URL.createObjectURL(audioBlob);
           onAudioRecorded(audioBlob, audioUrl);
           setAudioChunks([]);
           setRecordingStatus("inactive")
           navigate("/submit")
        };
    };

    const handleUpload = (e) => {
        e.preventDefault()
        const fileInput = e.target.querySelector('input[type="file"]');
        const file = fileInput.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                const audioBlob = new Blob([reader.result], { type: file.type })
                const audioUrl = URL.createObjectURL(audioBlob)
                onAudioRecorded(audioBlob, audioUrl)
                navigate("/submit")
            }
            reader.readAsArrayBuffer(file)
        }
        
    }

    return (
        <div className="flex justify-center items-center flex-col">
            {/* <h2 className="text-xl">{recordingStatus == "recording" ? "Recording..." : "Tap to record"}</h2>
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
            </div> */}
            <div>
                <form action="" className="flex flex-col justify-center items-center" onSubmit={handleUpload}>
                    <h2 className="text-xl">Upload file</h2>
                    <input className="m-[1em]" type="file"/>
                    <button type="submit">Upload</button>
                </form>
            </div>
        </div>
    );
};
export default AudioRecorder;