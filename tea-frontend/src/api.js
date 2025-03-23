const API_BASE_URL = "https://tea-theeverythingapp.onrender.com";

export async function getPosts() {
  try {
    const response = await fetch(`${API_BASE_URL}/posts`);
    if (!response.ok) {
      throw new Error("Failed to fetch posts");
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
}
