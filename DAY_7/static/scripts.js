document.addEventListener("DOMContentLoaded", () => {
  // --- Text-to-Speech Section ---
  const speakBtn = document.getElementById("speak-btn");
  const textInput = document.getElementById("text-input");
  const audioPlayerContainer = document.getElementById("audioPlayer");
  const audioPlayer = document.getElementById("audio-player");

  if (speakBtn && textInput && audioPlayer && audioPlayerContainer) {
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
          body: JSON.stringify({ text, voice_id: "en-US-ken", format: "mp3" })
        });

        const data = await response.json();

        if (!response.ok || !data.audio_url) {
          alert(
            "Error: " + (data.error || data.detail || "No audio URL returned from server.")
          );
          return;
        }

        audioPlayer.src = data.audio_url;
        audioPlayerContainer.style.display = "block";
        audioPlayer.play();
      } catch (err) {
        console.error("Request failed:", err);
        alert("Failed to fetch TTS audio. Check console for details.");
      }
    });
  }

  // --- Echo Bot v2 Section ---
  let mediaRecorder, audioChunks = [], recordedBlob = null;

  const startBtn = document.getElementById('startBtn');
  const stopBtn = document.getElementById('stopBtn');

  if (startBtn && stopBtn) {
    startBtn.addEventListener('click', async () => {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("🎙️ Your browser does not support audio recording.");
        return;
      }
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) audioChunks.push(event.data);
        };

        mediaRecorder.onstop = handleRecordingStop;

        mediaRecorder.start();
        startBtn.disabled = true;
        stopBtn.disabled = false;

        showProcessStatus("🎙️ Recording started...", true);
      } catch (error) {
        alert("❌ Unable to access microphone.");
        console.error("Microphone access error:", error);
      }
    });

    stopBtn.addEventListener('click', () => {
      if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
      }
      startBtn.disabled = false;
      stopBtn.disabled = true;
      showProcessStatus("🛑 Recording stopped. Processing...", true);
    });
  }

  async function handleRecordingStop() {
    startBtn.disabled = false;
    stopBtn.disabled = true;

    recordedBlob = new Blob(audioChunks, { type: 'audio/webm' });
    const url = URL.createObjectURL(recordedBlob);

    // Show original recording
    const originalPlayer = document.getElementById('originalPlayer');
    if (originalPlayer) {
      originalPlayer.src = url;
      originalPlayer.load();
      document.getElementById('originalPlayback')?.classList.remove('hidden');
    }

    showProcessStatus('✅ Recording complete! Processing...', true);

    // Process with Echo Bot pipeline
    await processEchoBot(recordedBlob);
  }

  async function processEchoBot(audioBlob) {
    showProcessStatus('🔄 Processing: Transcribing → Generating Murf Voice...', true);
    document.getElementById('echoPlayback')?.classList.add('hidden');
    document.getElementById('transcriptionArea')?.classList.add('hidden');

    try {
      const formData = new FormData();
      formData.append('file', audioBlob, 'echo_input.webm');

      const response = await fetch('/tts/echo', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (response.ok) {
        showTranscription(data.transcription);
        document.getElementById('transcriptionArea')?.classList.remove('hidden');

        if (data.audio_url) {
          playMurfEcho(data.audio_url);
          showProcessStatus('✅ Echo Bot v2 Complete! Murf voice generated!', true);
        } else {
          showProcessStatus('⚠ No speech detected in the audio.', false);
        }
      } else {
        throw new Error(data.detail || data.message || 'Echo processing failed');
      }
    } catch (error) {
      console.error('Echo Bot error:', error);
      showProcessStatus('❌ Echo processing failed: ' + error.message, false);
    }
  }

  function playMurfEcho(audioUrl) {
    const echoPlayer = document.getElementById('echoPlayer');
    if (!echoPlayer) return;

    echoPlayer.src = audioUrl;
    echoPlayer.load();

    document.getElementById('echoPlayback')?.classList.remove('hidden');

    // Auto-play Murf echo
    setTimeout(() => {
      echoPlayer.play().catch(() => {
        console.log('Auto-play prevented by browser');
      });
    }, 500);
  }

  function showProcessStatus(msg, ok = true) {
    const box = document.getElementById('processStatus');
    if (!box) return;

    box.innerHTML = msg;
    box.className = 'process-status ' + (ok ? 'ok' : 'err');
    box.classList.remove('hidden');
  }

  function showTranscription(text) {
    const transcriptionElement = document.getElementById('transcriptionResult');
    if (transcriptionElement) {
      transcriptionElement.innerText = "📝 Transcription: " + text;
    }
  }
});
