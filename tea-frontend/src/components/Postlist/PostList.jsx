import React, { useEffect, useState } from "react";
import { getPosts, getAccounts } from "../../api";
import "./PostList.css";

export default function PostList() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [view, setView] = useState("posts");

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
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <div className="button-group">
        <button onClick={() => setView("posts")}>Show Posts</button>
        <button onClick={() => setView("accounts")}>Show Accounts</button>
      </div>

      {loading && <p>Loading {view}...</p>}
      {error && <p className="error">Error: {error}</p>}

      {!loading && !error && (
        <>
          {view === "posts" && (
            <ul className="post-list">
              {data.length === 0 ? <p>No posts yet.</p> : data.map((post, index) => (
                <li key={index} className="post">
                  <p className="username">{post.username}</p>
                  <p className="content">{post.content}</p>
                  <p className="timestamp">{new Date(post.createdat).toLocaleString()}</p>
                </li>
              ))}
            </ul>
          )}

          {view === "accounts" && (
            <ul className="account-list">
              {data.length === 0 ? <p>No accounts yet.</p> : data.map((account, index) => (
                <li key={index} className="account">
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
