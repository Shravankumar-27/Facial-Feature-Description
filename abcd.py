from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Function to capture frames from webcam stream
def capture_frames():
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Route to display webcam stream
@app.route('/')
def index():
    return render_template('FFD_main.html')

# Route to stream webcam frames
@app.route('/video_feed')
def video_feed():
    return Response(capture_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(debug=True)
