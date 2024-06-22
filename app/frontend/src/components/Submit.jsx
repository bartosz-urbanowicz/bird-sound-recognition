import axios from 'axios'
import { useEffect, useState } from 'react';
import { birdNames, birdImages } from './birds.js'
import { useNavigate } from 'react-router-dom';

const Submit = ({ audioBlob, audioUrl, model, setPredictedSpecies, predictedSpecies }) => {
    const [waitingForPrediction, setWaitingForPrediction] = useState(true)
    const [accuracy, setAccuracy] = useState(0)
    const navigate = useNavigate()

    const api_url = "http://localhost:5000/api/predict/"

    function blobToBase64(blob) {
        return new Promise((resolve, _) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result.split(',')[1]);
          reader.readAsDataURL(blob);
        });
      }

    useEffect(() => {
      const postData = async () => {
        const base64audio = await blobToBase64(audioBlob)
        try {
            const response = await axios.post(api_url, {data: base64audio, model: model});
            setPredictedSpecies(response.data["bird_name"])
            setAccuracy(response.data["probability"])
            setWaitingForPrediction(false)
          } catch (error) {
            console.error('Error while posting:', error);
          }
    }
    postData()
    }, [])
    

    return (
        <div className='flex justify-center items-center flex-col bg-green-200 p-[2rem] rounded-xl'>
            {waitingForPrediction ? 
              <div className='flex flex-col justify-center items-center'>
                <div className="lds-ripple"><div></div><div></div></div>
              </div> :
              <div className='flex flex-col justify-center items-center'>
                <img src={birdImages[predictedSpecies]} alt={predictedSpecies} className='w-[10em] rounded-2xl' />
                <div><span className='font-bold'>{predictedSpecies}</span> ({birdNames[predictedSpecies]})</div>
                <div>{accuracy.toFixed(2) * 100}% confidence</div>
              </div>
            }
            <div className="audio-container flex items-center justify-center m-[1em]">
                <audio src={audioUrl} controls></audio>
                <a download href={audioUrl}>
                <i className="fa-solid fa-download m-[0.5em]"></i>
                </a>
            </div>
            <div className="flex mt-[2rem]">
              <button className="pushable flex-1 mr-[2rem] w-[8rem]" onClick={() => navigate("/")}>
                <span className="front">Back</span>
              </button>
              <button 
                className={`pushable flex-1 w-[8rem] ${waitingForPrediction ? "bg-gray-600" : ""}`} 
                onClick={waitingForPrediction ? () => {} : () => navigate("/add_observation")}
              >
                <span className={`front  ${waitingForPrediction ? "bg-gray-500" : ""}`}>Publish</span>
              </button>
            </div>
        </div>
    );
};
export default Submit;