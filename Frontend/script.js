const startBtn = document.getElementById("startBtn");

startBtn.addEventListener("click", function () {
    alert("Welcome to Third Eye Assistive AI!");

    const message = new SpeechSynthesisUtterance(
        "Hello! Welcome to Third Eye. Your AI assistant is ready."
    );

    speechSynthesis.speak(message);
});
