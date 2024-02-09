from deepface.deepface import DeepFace
import cv2
img= cv2.imread("crying_women_2.webp")
preds= DeepFace.analyze(img)
print(preds)