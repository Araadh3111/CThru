import { HandLandmarker, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.21";


const startButton = document.getElementById("start-btn");
const speakButton = document.getElementById("speak-btn");
const camera = document.getElementById("camera");
const requiredCount = 8;
const words = ["HELLO","HI","HELP","HOW","HOW ARE YOU","HAPPY","HUNGRY","HOME",
    "YES","NO","PLEASE","THANKS","THANK YOU","SORRY",
    "GOOD","GOOD MORNING","GOOD NIGHT","BYE",
    'WHAT','WHATS UP','WHERE','WHEN','WHY','WHO',
    'WATER','FOOD','EAT','DRINK',
    'I LOVE PIZZA','I AM', 'LOVE','LIKE', 'WANT','NEED',
    'MY NAME IS', 'NAME', 'FRIEND', 'FAMILY', 'SCHOOL',
    'PLAY', 'FOOTBALL', 'RONALDO', 'SIUUUUUUUUUUUUUUUU!',
    'VAMOS',"HACKCLUB!", "BEST", 'THE','MESSI','FOOTBALL','PLANT','CODIHG','HARDWARE','PHYSICS','MACBOOK','FRANCE','MOROCCO','F1'
];
const connections = [
    [0, 1], [1, 2], [2, 3], [3, 4],
    [0,5], [5,6], [6,7], [7,8],
    [9,10], [10,11], [11,12],
    [13,14],[14,15],[15,16],
    [0,17],[17,18],[18,19],[19,20],
    [5,9],[9,13],[13,17]
];
let canvas;
let drawing_tool;
let video;
let handLandmarker;
let busy = false;
let latestHand = null;
let text = "";
let lockedPrediction = null;
let lastPrediction = null;
let predictionCount = 0;
let shownSuggestions = "";

startButton.addEventListener("click", async function() {

    startButton.disabled = true;
    startButton.textContent = "Loading...";

    camera.innerHTML = `
        <video id="video" width="600" height="350" autoplay></video>
        <canvas id = "overlay" width="600" height="350" ></canvas>
    `;

    video = document.getElementById("video");
    
    canvas = document.getElementById("overlay");
    drawing_tool = canvas.getContext("2d");
    video.addEventListener("loadedmetadata", function() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    }); 
    const stream = await navigator.mediaDevices.getUserMedia({
        video: true
    });

    video.srcObject = stream;

    const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.21/wasm"
    );

    handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath: "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
            delegate: "GPU"
            
        },
        runningMode: "VIDEO",
        numHands: 1,
        minHandDetectionConfidence: 0.7
    });

    startButton.textContent = "Detecting";

    setInterval(sendFrame, 100);
    drawLoop();
});
function getCurrentWord(){
    var parts = text.split(" ");
    return parts[parts.length-1]

}

function getSuggestions(){
    var currentword = getCurrentWord()
    const results = [];
    if (currentword === "")
        {return results;}
        
    for (const word of words){
        if (word.startsWith(currentword)) {results.push(word)}
    
    }
    return results.slice(0,3);
}
function acceptSuggestion(word){
    var current = getCurrentWord()
    var keptwords = text.slice(0,text.length-current.length);
    text = keptwords + word + " "
    document.getElementById("detected-text").textContent = text;
    showSuggestions();
    
}
function showSuggestions(){
    var list = getSuggestions();
    var key = list.join("|");
    if (key === shownSuggestions) return;
    shownSuggestions = key;
    var box = document.getElementById("suggestions");
    box.innerHTML = "";

    for (const word of list) {

        var button = document.createElement("button");
        button.textContent = word;
        button.addEventListener("click",function(){acceptSuggestion(word);})
        box.appendChild(button);
    }
}
function drawLoop(){
    if (video.readyState >= 2){
        const result = handLandmarker.detectForVideo(video,performance.now());
        drawing_tool.clearRect(0,0,canvas.width,canvas.height);
        if(result.landmarks.length === 0){
            latestHand = null;
        }
        else{
            latestHand=result.landmarks[0];
             const hand = result.landmarks[0];
            drawing_tool.shadowColor = "#00E5FF";
            drawing_tool.shadowBlur = 15;
            drawing_tool.strokeStyle = "#00E5FF";
            drawing_tool.lineWidth = 2;

            for (const pair of connections) {

                const start = hand[pair[0]];
                const end = hand[pair[1]];

                drawing_tool.beginPath();
                drawing_tool.moveTo(start.x * canvas.width, start.y * canvas.height);
                drawing_tool.lineTo(end.x * canvas.width, end.y * canvas.height);
                drawing_tool.stroke();
            }
            drawing_tool.fillStyle = "#E6B450";
            for (const point of hand){
                drawing_tool.beginPath()
                drawing_tool.arc(point.x * canvas.width,point.y * canvas.height,3,0,Math.PI*2)
                drawing_tool.fill()
            }
            }

            
   
    }
    requestAnimationFrame(drawLoop);
}
async function sendFrame() {
    
    if (busy) return;
    if (video.readyState < 2) return;

    busy = true;

    try {

        
        
        if (latestHand=== null) {

            predictionCount = 0;
            lastPrediction = null;
            lockedPrediction = null;

            updateDetection("None", 0);
            return;
        }

        const points = [];
               
        
        for (const point of latestHand) {
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

    showSuggestions()
}


speakButton.addEventListener("click", function() {

    if (text.trim() === "") return;

    const speech = new SpeechSynthesisUtterance(text);

    window.speechSynthesis.speak(speech);
});
