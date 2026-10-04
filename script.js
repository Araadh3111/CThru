const startButton = document.getElementById("start-btn");
const camera = document.getElementById("camera");

let video;
let canvas;
let context;

startButton.addEventListener("click", async function() {

    camera.innerHTML = `
        <video id="video" width="600" height="350" autoplay></video>
    `;

    video = document.getElementById("video");

    const stream = await navigator.mediaDevices.getUserMedia({
        video: true
    });

    video.srcObject = stream;

    canvas = document.createElement("canvas");
    canvas.width = 600;
    canvas.height = 350;

    context = canvas.getContext("2d");

    setInterval(sendFrame, 500);
});


async function sendFrame() {

    if (!video) return;

    context.drawImage(video, 0, 0, 600, 350);

    canvas.toBlob(async function(blob) {

        const response = await fetch(
            "/api/predict",
            {
                method: "POST",
                body: blob
            }
        );

        const data = await response.json();

        updateDetection(
            data.sign,
            data.confidence,
            data.text
        );

    }, "image/jpeg");
}


function updateDetection(sign, confidence, text) {

    document.getElementById("current-sign").textContent = sign;

    document.getElementById("confidence").textContent =
        confidence + "%";

    document.getElementById("detected-text").textContent =
        text;
}
const speakButton = document.getElementById("speak-btn");

speakButton.addEventListener("click", function() {

    const text = document.getElementById("detected-text").textContent;

    if (text.trim() === "") return;

    const speech = new SpeechSynthesisUtterance(text);

    window.speechSynthesis.speak(speech);
});