import os
import cv2
import numpy as np

faceCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")

# Read in and simultaneously preprocess video
def read_video(video_path):
    
    folder_path = os.path.dirname(video_path)
    videoname = os.path.splitext(os.path.basename(video_path))[0]

    frames_folder = os.path.join(folder_path, f"{videoname}_frames")
    frames_folder_temp = os.path.join(folder_path, f"{videoname}_frames_temp")

    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    video_frames = []

    face_rects = ()

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        roi_frame = img

        # Detect face
        face_rects = faceCascade.detectMultiScale(gray, 1.1, 4)

        # Select ROI
        if len(face_rects) > 0:
            for (x, y, w, h) in face_rects:
                roi_frame = img[y:y + h, x:x + w]
            if roi_frame.size != img.size:
                roi_frame = cv2.resize(roi_frame, (36, 36))
                frame = np.ndarray(shape=roi_frame.shape, dtype="float")
                frame[:] = roi_frame * (1. / 255)
                video_frames.append(frame)

    frame_ct = len(video_frames)
    cap.release()

    return video_frames, frame_ct, fps
