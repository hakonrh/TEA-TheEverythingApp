import React, { useEffect, useState } from "react";
import { Link } from "react-router";

import Navbar from "../components/Navbar/Navbar";
import PostList from "../components/Postlist/PostList";

function Main() {
    return (
        <div>
    	    <Navbar />
            <PostList />
        </div>
    );
}

export default Main;
