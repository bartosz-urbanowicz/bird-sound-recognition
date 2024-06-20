import AudioRecorder from "./AudioRecorder"
import Submit from "./Submit";
import ObservationsNearby from "./ObservationsNearby"
import MyObservations from "./MyObservations"
import Navbar from "./Navbar";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from "react";

function App() {
  const [audioBlob, setAudioBlob] = useState(null)
  const [audioUrl, setAudioUrl] = useState(null)
  const [model, setModel] = useState("")

  const handleAudioRecorded = (audioBlob, audioUrl, model) => {
    setAudioBlob(audioBlob)
    setAudioUrl(audioUrl)
    setModel(model)
  }

  return (
    <BrowserRouter>
      <Navbar loggedIn={true}/>
      <div className="flex justify-center items-center h-[calc(100vh-4rem)] bg-green-100">
        <Routes>
          <Route path="/" element={<AudioRecorder onAudioRecorded={handleAudioRecorded}/>}/>
          <Route path="/submit" element={<Submit audioBlob={audioBlob} audioUrl={audioUrl} model={model}/>}/>
          <Route path="/my-observations" element={<MyObservations/>}/>
          <Route path="/nearby-observations" element={<ObservationsNearby/>}/>
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
