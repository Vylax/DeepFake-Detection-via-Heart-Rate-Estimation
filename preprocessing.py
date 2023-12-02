import os
import cv2
import numpy as np
import time
import pickle
import gzip

faceCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt0.xml")


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
    if os.path.exists(video_path+'.pkl.gz'):
        cap.release()
        # Get the list of file names and sort them in order to maintain frames order
        '''file_names = sorted(os.listdir(frames_folder))

        video_frames_imported = [
            cv2.imread(os.path.join(frames_folder, f))
            for f in file_names
        ]

        for f in video_frames_imported:
            f = cv2.resize(f, (500, 500))
            frame = np.ndarray(shape=f.shape, dtype="float")
            frame[:] = f * (1. / 255)
            video_frames.append(frame)'''
        video_frames = import_frames(video_path)
        print("Frames loaded")
        frame_ct = len(video_frames)

        # TODO: remove when testing is done
        end_time = time.time()
        print(f"Elapsed time: {end_time-start_time} seconds")
        #TODO remove when done debugging
        print(f"Color Depth: {video_frames[0].dtype}")

        print(frame_ct, fps)
        return video_frames, frame_ct, fps

    face_rects = ()

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        roi_frame = img

        # Detect face
        #if len(video_frames) == 0:
        face_rects = faceCascade.detectMultiScale(gray, 1.3, 5)

        # Select ROI
        if len(face_rects) > 0:
            for (x, y, w, h) in face_rects:
                roi_frame = img[y:y + h, x:x + w]
            if roi_frame.size != img.size:
                roi_frame = cv2.resize(roi_frame, (500, 500))
                frame = np.ndarray(shape=roi_frame.shape, dtype="float")
                frame[:] = roi_frame * (1. / 255)
                video_frames.append(frame)

    # Save frames into the created folder
    export_frames(video_path, video_frames)
    '''for i, frame in enumerate(video_frames):
        #TODO remove when done debugging
        if i==0:
            print(f"Color Depth: {frame.dtype}")

        cv2.imwrite(os.path.join(frames_folder_temp, f"{videoname}_frame_{i}.png"), (frame * 255).astype(np.uint8), [cv2.IMWRITE_PNG_COMPRESSION, 0])'''


    frame_ct = len(video_frames)
    cap.release()

    '''# Rename the folder without the '_temp' suffix to indicate that the process was completed successfully
    folder_name = os.path.basename(frames_folder_temp)
    parent_path = os.path.dirname(frames_folder_temp)

    # Check if the folder name ends with "_temp"
    if folder_name.endswith("_temp"):
        # Create the new folder name without "_temp"
        new_folder_name = folder_name[:-5]

        # Create the new folder path
        new_folder_path = os.path.join(parent_path, new_folder_name)

        # Rename the folder
        for i in range(10):
            try:
                os.rename(frames_folder_temp, new_folder_path)
                print("Frames saved")
                break
            except Exception as e:
                print(f"Rename failed for the {i}-th attempt")
                time.sleep(1)
            if i==9:
                print("Couldn't rename the folder after 10 attempts'")
        
    else:
        print("Folder does not end with '_temp', this should never happen!")'''

    # TODO: remove when testing is done
    end_time = time.time()
    print(f"Elapsed time: {end_time-start_time} seconds")
    print(frame_ct, fps)
    return video_frames, frame_ct, fps
