import React, { useState } from "react";
import { createPost } from "../../api";

export default function PostManager({ refreshPosts }) {
  const [newPostContent, setNewPostContent] = useState("");

  const handleCreatePost = async () => {
    if (!newPostContent.trim()) return;
    await createPost(newPostContent);
    setNewPostContent("");
    refreshPosts(); // Reload the post list
  };

  return (
    <div>
      <h3>Create a Post</h3>
      <textarea
        value={newPostContent}
        onChange={(e) => setNewPostContent(e.target.value)}
        placeholder="What's on your mind?"
      />
      <button onClick={handleCreatePost}>Post</button>
    </div>
  );
}
