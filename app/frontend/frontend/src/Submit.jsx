import axios from 'axios'
import { useEffect, useState } from 'react';
import { birdNames, birdImages } from './birds.js'
import { useNavigate } from 'react-router-dom';

const Submit = ({ audioBlob, audioUrl, model }) => {
    const [predictedClass, setPredictedClass] = useState("")
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
            setPredictedClass(response.data["bird_name"])
            setAccuracy(response.data["probability"])
          } catch (error) {
            console.error('Error while posting:', error);
          }
    }
    postData()
    }, [])
    

    const handleClick = (e) => {
      navigate("/")
    }

    return (
        <div className='flex flex-col'>
            {predictedClass == "" ? 
              <div className='flex flex-col justify-center items-center'>
                <div className="lds-ripple"><div></div><div></div></div>
              </div> :
              <div className='flex flex-col justify-center items-center'>
                <img src={birdImages[predictedClass]} alt={predictedClass} className='w-[10em] rounded-2xl' />
                <div><span className='font-bold'>{predictedClass}</span> ({birdNames[predictedClass]})</div>
                <div>{accuracy.toFixed(2) * 100}% confidence</div>
              </div>
            }
            <div className="audio-container flex items-center justify-center m-[1em]">
                <audio src={audioUrl} controls></audio>
                <a download href={audioUrl}>
                <i className="fa-solid fa-download m-[0.5em]"></i>
                </a>
            </div>
            <button onClick={handleClick}>Go back</button>
        </div>
    );
};
export default Submit;