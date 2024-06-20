import { useState, useEffect } from "react";
import ObservationTile from "./ObservationTile"

function ObservationList(props) {
    const [observations, setObservations] = useState([])
    useEffect(() => {
        setObservations(props.observations);
    }, [props.observations]);

    return (
        <ul>{observations.map((observation) => {
            return (<li key={observation.id}>
                <ObservationTile 
                    species={observation.species}
                />
                <button className='button-primary' onClick={() => handleDelete(observation.id)}><i className="fa-solid fa-trash-can"></i></button>
            </li> )
        })}
        </ul>
    )
}

export default ObservationList