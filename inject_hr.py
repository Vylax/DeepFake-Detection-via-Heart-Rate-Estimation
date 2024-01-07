import cv2
import numpy as np

def inject_heart_rate(video_path, output_path, target_heart_rate, amplitude_factor=1.7222):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    #print(amplitude_factor)

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

    # Loop through each frame
    for i in range(frame_count):
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect face
        face_rects = faceCascade.detectMultiScale(gray_frame, 1.3, 5)

        # Select ROI from the first detected face (you can modify this logic)
        if len(face_rects) > 0:
            x, y, w, h = face_rects[0]
            roi = frame[y:y + h, x:x + w]

            # Convert the ROI to HSV color space
            roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # Simulate heart rate by altering color in the ROI
            hue_variation = int(amplitude_factor * sinusoidal_signal[i])  # Adjust as needed
            roi_hsv[:, :, 0] = (roi_hsv[:, :, 0] + hue_variation) % 180

            # Convert the modified ROI back to BGR color space
            modified_roi = cv2.cvtColor(roi_hsv, cv2.COLOR_HSV2BGR)

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

# Example usage
target_heart_rate = 65
amplitude_factor = 4#1 not enough
video_path = '../cohface/cohface/1/1/data.avi'
output_path = '../cohface/cohface/1/1/data_hacked.avi'

#inject_heart_rate(video_path, output_path, target_heart_rate, amplitude_factor)
