const API_CACHE_URL = "https://tea-loadbalancer.onrender.com";
const API_BACKEND_URL = "https://tea-theeverythingapp.onrender.com";

function getAuthHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// Get all posts
export async function getPosts() {
  try {
    const response = await fetch(`${API_CACHE_URL}/posts`);
    if (!response.ok) {
      throw new Error("Failed to fetch posts");
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
}

// Get current user's posts
export async function getUserPosts() {
  const response = await fetch(`${API_CACHE_URL}/myposts`, {
    headers: getAuthHeaders(),
  });
  return response.json();
}


// Create a new post
export async function createPost(content) {
  const response = await fetch(`${API_BACKEND_URL}/posts`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeaders() },
    body: JSON.stringify({ content }),
  });
  return response.json();
}

// Edit a post
export async function editPost(postId, newContent) {
  const response = await fetch(`${API_BACKEND_URL}/posts/${postId}`, {
    method: "PUT",
    headers: { 
      ...getAuthHeaders(), 
      "Content-Type": "application/json" 
    },
    body: JSON.stringify({ new_content: newContent }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to edit post");
  }

  return response.json();
}


// Delete a post
export async function deletePost(postId) {
  await fetch(`${API_BACKEND_URL}/posts/${postId}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });
}

// Get all accounts
export async function getAccounts() {
  try {
    const response = await fetch(`${API_CACHE_URL}/accounts`);
    if (!response.ok) {
      throw new Error("Failed to fetch accounts");
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
}

// Register new user
export async function registerUser(username, email, password) {
  try {
    const response = await fetch(`${API_BACKEND_URL}/user/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Registration failed");
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
}

// Log in user
export async function loginUser(email, password) {
  try {
    const formData = new URLSearchParams();
    formData.append("email", email);
    formData.append("password", password);

    const response = await fetch(`${API_BACKEND_URL}/user/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Login failed");
    }

    const data = await response.json();
    localStorage.setItem("token", data.access_token);
    return data;
  } catch (error) {
    throw error;
  }
}

// Search posts
export async function searchPosts(query) {
  const response = await fetch(`${API_CACHE_URL}/search/posts?q=${encodeURIComponent(query)}`);
  if (!response.ok) {
    throw new Error("Failed to search posts");
  }
  return await response.json();
}

// Search accounts
export async function searchAccounts(query) {
  const response = await fetch(`${API_CACHE_URL}/search/accounts?q=${encodeURIComponent(query)}`);
  if (!response.ok) {
    throw new Error("Failed to search accounts");
  }
  return await response.json();
}

// Search hashtags
export async function searchHashtags(query) {
  const response = await fetch(`${API_CACHE_URL}/search/hashtags?q=${encodeURIComponent(query)}`);
  if (!response.ok) {
    throw new Error("Failed to search hashtags");
  }
  return await response.json();
}

// Like a post
export async function likePost(postId) {
  const response = await fetch(`${API_BACKEND_URL}/posts/${postId}/like`, {
    method: "PATCH",
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to like post");
  }

  return await response.json();
}
