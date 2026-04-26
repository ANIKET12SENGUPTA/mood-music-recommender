async function getMusic() {
    const moodInput = document.getElementById("text");
    const mood = moodInput.value.trim();
    const resultsDiv = document.getElementById("results");
    const emotionDiv = document.getElementById("emotion");

    if (!mood) {
        alert("Please enter a mood");
        return;
    }

    resultsDiv.innerHTML = "<p>Loading recommendations...</p>";
    emotionDiv.innerHTML = "";

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
        emotionDiv.innerHTML = "Detected Emotion: " + (data.emotion || "unknown");

        const recommendations = data.recommendations || [];

        if (recommendations.length === 0) {
            resultsDiv.innerHTML = "<p>No recommendations found.</p>";
            return;
        }

        recommendations.forEach(track => {
            const item = document.createElement("div");
            item.className = "song";

            item.innerHTML = `
                <h3>${track.name}</h3>
                <p>${track.artist}</p>
                <a href="${track.url}" target="_blank">🎧 Open in Spotify</a>
            `;

            resultsDiv.appendChild(item);
        });

    } catch (error) {
        resultsDiv.innerHTML = "<p>Error getting recommendations.</p>";
        console.error(error);
    }
}