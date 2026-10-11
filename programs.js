const programsBox = document.getElementById("programs");
const runningText = document.getElementById("running");
const stopButton = document.getElementById("stop-btn");
const cameraBox = document.getElementById("camera");
const startDetectButton = document.getElementById("start-btn");
const loader = document.getElementById("loader");

let currentId = null;

window.addEventListener("load", function() {
    this.setTimeout(function() {
        loader.classList.add("hidden");
    }, 1200);
});

async function loadPrograms() {
    try {
        const response = await fetch("/api/programs");
        const programs = await response.json();

        programsBox.innerHTML = ""

        for (const program of programs) {
            const button = document.createElement("button");
            button.className = "program-btn";
            button.dataset.id = program.id;
            button.innerHTML = program.name + '<span class="member">' + program.member + '</span>';
            button.disabled = !program.ready;
            button.addEventListener("click", function() {startProgram(program.id, program.name); });
            programsBox.appendChild(button);
        }

    } catch (error) {
        programsBox.textContent = "programs only work when the site runs locally (python server.py)";
        stopButton.disabled = true;
    }
}

async function startProgram(id, name) {
    const video = cameraBox.querySelector("video");
    if (video && video.srcObject) {
        video.srcObject.getTracks().forEach(function(track) { track.stop(); });
    }
    startDetectButton.disabled = true;

    cameraBox.innerHTML = '<p class="cam-loading">Starting ' + name + '...</p><img id="stream" alt="">';
    runningText.textContent = "Starting..."

    const response = await fetch("/api/start/" + id, { method: "POST"});
    const data = await response.json();

    if (!data.ok) {
        cameraBox.innerHTML = "<p>" + data.error + "</p>";
        runningText.textContent = "Nothing";
        return;
    } 

    currentId = id;
    runningText.textContent = data.running;
    highlightButton(id);

    const stream = document.getElementById("stream");
    stream.onload = function() {
        const loading = cameraBox.querySelector(".cam-loading");
        if (loading) loading.remove();
    };
    stream.src = "/video?t=" + Date.now();
}

function highlightButton(id) {
    for (const button of programsBox.querySelectorAll(".program-btn")) {
        button.classList.toggle("active", button.dataset.id === id);
    }
}

stopButton.addEventListener("click", async function() {
    await fetch("/api/stop", {method: "POST"});
    location.reload();
})

document.addEventListener("keydown", function(event) {
    if (currentId === null) return;
    if (event.key.length !== 1) return;
    if (event.key === " ") event.preventDefault();

    fetch("/api/key", {
        method: "POST",
        headers: {"Content-Type": "application/json" },
        body: JSON.stringify({ key: event.key.toLowerCase() })    });
});

async function updateStatus() {
    if (currentId === null) return;
    try{
        const response = await fetch("/api/status");
        const data = await response.json();
        if (data.running === null) {
            location.reload();
        }
    } catch (error) {

    }
}

loadPrograms();

setInterval(updateStatus, 2000);