import React, { useState } from "react";
import { searchPosts, searchAccounts, searchHashtags } from "../../api";
import "./SearchBar.css";

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState("posts");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSearch(e) {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResults([]);

    try {
      if (mode === "posts") {
        const data = await searchPosts(query);
        setResults(data.posts);
      } else if (mode === "accounts") {
        const data = await searchAccounts(query);
        setResults(data.accounts);
      } else if (mode === "hashtags") {
        const data = await searchHashtags(query);
        setResults(data.hashtags);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="search-container">
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          placeholder={`Search ${mode}...`}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="search-input"
        />
        <select value={mode} onChange={(e) => setMode(e.target.value)} className="search-select">
          <option value="posts">Posts</option>
          <option value="accounts">Accounts</option>
          <option value="hashtags">Hashtags</option>
        </select>
        <button type="submit" className="search-button">Search</button>
      </form>

      {loading && <p>Searching...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && results.length > 0 && (
        <ul className="search-results">
          {results.map((item, index) => (
            <li key={index}>
              {mode === "accounts" ? (
                <>
                  <strong>{item.username}</strong> – {item.email}
                </>
              ) : (
                <>
                  <strong>{item.username}</strong>: {item.content}
                  <br />
                  <small>{new Date(item.createdat).toLocaleString()}</small>
                </>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
