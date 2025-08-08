document.addEventListener("DOMContentLoaded", () => {
    const speakBtn = document.getElementById("speak-btn");
    const textInput = document.getElementById("text-input");
    const audioPlayer = document.getElementById("audio-player");

    speakBtn.addEventListener("click", async () => {
        const text = textInput.value.trim();
        if (!text) {
            alert("Please enter some text");
            return;
        }

        try {
            const response = await fetch("/tts", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text })
            });

            if (!response.ok) {
                const err = await response.json();
                alert(`Error: ${err.error}`);
                return;
            }

            const blob = await response.blob();
            const audioURL = URL.createObjectURL(blob);
            audioPlayer.src = audioURL;
            audioPlayer.play();
        } catch (err) {
            console.error("Request failed:", err);
        }
    });
});
