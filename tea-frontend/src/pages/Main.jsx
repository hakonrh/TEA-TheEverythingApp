import React from "react";

import Navbar from "../components/Navbar/Navbar";
import PostList from "../components/Postlist/PostList";
import PostManager from "../components/PostManager/PostManager";
import SearchBar from "../components/SearchBar/SearchBar";

function Main() {
    return (
        <div>
    	    <Navbar />
            <PostManager />
            <br />
            <SearchBar />
            <br />
            <PostList />
        </div>
    );
}

export default Main;
