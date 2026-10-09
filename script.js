import { HandLandmarker, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.21";

const startButton = document.getElementById("start-btn");
const speakButton = document.getElementById("speak-btn");
const camera = document.getElementById("camera");

const requiredCount = 8;

let video;
let handLandmarker;
let busy = false;

let text = "";
let lockedPrediction = null;
let lastPrediction = null;
let predictionCount = 0;

startButton.addEventListener("click", async function() {

    startButton.disabled = true;
    startButton.textContent = "Loading...";

    camera.innerHTML = `
        <video id="video" width="600" height="350" autoplay></video>
        <canvas id = "overlay" width="600" height="350" ></canvas>
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

    setInterval(sendFrame, 100);
});


async function sendFrame() {

    if (busy) return;
    if (video.readyState < 2) return;

    busy = true;

    try {

        const result = handLandmarker.detectForVideo(video, performance.now());

        if (result.landmarks.length === 0) {

            predictionCount = 0;
            lastPrediction = null;
            lockedPrediction = null;

            updateDetection("None", 0);
            return;
        }

        const points = [];

        for (const point of result.landmarks[0]) {
            points.push(point.x, point.y, point.z);
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

        addToText(data.sign);

        updateDetection(data.sign, data.confidence);

    } finally {

        busy = false;
    }
}


function addToText(prediction) {

    if (prediction === lastPrediction) {

        predictionCount += 1;

    } else {

        lastPrediction = prediction;
        predictionCount = 1;
    }

    if (predictionCount >= requiredCount) {

        if (prediction !== lockedPrediction) {

            if (prediction === "space") {

                text += " ";

            } else if (prediction === "backspace") {

                text = text.slice(0, -1);

            } else if (prediction === "clear") {

                text = "";

            } else {

                text += prediction;
            }

            lockedPrediction = prediction;

            predictionCount = 0;
        }
    }
}


function updateDetection(sign, confidence) {

    document.getElementById("current-sign").textContent = sign;

    document.getElementById("confidence").textContent =
        confidence + "%";

    document.getElementById("detected-text").textContent =
        text;
}


speakButton.addEventListener("click", function() {

    if (text.trim() === "") return;

    const speech = new SpeechSynthesisUtterance(text);

    window.speechSynthesis.speak(speech);
});