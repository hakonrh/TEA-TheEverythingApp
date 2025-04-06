import React, { useEffect, useState } from "react";
import { Link } from "react-router";
import { getAuthStatus } from "../auth/auth";
import "./Navbar.css"; 

function Navbar() {
    const [auth, setAuth] = useState({ isAuthenticated: false, username: "" });

    useEffect(() => {
        setAuth(getAuthStatus());
    }, []);

    function logout() {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        setAuth({ isAuthenticated: false, username: "" });
    }

    return (
        <nav>
            <Link to="/" className="link-style logo">TEA - The Everything App</Link>
            {auth.isAuthenticated ? (
                <>
                    <span>Logged in as {auth.username}.</span>
                    <button onClick={logout} className="logout-button">Logout</button>
                </>
            ) : (
                <>
                    <Link to="/register" className="link-style">Register</Link>
                    <Link to="/login" className="link-style">Log in</Link>
                </>
            )}
        </nav>
    );
}

export default Navbar;