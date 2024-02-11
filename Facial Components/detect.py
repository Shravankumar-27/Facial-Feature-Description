import mediapipe
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
import cv2
import math
import numpy as np
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from PIL import Image



def draw_landmarks_on_image(rgb_image, detection_result):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.
    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])


    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_contours_style(1))
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_NOSE,
        landmark_drawing_spec=None)


  return annotated_image




# Performs resizing and showing the image
def resize_and_show(image):
  DESIRED_HEIGHT = 480
  DESIRED_WIDTH = 480
  h, w = image.shape[:2]
  if h < w:
    img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
  else:
    img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
  #img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  # Convert the ndarray to a PIL Image
  # print("Output")
  img_file = Image.fromarray(img)

  # Save the PIL Image as a PNG file
  img_file.save("output.png")
  print("saved file")
  cv2.imshow("",img)
  cv2.waitKey(0)

def detect():
  # STEP 2: Create an FaceLandmarker object.
  base_options = python.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
  options = vision.FaceLandmarkerOptions(base_options=base_options,
                                        output_face_blendshapes=True,
                                        output_facial_transformation_matrixes=True,
                                        num_faces=1)
  detector = vision.FaceLandmarker.create_from_options(options)

  # STEP 3: Load the input image.
  image = mp.Image.create_from_file("C:/Users/Sharavn/Downloads/Hack/uploaded_frames/webcam_frame.jpg")

  # STEP 4: Detect face landmarks from the input image.
  detection_result = detector.detect(image)

  # STEP 5: Process the detection result. In this case, visualize it.
  annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
  image1 = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
  # cv2.imshow("",image1)


  # Height and width that will be used by the model
  

  BG_COLOR = (192, 192, 192) # gray
  MASK_COLOR = (255, 255, 255) # white
  BLUE_COLOR = (255, 0, 0) #blue


  # Create the options that will be used for ImageSegmenter
  base_options = python.BaseOptions(model_asset_path='hair_segmenter.tflite')
  options = vision.ImageSegmenterOptions(base_options=base_options,
                                        output_category_mask=True)

  # Create the image segmenter
  with vision.ImageSegmenter.create_from_options(options) as segmenter:

    # Loop through demo image(s)
    #for image_file_name in IMAGE_FILENAMES:

      # Create the MediaPipe image file that will be segmented
      image = mp.Image.create_from_file("C:/Users/Sharavn/Downloads/Hack/uploaded_frames/webcam_frame.jpg")

      # Retrieve the masks for the segmented image
      segmentation_result = segmenter.segment(image)
      category_mask = segmentation_result.category_mask

      # Generate solid color images for showing the output segmentation mask.
      image_data = image.numpy_view()
      fg_image = np.zeros(image_data.shape, dtype=np.uint8)
      fg_image[:] = BLUE_COLOR
      bg_image = np.zeros(image_data.shape, dtype=np.uint8)
      bg_image[:] = BG_COLOR

      condition = np.stack((category_mask.numpy_view(),) * 3, axis=-1) > 0.2
      output_image = np.where(condition, fg_image, bg_image)

      #print(f'Segmentation mask of {name}:')
      #resize_and_show(output_image)

      image_data = cv2.cvtColor(image.numpy_view(), cv2.COLOR_BGR2RGB)

      # Apply effects
      blurred_image = cv2.GaussianBlur(image_data, (55,55), 0)
      condition = np.stack((category_mask.numpy_view(),) * 3, axis=-1) > 0.1
      output_image = np.where(condition, fg_image, image1)

      #print(f'Blurred background of {image_file_name}:')
      resize_and_show(output_image)