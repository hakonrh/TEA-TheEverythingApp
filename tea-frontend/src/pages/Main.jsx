import React, { useEffect, useState } from "react";

import Navbar from "../components/Navbar/Navbar";
import PostList from "../components/Postlist/PostList";
import PostManager from "../components/PostManager/PostManager";

function Main() {
    return (
        <div>
    	    <Navbar />
            <PostManager />
            <br /><br />
            <PostList />
        </div>
    );
}

export default Main;
