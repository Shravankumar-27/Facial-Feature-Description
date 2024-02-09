// Define global variable to store webcam stream
var webcamStream;

// Dictionary data
var dictionaryData = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
    // Add more key-value pairs as needed
};

// Function to convert dictionary data to string
function dictionaryToString(dictionary) {
    var string = "";
    for (var key in dictionary) {
        string += key + ": " + dictionary[key] + "\n";
    }
    return string;
}

// Display dictionary data in the textarea
var textareaElement = document.getElementById('dictionary-textarea');
textareaElement.value = dictionaryToString(dictionaryData);

// Accessing the webcam feed
navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(stream) {
        // Store webcam stream in the global variable
        webcamStream = stream;

        // Display webcam feed in the video element
        var videoElement = document.getElementById('webcam-video');
        videoElement.srcObject = webcamStream;
    })
    .catch(function(error) {
        console.error('Error accessing webcam:', error);
    });


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Write the variable to a file
const fs = require('fs');
var code="abcd"
fs.writeFile('data.txt', code, (err) => {
  if (err) throw err;
  console.log('Variable written to file');
});
