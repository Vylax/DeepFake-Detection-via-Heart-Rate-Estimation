import cv2
import numpy as np
import gc
from scipy.fft import fft, ifft

def generate_heart_rate_signal(length, target_bpm, fps):
    t = np.arange(0, length / fps, 1 / fps)
    heart_rate_signal = np.sin(2 * np.pi * target_bpm / 60 * t)
    return heart_rate_signal

def create_skin_mask(face_roi):
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    hsv_face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
    skin_mask = cv2.inRange(hsv_face_roi, lower_skin, upper_skin)

    return skin_mask

def inject_heart_rate(video_path, output_path, target_heart_rate):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    modified_frames = []
    t = np.arange(0, frame_count / fps, 1 / fps)
    sinusoidal_signal = 0.02 * np.sin(2 * np.pi * target_heart_rate / 60 * t) #0.02 works great but is a bit noticable

    face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")

    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray_frame, 1.1, 4)

        if len(face_rects) > 0:
            x, y, w, h = face_rects[0]
            roi = frame[y:y + h, x:x + w]

            # Create a skin mask
            skin_mask = create_skin_mask(roi)

            # Inject the synthetic heart rate signal only in the skin region
            roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            roi_hsv[:, :, 2] = np.clip(roi_hsv[:, :, 2] + sinusoidal_signal[i] * skin_mask, 0, 255)
            modified_roi = cv2.cvtColor(roi_hsv, cv2.COLOR_HSV2BGR)

            # Replace the original face region with the modified one
            frame[y:y + h, x:x + w] = modified_roi

        modified_frames.append(frame)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (modified_frames[0].shape[1], modified_frames[0].shape[0]))

    for frame in modified_frames:
        out.write(frame)

    cap.release()
    out.release()
    gc.collect()

# Example usage but usualy this is called from another script
'''
video_path = 'path/to/your/video.mp4'
output_path = 'path/to/your/output_video_hacked.avi'

inject_heart_rate(video_path, output_path, target_heart_rate)
'''
