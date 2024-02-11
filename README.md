This project demonstrates the implementation of real-time facial emotion recognition using the deepface library and OpenCV. The
objective is to capture live video from a webcam, identify faces within the video stream, and predict the corresponding emotions for
each detected face. The emotions predicted are displayed in real-time on the video frames.

To set up:
1. Clone the github repository
2. Install required dependencies
    Use pip install -r requirements.txt or 
    the following two commands
    pip install deepface
    pip install opencv-python
3. Run the code


Approach:
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