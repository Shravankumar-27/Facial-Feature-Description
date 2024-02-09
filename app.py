from flask import Flask, request, send_file
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import base64

# Create Flask app
app = Flask(__name__)

# Import necessary modules from mediapipe

from mediapipe import landmark_pb2
import mediapipe as mp

# Initialize mediapipe face landmark model
mp_face_landmark = mp.solutions.face_landmark
face_landmark = mp_face_landmark.FaceLandmark(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Function to process video frame and extract landmarks
def process_frame(image_bytes):
    image = Image.open(BytesIO(image_bytes))
    image_np = np.array(image)

    # Convert image to RGB
    if image_np.shape[-1] == 4:  # If image has an alpha channel, remove it
        image_np = image_np[..., :3]
    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

    # Process image and extract face landmarks
    results = face_landmark.process(image_rgb)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw face landmarks on image
            annotated_image = np.copy(image_rgb)
            solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style(1)
            )

            # Convert processed image back to bytes
            processed_image = Image.fromarray(cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
            processed_image_bytes = BytesIO()
            processed_image.save(processed_image_bytes, format='JPEG')
            processed_image_bytes.seek(0)
            
            return processed_image_bytes

    return image_bytes  # Return original image if no face landmarks found

# Route to process video frames
@app.route('/process_frames', methods=['POST'])
def process_frames():
    # Get image data from request
    image_data = request.json['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)
    
    # Process video frame
    processed_image_bytes = process_frame(image_bytes)
    
    # Return processed image as response
    return send_file(processed_image_bytes, mimetype='image/jpeg')

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
