import React, { useEffect, useState } from "react";
import { Link } from "react-router";

function Navbar() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [username, setUsername] = useState("");


    useEffect(() => {
        const token = localStorage.getItem("token");
        const storedUsername = localStorage.getItem("username");

        setIsAuthenticated(!!token);
        setUsername(storedUsername || "");
    }, []);

    function logout() {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        setIsAuthenticated(false);
        setUsername("");
    }

    return (
        <div>
            <Link to="/" className="link-style">Home</Link>
            {isAuthenticated ? (
                <>
                    <span>Logged in as {username}.</span>
                    <button onClick={logout} className="logout-button">Logout</button>
                </>
            ) : (
                <>
                    <Link to="/register" className="link-style">Register</Link>
                    <Link to="/login" className="link-style">Log in</Link>
                </>
            )}
        </div>
    );
}

export default Navbar;


/*
Logo

Posts
Accounts

Login/Logout
*/