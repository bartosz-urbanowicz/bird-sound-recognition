import AudioRecorder from "./AudioRecorder"
import Submit from "./Submit";
import ObservationsNearby from "./ObservationsNearby"
import MyObservations from "./MyObservations"
import Navbar from "./Navbar";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from "react";
import AddObservation from "./AddObservation";

function App() {
  const [audioBlob, setAudioBlob] = useState(null)
  const [audioUrl, setAudioUrl] = useState(null)
  const [model, setModel] = useState("")
  const [loggedIn, setLoggedIn] = useState(true)
  const [username, setUsername] = useState("admin")
  const [predictedSpecies, setPredictedSpecies] = useState("")

  const handleAudioRecorded = (audioBlob, audioUrl, model) => {
    setAudioBlob(audioBlob)
    setAudioUrl(audioUrl)
    setModel(model)
  }

  return (
    <BrowserRouter>
      <Navbar loggedIn={loggedIn} username={username}/>
      <div className="flex justify-center items-center h-[calc(100vh-4rem)] bg-green-100">
        <Routes>
          <Route path="/" element={<AudioRecorder onAudioRecorded={handleAudioRecorded}/>}/>
          <Route path="/submit" element={<Submit audioBlob={audioBlob} audioUrl={audioUrl} model={model} setPredictedSpecies={setPredictedSpecies} predictedSpecies={predictedSpecies}/>}/>
          <Route path="/my-observations" element={<MyObservations/>}/>
          <Route path="/nearby-observations" element={<ObservationsNearby/>}/>
          <Route path="/nearby-observations" element={<ObservationsNearby/>}/>
          <Route path="/add_observation" element={<AddObservation username={username} predictedSpecies={predictedSpecies}/>}/>
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
