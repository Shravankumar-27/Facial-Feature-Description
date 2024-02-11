from flask import Flask, render_template, request, jsonify ,redirect, url_for
import base64
import os
from deepface import DeepFace
import cv2  
import detect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data_url = request.form['data']
    image_data = base64.b64decode(data_url.split(',')[1])

    # Specify the directory to save the frames
    save_directory = 'uploaded_frames'
    os.makedirs(save_directory, exist_ok=True)

    # Save the image to a file
    image_filename = os.path.join(save_directory, 'webcam_frame.jpg')
    with open(image_filename, 'wb') as f:
        f.write(image_data)

    detect.detect()
    print("Detected")
    
    return redirect(url_for('home'))
@app.route('/home')
def home():
    return render_template('output.html')

app.run(debug=True)
