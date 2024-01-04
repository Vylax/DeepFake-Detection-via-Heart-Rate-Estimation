import cv2
import numpy as np
import pyramids
import heartrate
import preprocessing
import eulerian
import em_hr

# Frequency range for Fast-Fourier Transform
freq_min = 1
freq_max = 1.8

def inject_heart_rate(video_path, output_path, target_heart_rate, amplitude_factor=0.025):
    # Preprocessing phase
    video_frames, frame_ct, fps = preprocessing.read_video(video_path)

    # Build Laplacian video pyramid
    lap_video = pyramids.build_video_pyramid(video_frames)

    # Inject heart rate into the video
    for i, video in enumerate(lap_video):
        if i == 0 or i == len(lap_video)-1:
            continue

        # Eulerian magnification with temporal FFT filtering
        result, fft, frequencies = eulerian.fft_filter(video, freq_min, freq_max, fps)
        video += result * amplitude_factor

    # Collapse the modified pyramid to obtain the final frames
    modified_frames = pyramids.collapse_laplacian_video_pyramid(lap_video, frame_ct)

    # Save the modified frames into a new video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (modified_frames[0].shape[1], modified_frames[0].shape[0]))

    for frame in modified_frames:
        out.write(frame)

    out.release()

# Example usage
target_heart_rate = 65
amplitude_factor = 0.01  # Adjust as needed to make it less noticeable
video_path = '../cohface/cohface/1/2/data.avi'
output_path = '../cohface/cohface/1/2/data_hacked_2.avi'

# Inject the heart rate into the video
inject_heart_rate(video_path, output_path, target_heart_rate, amplitude_factor)

# Calculate the heart rate from the injected video
injected_heart_rate = em_hr.get_heart_rate(output_path)
print(f"Injected Heart Rate: {injected_heart_rate} bpm")
