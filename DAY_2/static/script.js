// static/script.js

// This function runs when the DOM is fully loaded.
document.addEventListener("DOMContentLoaded", (event) => {
  // Select the paragraph element with the id 'message'.
  const messageElement = document.getElementById("message");

  // Log a message to the browser's developer console.
  console.log("Frontend JavaScript is loaded and running!");

  // You can add more dynamic functionality here.
  // For example, let's change the message text after a delay.
  setTimeout(() => {
    if (messageElement) {
      messageElement.textContent = "The JavaScript has updated this text!";
      console.log("Text content updated by JavaScript.");
    }
  }, 3000); // 3000 milliseconds = 3 seconds
});