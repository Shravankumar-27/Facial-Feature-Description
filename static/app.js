// Get references to HTML elements
const webcamVideo = document.getElementById('webcam');
const processedVideoCanvas = document.getElementById('processedVideoCanvas');
const processedVideoCtx = processedVideoCanvas.getContext('2d');

// Initialize webcam stream
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        webcamVideo.srcObject = stream;
    })
    .catch(error => {
        console.error('Error accessing webcam:', error);
    });

// Function to capture video frames from webcam and send to backend
function captureAndProcessFrames() {
    // Capture video frame from webcam
    processedVideoCtx.drawImage(webcamVideo, 0, 0, processedVideoCanvas.width, processedVideoCanvas.height);
    const imageData = processedVideoCanvas.toDataURL('image/jpeg');

    // Send captured frame to backend for processing
    fetch('/process_frames', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.blob())
    .then(blob => {
        // Display processed video frame in third box
        const objectURL = URL.createObjectURL(blob);
        const processedVideo = new Image();
        processedVideo.onload = function() {
            processedVideoCtx.drawImage(processedVideo, 0, 0, processedVideoCanvas.width, processedVideoCanvas.height);
            URL.revokeObjectURL(objectURL);
        };
        processedVideo.src = objectURL;
    })
    .catch(error => {
        console.error('Error processing frame:', error);
    });
}

// Call the captureAndProcessFrames function repeatedly to continuously process frames
setInterval(captureAndProcessFrames, 1000); // Adjust as needed
