import React, { useEffect, useState } from "react";
import { createPost } from "../../api";
import { getAuthStatus } from "../auth/auth";
import "./PostManager.css"

export default function PostManager() {
  const [newPostContent, setNewPostContent] = useState("");
  const [auth, setAuth] = useState({ isAuthenticated: false });

  useEffect(() => {
    setAuth(getAuthStatus());
  }, []);

  const handleCreatePost = async () => {
    if (!newPostContent.trim()) return;
    await createPost(newPostContent);
    window.location.reload();
  };

  return (
    <div>
      {auth.isAuthenticated ? (
        <div className="create-post-container">
          <h3>Create a Post</h3>
          <textarea className="write-post"
            value={newPostContent}
            onChange={(e) => setNewPostContent(e.target.value)}
            placeholder="What's on your mind?"
          />
          <button onClick={handleCreatePost}>Post</button>
        </div>
      ) : (
        <>
          <div className="login-prompt">Log in to post!</div>
        </>
      )
      }
    </div>

  );
}
