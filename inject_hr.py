import cv2
import numpy as np

def inject_heart_rate(video_path, output_path, target_heart_rate):
    print(amplitude_factor)
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
    
    # Loop through each frame
    for i in range(frame_count):
        ret, frame = cap.read()

        if not ret:
            break

        # Simulate heart rate by modulating pixel intensity
        modified_frame = np.clip(frame * (1 + amplitude_factor * sinusoidal_signal[i]), 0, 255).astype(np.uint8)

        # Append the modified frame to the array
        modified_frames.append(modified_frame)

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
# Reducing the amplitude to make it less noticeable
amplitude_factor = 0.15
video_path = '../cohface/cohface/1/0/data.avi'
output_path = '../cohface/cohface/1/0/hacked_data_'+str(target_heart_rate)+'bpm'+str(amplitude_factor)+'amp.avi'

#inject_heart_rate(video_path, output_path, target_heart_rate)

