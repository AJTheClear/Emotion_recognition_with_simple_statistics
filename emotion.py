"""
Detects and displays emotions from camera feed using OpenCV and DeepFace
"""
from time import localtime, strftime, time
import cv2
import numpy as np
from deepface import DeepFace
from data_science import save_data, get_current_mood

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 600
IMAGE_REGION_WIDTH = int(WINDOW_WIDTH * 2 / 3)

def detect_emotions():
    """
    Detects and displays emotions form camera feed using OpenCV and DeepFace
    How it works:
    1. Starts a video capture
    2. Enters a while loop that can only be exited by pressing Escape key
    3. Reshaped each frame and calculates the white space where the statistics would stay
    4. After converting the resized frame to graysacle detects the faces
    5. For each face detects an emotion
       and displays it on the frame with both an outline of the face and label
    6. Saves the collected data each second
    7. Places statistics on teh white space on the right
    8. Combines the resized frame and the white space and displays it
    9. Releases te video and destroys the window
    """
    emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    font = cv2.FONT_HERSHEY_SIMPLEX

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    video = cv2.VideoCapture(0)

    last_save_time = time()

    while cv2.waitKey(1) != 27:
        _, frame = video.read()

        image_height, image_width = frame.shape[:2]
        image_width_scaled = max(image_width, IMAGE_REGION_WIDTH)
        image_height_scaled = int(image_height * (image_width_scaled / image_width))
        image_resized = cv2.resize(frame, (image_width_scaled, image_height_scaled))

        blank_region_width = WINDOW_WIDTH - IMAGE_REGION_WIDTH
        blank_image = np.ones((image_height_scaled, blank_region_width, 3), dtype=np.uint8) * 255

        gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        emotion_counts = {emotion: 0 for emotion in emotion_labels}

        for (x, y, w, h) in faces:

            face_img = frame[y:y+h, x:x+w]

            try:
                analyze = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)

                emotion = analyze[0]['dominant_emotion']
                emotion_counts[emotion] += 1

                cv2.putText(image_resized, emotion, (x, y-10), font, 0.9, (36,255,12), 2)
            except Exception as e:
                print('error:', e)

            cv2.rectangle(image_resized, (x, y), (x+w, y+h), (0, 0, 225), 1)

        num_faces = len(faces)

        current_time = time()
        if current_time - last_save_time >= 1:
            date = strftime("%d %b %Y %H:%M:%S", localtime())
            save_data(date, num_faces, emotion_counts)
            last_save_time = current_time

        mood = get_current_mood()
        cv2.putText(blank_image, f'current mood is: {mood}', (20, 200), font, 0.8, (0, 0, 0), 2)
        cv2.putText(blank_image, f'number of faces: {num_faces}', (20, 100), font, 0.8, (0, 0, 0),2)
        cv2.putText(blank_image, 'To exit press Esc button', (20, 525), font, 0.8, (0, 0, 0), 2)
        cv2.putText(blank_image, 'Emotion Recognition App', (20, 20), font, 0.8, (0, 0, 0), 2)

        i = 0
        for key, value in emotion_counts.items():
            cv2.putText(blank_image, f'{key} = {value}', (20, 300 + i), font, 0.8, (0, 0, 0), 2)
            i += 20

        cv2.namedWindow('Window', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Window', WINDOW_WIDTH, WINDOW_HEIGHT)

        combined_image = np.hstack((image_resized, blank_image))

        cv2.imshow('Window', combined_image)

    video.release()
    cv2.destroyAllWindows()
