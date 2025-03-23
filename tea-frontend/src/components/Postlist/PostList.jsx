import React from "react";
import { useEffect, useState } from "react";
import { getPosts } from "../../api";
import "./PostList.css";

export default function PostList() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getPosts();
        setPosts(data.posts);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) return <p>Loading posts...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="container">
      <h1>Posts</h1>
      {posts.length === 0 ? (
        <p>No posts yet.</p>
      ) : (
        <ul className="post-list">
          {posts.map((post, index) => (
            <li key={index} className="post">
              <p className="username">{post.username}</p>
              <p className="content">{post.content}</p>
              <p className="timestamp">{new Date(post.createdat).toLocaleString()}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
