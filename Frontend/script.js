const startBtn = document.getElementById("startBtn");
const voiceBtn = document.getElementById("voiceBtn");
const statusText = document.getElementById("status");

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

async function sendMessage(message) {

    statusText.textContent = "Processing your request...";

    try {

        const response = await fetch("/api/assistant", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                language: "English"
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }

        statusText.textContent = data.response;

        const speech = new SpeechSynthesisUtterance(
            data.response
        );

        speech.lang = "en-IN";

        window.speechSynthesis.speak(speech);

    } catch (error) {

        statusText.textContent =
            "Unable to connect to the assistant.";

        console.error(error);

    }
}


// Text input
startBtn.addEventListener("click", function () {

    const message = prompt("How can I help you?");

    if (message && message.trim()) {
        sendMessage(message.trim());
    }

});


// Voice input
if (SpeechRecognition) {

    const recognition = new SpeechRecognition();

    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    voiceBtn.addEventListener("click", function () {

        statusText.textContent = "Listening...";

        recognition.start();

    });

    recognition.onresult = function (event) {

        const spokenMessage =
            event.results[0][0].transcript;

        statusText.textContent =
            "You said: " + spokenMessage;

        sendMessage(spokenMessage);

    };

    recognition.onerror = function (event) {

        statusText.textContent =
            "Voice recognition error: " + event.error;

    };

    recognition.onend = function () {

        console.log("Voice recognition ended.");

    };

} else {

    voiceBtn.disabled = true;

    statusText.textContent =
        "Voice recognition is not supported in this browser.";

}