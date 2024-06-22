
function ObservationTile( {species, coordinates, time, username } ) {
    return (
        <div className="flex">
            <div>{species}</div>
            <div>{coordinates}</div>
            <div>{time}</div>
            <div>{username}</div>
        </div>
    )
}

export default ObservationTile