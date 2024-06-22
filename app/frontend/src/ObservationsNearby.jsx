import { useState, useEffect } from "react";
import ObservationList from "./ObservationList"
import axios from "axios";

const api_url = "http://localhost:5000/api/"

function ObservationsNearby() {
    const [observations, setObservations] = useState([])
    useEffect(() => {
        axios.get(api_url + "/observations", {"location": "1,1"})
        setObservations([{"species": "Parus major"}]);
    }, []);
    return (
        <div>
            <div className="text-xl m-[1rem]">Nearby observations</div>
            <ObservationList observations={observations}/>
        </div>
    )
}

export default ObservationsNearby