import AudioRecorder from "./AudioRecorder"
import Submit from "./Submit";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from "react";

function App() {
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null)

  const handleAudioRecorded = (audioBlob, audioUrl) => {
    setAudioBlob(audioBlob);
    setAudioUrl(audioUrl)
  };

  return (
    <div className="flex justify-center items-center h-[100vh] bg-green-100">
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<AudioRecorder onAudioRecorded={handleAudioRecorded}/>}/>
        <Route path="/submit" element={<Submit audioBlob={audioBlob} audioUrl={audioUrl} />}/>
      </Routes>
    </BrowserRouter>
    </div>
  )
}

export default App
