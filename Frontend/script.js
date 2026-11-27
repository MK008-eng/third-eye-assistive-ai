const startBtn = document.getElementById("startBtn");

startBtn.addEventListener("click", async function () {

    const userMessage = prompt("How can I help you?");

    if (!userMessage || !userMessage.trim()) {
        return;
    }

    startBtn.textContent = "Processing...";
    startBtn.disabled = true;

    try {

        const response = await fetch("/api/assistant", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: userMessage,
                language: "English"
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }

        alert(data.response);

        const speech = new SpeechSynthesisUtterance(
            data.response
        );

        speech.lang = "en-IN";

        window.speechSynthesis.speak(speech);

    } catch (error) {

        alert("Unable to connect to the assistant. Please try again.");

        console.error(error);

    } finally {

        startBtn.textContent = "Start Assistant";
        startBtn.disabled = false;

    }

}); 