import React, { useEffect, useState } from "react";
import { getPosts, getAccounts, getUserPosts, editPost, deletePost } from "../../api";
import "./PostList.css";

export default function PostList() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [view, setView] = useState("posts");
  const [editingPost, setEditingPost] = useState(null);
  const [editContent, setEditContent] = useState("");

  useEffect(() => {
    fetchData();
  }, [view]);

  async function fetchData() {
    setLoading(true);
    setError(null);
    
    try {
      let result;
      if (view === "posts") {
        result = await getPosts();
        setData(result.posts);
      } else if (view === "accounts") {
        result = await getAccounts();
        setData(result.accounts);
      } else if (view === "myPosts") {
        result = await getUserPosts();
        setData(result.posts);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleEditPost(postId) {
    await editPost(postId, editContent);
    setEditingPost(null);
    fetchData(); // Refresh posts
  }

  async function handleDeletePost(postId) {
    await deletePost(postId);
    fetchData(); // Refresh posts
  }

  return (
    <div className="container">
      <div className="button-group">
        <button onClick={() => setView("posts")}>Show All Posts</button>
        <button onClick={() => setView("myPosts")}>Show My Posts</button>
        <button onClick={() => setView("accounts")}>Show Accounts</button>
      </div>

      {loading && <p>Loading {view}...</p>}
      {error && <p className="error">Error: {error}</p>}

      {!loading && !error && (
        <>
          {view === "posts" && (
            <ul className="post-list">
              {data.length === 0 ? <p>No posts yet.</p> : data.map((post) => (
                <li key={post.postid} className="post">
                  <p className="username">{post.username}</p>
                  <p className="content">{post.content}</p>
                  <p className="timestamp">{new Date(post.createdat).toLocaleString()}</p>
                </li>
              ))}
            </ul>
          )}

          {view === "myPosts" && (
            <ul className="post-list">
              {data.length === 0 ? <p>You haven't posted anything yet.</p> : data.map((post) => (
                <li key={post.postid} className="post">
                  {editingPost === post.postid ? (
                    <>
                      <textarea 
                        value={editContent} 
                        onChange={(e) => setEditContent(e.target.value)}
                      />
                      <button onClick={() => handleEditPost(post.postid)}>Save</button>
                      <button onClick={() => setEditingPost(null)}>Cancel</button>
                    </>
                  ) : (
                    <>
                      <p className="content">{post.content}</p>
                      <p className="timestamp">{new Date(post.createdat).toLocaleString()}</p>
                      <button onClick={() => { setEditingPost(post.postid); setEditContent(post.content); }}>Edit</button>
                      <button onClick={() => handleDeletePost(post.postid)}>Delete</button>
                    </>
                  )}
                </li>
              ))}
            </ul>
          )}

          {view === "accounts" && (
            <ul className="account-list">
              {data.length === 0 ? <p>No accounts yet.</p> : data.map((account) => (
                <li key={account.email} className="account">
                  <p className="username">{account.username}</p>
                  <p className="email">{account.email}</p>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </div>
  );
}
