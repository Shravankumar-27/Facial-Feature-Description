from flask import Flask, render_template, request, jsonify
import base64
import os
from deepface import DeepFace
import cv2  

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data_url = request.form['data']
    image_data = base64.b64decode(data_url.split(',')[1])
    typ= str(type(image_data))

    # Specify the directory to save the frames
    save_directory = 'uploaded_frames'
    os.makedirs(save_directory, exist_ok=True)

    # Save the image to a file
    image_filename = os.path.join(save_directory, 'webcam_frame.jpg')
    with open(image_filename, 'wb') as f:
        f.write(image_data)
    img= cv2.imread("A:/FACIAL RECOGNITION/example/uploaded_frames/webcam_frame.jpg")
    preds= DeepFace.analyze(img,actions="emotion")
    var1=preds[0]["dominant_emotion"]


    return jsonify({'message': 'Frame uploaded successfully!', 'filename': image_filename, 'typ': typ , 'var1': var1})

app.run(debug=True)
