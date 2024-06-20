import { Link } from "react-router-dom";

function Navbar(props) {
    const loggedIn = props.loggedIn

    return (
        <div className="bg-green-700 h-[4rem] flex justify-around p-[1rem] items-center">
            <Link to={"/"} className="text-2xl">Predict</Link>
            {loggedIn ? 
                <>
                    <Link to={"/my-observations"} className="text-2xl">My observations</Link>
                    <Link to={"/nearby-observations"} className="text-2xl">Observations nearby</Link>
                </>
            : 
                <Link to={"/login"} className="text-2xl">Log In</Link>
            }
        </div>
    )
}

export default Navbar