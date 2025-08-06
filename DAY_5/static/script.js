// static/script.js
// This function runs when the DOM is fully loaded.
document.addEventListener("DOMContentLoaded", (event) => {
  console.log("Frontend JavaScript is loaded and running!");

  // Initialize TTS functionality if elements exist
  initializeTTS();

  // Original functionality - update message if element exists
  const messageElement = document.getElementById("message");
  if (messageElement) {
    setTimeout(() => {
      messageElement.textContent = "The JavaScript has updated this text!";
      console.log("Text content updated by JavaScript.");
    }, 3000); // 3000 milliseconds = 3 seconds
  }
});

// Initialize Text-to-Speech functionality
function initializeTTS() {
  // Get all the DOM elements
  const form = document.getElementById("ttsForm");
  const textInput = document.getElementById("textInput");
  const submitBtn = document.getElementById("submitBtn");
  const loading = document.getElementById("loading");
  const errorMsg = document.getElementById("errorMsg");
  const successMsg = document.getElementById("successMsg");
  const audioPlayer = document.getElementById("audioPlayer");
  const audioElement = document.getElementById("audioElement");
  const audioInfo = document.getElementById("audioInfo");
  const charCount = document.getElementById("charCount");

  // Exit if TTS elements don't exist (for backward compatibility)
  if (!form || !textInput) {
    console.log("TTS elements not found - skipping TTS initialization");
    return;
  }

  console.log("🎤 Initializing TTS functionality...");

  // Character counter functionality
  textInput.addEventListener("input", function () {
    const count = this.value.length;
    if (charCount) {
      charCount.textContent = count;

      // Color coding for character count
      if (count > 2500) {
        charCount.style.color = "#ff6b6b";
      } else if (count > 2000) {
        charCount.style.color = "#ffa726";
      } else {
        charCount.style.color = "#666";
      }
    }
  });

  // Utility functions for messages
  function hideMessages() {
    if (errorMsg) errorMsg.style.display = "none";
    if (successMsg) successMsg.style.display = "none";
  }

  function showError(message) {
    hideMessages();
    if (errorMsg) {
      errorMsg.textContent = message;
      errorMsg.style.display = "block";
      errorMsg.scrollIntoView({ behavior: "smooth" });
    }
    console.error("TTS Error:", message);
  }

  function showSuccess(message) {
    hideMessages();
    if (successMsg) {
      successMsg.textContent = message;
      successMsg.style.display = "block";
    }
    console.log("TTS Success:", message);
  }

  // Main form submission handler
  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    console.log("🚀 TTS form submitted");

    const text = textInput.value.trim();

    // Validation
    if (!text) {
      showError("Please enter some text to convert to speech.");
      return;
    }

    if (text.length > 3000) {
      showError("Text is too long. Please limit to 3000 characters.");
      return;
    }

    // Show loading state
    setLoadingState(true);

    try {
      // Prepare request data
      const requestData = {
        text: text,
        voice_id: document.getElementById("voiceSelect")?.value || "en-US-ken",
        format: "mp3",
        speech_rate: parseInt(
          document.getElementById("speedSelect")?.value || "0"
        ),
      };

      console.log("📤 Sending TTS request:", requestData);

      // Make request to Flask backend
      const response = await fetch("/tts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      const data = await response.json();
      console.log("📥 TTS response:", data);

      if (data.success && data.audio_url) {
        // Success - handle audio
        handleAudioSuccess(data, requestData, text);
      } else {
        // Handle API error
        const errorMessage =
          data.error || "Failed to generate audio. Please try again.";
        showError(`❌ ${errorMessage}`);

        if (data.suggestion) {
          console.log("💡 API Suggestion:", data.suggestion);
        }
      }
    } catch (error) {
      console.error("💥 Request failed:", error);
      showError(
        `❌ Network error: ${error.message}. Please check if the Flask server is running on port 5001.`
      );
    } finally {
      setLoadingState(false);
    }
  });

  // Set loading state
  function setLoadingState(isLoading) {
    if (loading) {
      loading.style.display = isLoading ? "block" : "none";
    }

    if (submitBtn) {
      submitBtn.disabled = isLoading;
      submitBtn.textContent = isLoading
        ? "⏳ Generating..."
        : "🎵 Generate Speech";
    }

    if (isLoading) {
      hideMessages();
      if (audioPlayer) {
        audioPlayer.classList.remove("show");
      }
    }
  }

  // Handle successful audio generation
  function handleAudioSuccess(data, requestData, text) {
    if (audioElement && audioPlayer) {
      // Set audio source
      audioElement.src = data.audio_url;
      audioPlayer.classList.add("show");

      // Update audio info
      if (audioInfo) {
        audioInfo.innerHTML = `
                    <strong>Voice:</strong> ${
                      data.voice_used || requestData.voice_id
                    } &nbsp;|&nbsp;
                    <strong>Format:</strong> ${
                      data.format || "MP3"
                    } &nbsp;|&nbsp;
                    <strong>Characters:</strong> ${
                      data.characters_used || text.length
                    } &nbsp;|&nbsp;
                    <strong>Generated:</strong> ${new Date().toLocaleTimeString()}
                `;
      }

      showSuccess(
        "✅ Audio generated successfully! You can now play it below."
      );

      // Auto-scroll to audio player after a short delay
      setTimeout(() => {
        audioPlayer.scrollIntoView({ behavior: "smooth" });
      }, 500);
    }
  }

  // Audio event listeners
  if (audioElement) {
    audioElement.addEventListener("loadstart", function () {
      console.log("🎵 Audio loading started");
    });

    audioElement.addEventListener("canplay", function () {
      console.log("✅ Audio ready to play");
    });

    audioElement.addEventListener("error", function (e) {
      console.error("❌ Audio error:", e);
      showError(
        "❌ Failed to load audio. The audio URL may be invalid or expired."
      );
    });

    audioElement.addEventListener("play", function () {
      console.log("▶️ Audio playback started");
    });

    audioElement.addEventListener("ended", function () {
      console.log("⏹️ Audio playback ended");
    });
  }

  // Sample texts for testing (optional feature)
  const sampleTexts = [
    "Hello! Welcome to our text-to-speech demonstration. This is a sample of what our AI voice can do.",
    "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet.",
    "In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole filled with the ends of worms and an oozy smell.",
    "To be or not to be, that is the question. Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune.",
    "Artificial intelligence is transforming the way we interact with technology, making it more natural and accessible.",
    "The sun was setting behind the mountains, painting the sky in brilliant shades of orange, pink, and purple.",
  ];

  // Optional: Add sample text on double-click (uncomment if desired)
  /*
    textInput.addEventListener('dblclick', function() {
        const randomText = sampleTexts[Math.floor(Math.random() * sampleTexts.length)];
        this.value = randomText;
        this.dispatchEvent(new Event('input')); // Trigger character counter update
        console.log('📝 Sample text loaded');
    });
    */

  // Keyboard shortcuts (optional enhancement)
  document.addEventListener("keydown", function (e) {
    // Ctrl/Cmd + Enter to submit form
    if (
      (e.ctrlKey || e.metaKey) &&
      e.key === "Enter" &&
      textInput.value.trim()
    ) {
      e.preventDefault();
      form.dispatchEvent(new Event("submit"));
    }
  });

  console.log("✅ TTS functionality initialized successfully!");
}

