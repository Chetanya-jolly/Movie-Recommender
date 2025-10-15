async function getRecommendations() {
  const movieTitle = document.getElementById("movieInput").value.trim();
  const recommendationsDiv = document.getElementById("recommendations");
  recommendationsDiv.innerHTML = "Loading...";

  if (!movieTitle) {
    recommendationsDiv.innerHTML = "<p>Please enter a movie title.</p>";
    return;
  }

  try {
    const response = await fetch(`/recommend?title=${encodeURIComponent(movieTitle)}`);

    if (!response.ok) throw new Error("Movie not found or server error.");

    const data = await response.json();

    if (data.recommendations && data.recommendations.length > 0) {
      recommendationsDiv.innerHTML = "<h3>Top Recommendations:</h3>";
      data.recommendations.forEach((movie, index) => {
        const div = document.createElement("div");
        div.className = "recommendation";
        div.textContent = `${index + 1}. ${movie}`;
        recommendationsDiv.appendChild(div);
      });
    } else {
      recommendationsDiv.innerHTML = "<p>No recommendations found.</p>";
    }
  } catch (error) {
    recommendationsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
  }
}