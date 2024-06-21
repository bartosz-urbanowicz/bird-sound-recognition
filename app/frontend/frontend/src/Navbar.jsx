import { Link } from "react-router-dom";

function Navbar(props) {
    const loggedIn = props.loggedIn

    return (
        <div className="bg-green-700 h-[4rem] flex justify-between p-[1rem] items-center pl-[3rem] pr-[3rem]">
            <Link to={"/"} className="w-[2rem] h-[2rem] text-white fill-white navbar-button"><img src="/bird-white.svg" alt="" /></Link>
            {loggedIn ? 
                <>
                    <Link to={"/my-observations"} className="text-xl text-white">My observations</Link>
                    <Link to={"/nearby-observations"} className="text-xl text-white">Observations nearby</Link>
                </>
            : 
                <Link to={"/login"} className="text-xl text-white navbar-button">Log In</Link>
            }
        </div>
    )
}

export default Navbar