// Utility function to test TTS endpoint
async function testTTSEndpoint() {
  try {
    const response = await fetch("/tts/test");
    const data = await response.json();
    console.log("🧪 TTS Test Result:", data);
    return data;
  } catch (error) {
    console.error("❌ TTS Test Failed:", error);
    return null;
  }
}

// Utility function to get available voices
async function getAvailableVoices() {
  try {
    const response = await fetch("/tts/voices");
    const data = await response.json();
    console.log("🎙️ Available Voices:", data);
    return data;
  } catch (error) {
    console.error("❌ Failed to get voices:", error);
    return null;
  }
}

// Export functions for potential use in console or other scripts
window.TTSUtils = {
  testTTSEndpoint,
  getAvailableVoices,
};

// Echo Bot Functionality
document.addEventListener("DOMContentLoaded", () => {
  const startBtn = document.getElementById("startRecordBtn");
  const stopBtn = document.getElementById("stopRecordBtn");
  const echoAudioElement = document.getElementById("echoAudioElement");
  const echoAudioPlayer = document.getElementById("echoAudioPlayer");

  let mediaRecorder;
  let audioChunks = [];

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert("🎙️ Your browser does not support audio recording.");
    startBtn.disabled = true;
    stopBtn.disabled = true;
    return;
  }

  startBtn.addEventListener("click", async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);

      audioChunks = [];
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        const audioUrl = URL.createObjectURL(audioBlob);
        echoAudioElement.src = audioUrl;
        echoAudioPlayer.classList.add("show");
        echoAudioElement.play();
        console.log("🔁 Playing recorded audio");
      };

      mediaRecorder.start();
      console.log("🎙️ Recording started");

      startBtn.disabled = true;
      stopBtn.disabled = false;
    } catch (error) {
      console.error("❌ Error accessing microphone:", error);
      alert("❌ Unable to access microphone. Please allow permission.");
    }
  });

  stopBtn.addEventListener("click", () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
      console.log("🛑 Recording stopped");
    }

    startBtn.disabled = false;
    stopBtn.disabled = true;
  });
});