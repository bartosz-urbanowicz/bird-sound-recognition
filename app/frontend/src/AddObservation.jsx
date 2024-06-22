import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import GeoForm from './GeoForm';
import ObservationTile from './ObservationTile';
import axios from 'axios';

const api_url = "http://localhost:5000/api"

const AddObservation = ({ predictedSpecies, username }) => {
    const [latitude, setLatitude] = useState('');
    const [longitude, setLongitude] = useState('');
    const [success, setScuccess] = useState(false)
    const navigate = useNavigate()

    console.log(predictedSpecies)

    const handleCoordinatesSubmit = (latitude, longitude) => {
        setLatitude(latitude)
        setLongitude(longitude)
    }

    const handleSubmit = () => {
        axios.post(
            api_url + "/observations/",
            {"species": predictedSpecies, "username": username, "location": `${latitude},${longitude}`}
        )
            .then(response => {
                setScuccess(true)
          })
          .catch(error => {
            alert('Error while posting:', error);
          });
    }

    return (
        <div className="bg-green-300 p-[2rem] rounded-xl">
            {
                success ? 
                <div className={`${success ? "flex" : "hidden"} flex-col justify-center items-center`}>
                    <div className="text-xl mb-[1rem]">Observation submitted!</div>
                    <button className="pushable" onClick={() => navigate("/")}>
                        <span className="front">Back to start</span>
                    </button>
                </div>
                :
                <>
                    <div className="m-[1rem]">
                        <GeoForm handleCoordinatesSubmit={handleCoordinatesSubmit}/>

                    </div>
                    <div className="m-[1rem]">
                        <ObservationTile species={predictedSpecies}/>
                    </div>
                    <div className="flex justify-center">
                        <button className="pushable" onClick={handleSubmit}><span className="front">Submit</span></button>
                    </div>
                </>
            }            
        </div>
    );
};
export default AddObservation;