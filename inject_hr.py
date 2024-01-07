import cv2
import numpy as np
import gc

def inject_heart_rate(video_path, output_path, target_heart_rate, amplitude_factor=1.7222, texture_factor=0.2):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create an array to store the modified frames
    modified_frames = []

    # Time vector for the sinusoidal modulation
    t = np.arange(0, frame_count / fps, 1 / fps)

    # Sinusoidal modulation for heart rate simulation
    sinusoidal_signal = np.sin(2 * np.pi * target_heart_rate / 60 * t)

    # Load the face detection cascade
    faceCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt0.xml")

    face_rects = ()
    temp = True

    # Loop through each frame
    for i in range(frame_count):
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect face
        #TODO comment this when done tweaking
        if temp:
            face_rects = faceCascade.detectMultiScale(gray_frame, 1.3, 5)
            temp = False

        # Select ROI from the first detected face (you can modify this logic)
        if len(face_rects) > 0:
            x, y, w, h = face_rects[0]
            roi = frame[y:y + h, x:x + w]

            #Use this for Hue variation
            # Convert the ROI to HSV color space
            roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # Simulate heart rate by altering color in the ROI
            hue_variation0 = int(sinusoidal_signal[i] * 1.5)  # Adjust as needed
            hue_variation1 = int(sinusoidal_signal[i] * 0.5)  # Adjust as needed
            hue_variation2 = int(sinusoidal_signal[i] * 1.2)  # Adjust as needed
            roi_hsv[:, :, 0] = (roi_hsv[:, :, 0] + hue_variation0) % 180

            # Increase saturation and value to simulate blood perfusion
            roi_hsv[:, :, 1] = np.clip(roi_hsv[:, :, 1] + hue_variation1, 0, 255)
            roi_hsv[:, :, 2] = np.clip(roi_hsv[:, :, 2] + hue_variation2, 0, 255)

            # Clip the values to stay within the valid range
            #roi_hsv = np.clip(roi_hsv, 0, 255)

            # Convert the modified ROI back to BGR color space
            modified_roi = cv2.cvtColor(roi_hsv, cv2.COLOR_HSV2BGR)

            #Use this for Texture modulation
            # Modulate texture with increased amplitude
            texture_variation = np.clip(0.7 * sinusoidal_signal[i], -1, 1)

            # Apply the texture modulation to the image
            modified_roi = cv2.addWeighted(modified_roi, 1.0, texture_variation, 0.5, 0)

            # Replace the original ROI with the modified ROI in the frame
            frame[y:y + h, x:x + w] = modified_roi

        # Append the modified frame to the array
        modified_frames.append(frame)

    # Create a new video file with the modified frames
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (modified_frames[0].shape[1], modified_frames[0].shape[0]))

    for frame in modified_frames:
        out.write(frame)

    # Release video capture and writer
    cap.release()
    out.release()
    gc.collect()

# Example usage
target_heart_rate = 65
amplitude_factor = 4
video_path = '../cohface/cohface/1/1/data.avi'
output_path = '../cohface/cohface/1/1/data_hacked.avi'

#inject_heart_rate(video_path, output_path, target_heart_rate, amplitude_factor)
