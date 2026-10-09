import { HandLandmarker, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.21"; // To Import mediapipes hand tracker replacing the import I deleted in requirements


const startButton = document.getElementById("start-btn");
const speakButton = document.getElementById("speak-btn");
const camera = document.getElementById("camera");

let video; //camera
let handLandmarker; //tradker
let busy = false; // stops anew request going out while the last one waits

startButton.addEventListener("click", async function() {

    startButton.disabled = true;
    startButton.textContent = "Loading...";

    camera.innerHTML = `
        <video id="video" width="600" height="350" autoplay></video>
    `;

    video = document.getElementById("video");

    const stream = await navigator.mediaDevices.getUserMedia({
        video: true
    });

    video.srcObject = stream;

    const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.21/wasm"
    );

    handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath: "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
        },
        runningMode: "VIDEO",
        numHands: 1,
        minHandDetectionConfidence: 0.7
    });

    startButton.textContent = "Detecting";

    setInterval(sendFrame, 300);
});


async function sendFrame() {

    if (busy) return;
    if (video.readyState < 2) return;

    busy = true;

    try {

        const result = handLandmarker.detectForVideo(video, performance.now());

        const points = [];

        if (result.landmarks.length > 0) {

            for (const point of result.landmarks[0]) {
                points.push(point.x, point.y, point.z);
            }
        }

        const response = await fetch(
            "/api/predict",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(points)
            }
        );

        if (!response.ok) {
            document.getElementById("current-sign").textContent = "Server error";
            return;
        }

        const data = await response.json();

        updateDetection(
            data.sign,
            data.confidence,
            data.text
        );

    } finally {

        busy = false;
    }
}


function updateDetection(sign, confidence, text) {

    document.getElementById("current-sign").textContent = sign;

    document.getElementById("confidence").textContent =
        confidence + "%";

    document.getElementById("detected-text").textContent =
        text;
}


speakButton.addEventListener("click", function() {

    const text = document.getElementById("detected-text").textContent;

    if (text.trim() === "") return;

    const speech = new SpeechSynthesisUtterance(text);

    window.speechSynthesis.speak(speech);
});