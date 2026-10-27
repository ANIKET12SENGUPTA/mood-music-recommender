let currentRecommendations = [];

async function getMusic() {
    const moodInput = document.getElementById("text");
    const mood = moodInput.value.trim();
    const resultsDiv = document.getElementById("results");
    const emotionDiv = document.getElementById("emotion");

    if (!mood) {
        alert("Please describe your mood or the vibe you want.");
        return;
    }

    resultsDiv.innerHTML = "<p>Loading recommendations...</p>";
    emotionDiv.innerHTML = "";

    try {
        const response = await fetch("/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: mood })
        });

        const data = await response.json();
        currentRecommendations = data.recommendations || [];

        resultsDiv.innerHTML = "";
        emotionDiv.innerHTML = "Detected vibe: " + (data.emotion || "unknown");

        const recommendations = data.recommendations || [];
        if (recommendations.length === 0) {
            resultsDiv.innerHTML = "<p>No recommendations found. Try a different mood or activity.</p>";
            return;
        }

        recommendations.forEach((track) => {
            const item = document.createElement("div");
            item.className = "song";

            item.innerHTML = `
                <div class="song-info">
                    <h3>${track.name}</h3>
                    <p>${track.artist}</p>
                </div>
                <div class="song-actions">
                    <a href="${track.url || '#'}" target="_blank">Open in Spotify</a>
                    <button class="mini" data-uri="${track.uri || ''}" data-name="${track.name}">Add to Playlist</button>
                </div>
            `;

            item.querySelector("button.mini").addEventListener("click", () => savePlaylist([track.uri]));
            resultsDiv.appendChild(item);
        });

    } catch (error) {
        resultsDiv.innerHTML = "<p>Error getting recommendations. Please try again.</p>";
        console.error(error);
    }
}

async function savePlaylist(trackUris = null) {
    const selectedUris = trackUris || currentRecommendations
        .map((track) => track.uri)
        .filter(Boolean);

    if (!selectedUris.length) {
        alert("There are no songs to save yet. Generate recommendations first.");
        return;
    }

    try {
        const response = await fetch("/playlist/create", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: "VibeVault Mix",
                track_uris: selectedUris
            })
        });

        const data = await response.json();
        if (!response.ok || data.error) {
            throw new Error(data.error || "Unable to save to Spotify playlist.");
        }

        const playlistUrl = data.playlist.url;
        window.open(playlistUrl, "_blank");
        alert(`Playlist created: ${data.playlist.name}`);
    } catch (error) {
        alert(error.message || "Login to Spotify first to save songs to a playlist.");
    }
}

async function updateLoginStatus() {
    const statusEl = document.getElementById("auth-status");
    const loginBtn = document.getElementById("spotify-login");
    try {
        const response = await fetch("/auth/status");
        const data = await response.json();

        if (data.logged_in && data.user) {
            statusEl.textContent = `Spotify connected: ${data.user.display_name || data.user.id || "user"}`;
            loginBtn.textContent = "Log out from Spotify";
            loginBtn.onclick = () => window.location.href = "/auth/logout";
        } else {
            statusEl.textContent = "Spotify login not active yet. Connect your account to save recommendations to a playlist.";
            loginBtn.textContent = "Login with Spotify";
            loginBtn.onclick = () => window.location.href = "/auth/login";
        }
    } catch (error) {
        statusEl.textContent = "Unable to verify Spotify login status.";
        loginBtn.textContent = "Login with Spotify";
        loginBtn.onclick = () => window.location.href = "/auth/login";
    }
}

window.addEventListener("DOMContentLoaded", () => {
    const loginBtn = document.getElementById("spotify-login");
    if (loginBtn) {
        loginBtn.onclick = () => window.location.href = "/auth/login";
    }
    updateLoginStatus();
});