async function getRecommendations() {
    const moodInput = document.getElementById("moodInput");
    const mood = moodInput.value.trim();
    const resultsDiv = document.getElementById("results");

    if (!mood) {
        alert("Please enter a mood");
        return;
    }

    resultsDiv.innerHTML = "<p>Loading...</p>";

    try {
        const response = await fetch("/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: mood })
        });

        const data = await response.json();
        resultsDiv.innerHTML = "";

        const recommendations = data.recommendations || [];

        if (recommendations.length === 0) {
            resultsDiv.innerHTML = "<p>No recommendations found.</p>";
            return;
        }

        recommendations.forEach(track => {
            const trackDiv = document.createElement("div");
            trackDiv.innerHTML = `
                <p><strong>${track.name}</strong> - ${track.artist}</p>
                <a href="${track.url}" target="_blank">Open in Spotify</a>
            `;
            resultsDiv.appendChild(trackDiv);
        });
    } catch (error) {
        resultsDiv.innerHTML = "<p>Error getting recommendations.</p>";
        console.error(error);
    }
}
