from deepface import DeepFace
import cv2
img= cv2.imread("A:/FACIAL RECOGNITION/example/uploaded_frames/webcam_frame.jpg")
preds= DeepFace.analyze(img,actions="emotion")
print("Dominant Emotion= : " +preds[0]["dominant_emotion"])
