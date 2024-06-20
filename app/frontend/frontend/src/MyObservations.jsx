import { useState, useEffect } from "react";
import ObservationList from "./ObservationList"

function MyObservations() {
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

export default MyObservations