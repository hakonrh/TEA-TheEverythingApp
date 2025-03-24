import React, { useEffect, useState } from "react";

import Navbar from "../components/Navbar/Navbar";
import PostList from "../components/Postlist/PostList";
import PostManager from "../components/PostManager/PostManager";

function Main() {

    const [refreshKey, setRefreshKey] = useState(0);

    return (
        <div>
    	    <Navbar />
            <PostManager refreshPosts={() => setRefreshKey((prev) => prev + 1)} />
            <PostList />
        </div>
    );
}

export default Main;
