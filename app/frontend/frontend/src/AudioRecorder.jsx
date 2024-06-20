import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const mimeType = "audio/wav";

const AudioRecorder = ({ onAudioRecorded }) => {
    const navigate = useNavigate()

    const handleUpload = (e) => {
        e.preventDefault()
        const fileInput = e.target.querySelector('input[type="file"]')
        const model = e.target.querySelector('select[name="options"]')
        const file = fileInput.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                const audioBlob = new Blob([reader.result], { type: file.type })
                const audioUrl = URL.createObjectURL(audioBlob)
                onAudioRecorded(audioBlob, audioUrl, model)
                navigate("/submit")
            }
            reader.readAsArrayBuffer(file)
        }
        
    }

    return (
        <div className="flex justify-center items-center flex-col">
        <div>
            <form action="" className="flex flex-col justify-center items-center" onSubmit={handleUpload}>
                <h2 className="text-xl">Upload file</h2>
                <input className="m-[1em]" type="file"/>
                <h2 className="text-xl">Select model</h2>
                <select className="m-[1em]" name="options" required>
                    <option value="CNN">CNN (~70% accuracy)</option>
                    <option value="LSTM">LSTM (~55% accuracy)</option>
                </select>
                <button type="submit">Upload</button>
            </form>
        </div>
    </div>
    );
};
export default AudioRecorder;