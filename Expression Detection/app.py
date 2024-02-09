from flask import Flask, request, jsonify , render_template
from deepface import DeepFace
import base64
import numpy as np
import cv2

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.get_json()
    image_data = data['image'][data['image'].find(",")+1:]  # Remove data URL prefix
    image_bytes = base64.b64decode(image_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Analyze emotions using DeepFace
    preds = DeepFace.analyze(image, actions='emotion')
    dominant_emotion=""
    for i in range(len(preds)):
        dominant_emotion += preds[i]['dominant_emotion'] + " , "

    return jsonify({'emotion': dominant_emotion})

if __name__ == '__main__':
    app.run(debug=True)
