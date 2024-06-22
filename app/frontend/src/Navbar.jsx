import { Link } from "react-router-dom";
import { useState } from "react";

function Navbar({ loggedIn, username }) {
    const [profileMenu, toggleProfileMenu] = useState(false)

    return (
        <div className="bg-green-700 h-[4rem] flex justify-between p-[1rem] items-center pl-[3rem] pr-[3rem]">
            <Link to={"/"} className="w-[2rem] h-[2rem] text-white fill-white navbar-button"><img src="/bird-white.svg" alt="" /></Link>
            {loggedIn ? 
                <>
                    <div 
                        className={
                            `${profileMenu ? "flex" : "hidden"}  
                            flex-col items-start p-6 absolute top-20 right-0 mx-4 my-2 min-w-[140px] rounded-xl bg-green-300`}
                    >
                       <Link to={"/my-observations"} className="text-xl">My observations</Link>
                       <button className="text-xl">Log out</button>
                    </div>
                    
                    <Link to={"/nearby-observations"} className="navbar-button">Observations nearby</Link>
                    <button className="navbar-button" onClick={() => toggleProfileMenu((prev) => !prev)}>{username}</button>
                </>
            : 
                <Link to={"/login"} className="navbar-button">Log In</Link>
            }
        </div>
    )
}

export default Navbar