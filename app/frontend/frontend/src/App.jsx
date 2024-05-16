import AudioRecorder from "./AudioRecorder"
import Submit from "./Submit";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {

  return (
    <div className="flex justify-center items-center h-[100vh] bg-green-100">
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<AudioRecorder/>}>
          <Route path="submit" element={<Submit/>}/>
        </Route>
      </Routes>
    </BrowserRouter>
    </div>
  )
}

export default App
