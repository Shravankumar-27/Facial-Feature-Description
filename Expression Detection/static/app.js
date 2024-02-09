// Get webcam stream and display it in the video element
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        const videoElement = document.getElementById('webcam');
        videoElement.srcObject = stream;
    })
    .catch(error => {
        console.error('Error accessing webcam:', error);
    });
    const videoElement = document.getElementById('webcam');

    // Send webcam frames to backend for processing
    setInterval(() => {
        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/jpeg');
    
        fetch('/process_frame', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('emotionOutput').innerText = data.emotion;
        })
        .catch(error => {
            console.error('Error processing frame:', error);
        });
    }, 1000); // Send frame every second (adjust as needed)
    