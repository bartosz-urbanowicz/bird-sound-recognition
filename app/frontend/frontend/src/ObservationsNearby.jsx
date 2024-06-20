import { useState, useEffect } from "react";
import ObservationList from "./ObservationList"

function ObservationsNearby() {
    const [observations, setObservations] = useState([])
    useEffect(() => {
        setObservations([{"species": "Parus major"}]);
    }, []);
    return (
        <div>
            <div>Nearby observations</div>
            <ObservationList observations={observations}/>
        </div>
    )
}

export default ObservationsNearby