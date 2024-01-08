import os
import cv2
import numpy as np
import time
import pickle
import gzip

faceCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")


def export_frames(video_path, video_frames):
    with gzip.open(video_path+'.pkl.gz', 'wb') as file:
        pickle.dump(video_frames, file)

def import_frames(video_path):
    with gzip.open(video_path+'.pkl.gz', 'rb') as file:
        video_frames = pickle.load(file)
    return video_frames

# Read in and simultaneously preprocess video
def read_video(video_path):

    # TODO: remove when testing is done
    start_time = time.time()
    
    folder_path = os.path.dirname(video_path)
    videoname = os.path.splitext(os.path.basename(video_path))[0]

    frames_folder = os.path.join(folder_path, f"{videoname}_frames")
    frames_folder_temp = os.path.join(folder_path, f"{videoname}_frames_temp")

    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    video_frames = []

    # If the processed frames file exists, load frames from it
    '''if os.path.exists(video_path+'.pkl.gz'):
        cap.release()
        video_frames = import_frames(video_path)
        print("Frames loaded")
        frame_ct = len(video_frames)

        # TODO: remove when testing is done
        end_time = time.time()
        print(f"Elapsed time: {end_time-start_time} seconds")
        #TODO remove when done debugging
        print(f"Color Depth: {video_frames[0].dtype}")

        print(frame_ct, fps)
        return video_frames, frame_ct, fps'''

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

    # Save frames into the created folder
    #export_frames(video_path, video_frames)

    frame_ct = len(video_frames)
    cap.release()


    # TODO: remove when testing is done
    end_time = time.time()
    #print(f"Elapsed time: {end_time-start_time} seconds")
    #print(frame_ct, fps)
    return video_frames, frame_ct, fps
