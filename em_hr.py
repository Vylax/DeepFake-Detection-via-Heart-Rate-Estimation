import cv2
import pyramids
import heartrate
import preprocessing
import eulerian

# Frequency range for Fast-Fourier Transform
freq_min = 1
freq_max = 1.8

def get_heart_rate(video_path):
    # Preprocessing phase
    video_frames, frame_ct, fps = preprocessing.read_video(video_path)

    # Build Laplacian video pyramid
    lap_video = pyramids.build_video_pyramid(video_frames)
    amplified_video_pyramid = []

    for i, video in enumerate(lap_video):
        if i == 0 or i == len(lap_video)-1:
            continue

        # Eulerian magnification with temporal FFT filtering
        result, fft, frequencies = eulerian.fft_filter(video, freq_min, freq_max, fps)
        lap_video[i] += result

        # Calculate heart rate
        heart_rate = heartrate.find_heart_rate(fft, frequencies, freq_min, freq_max)
        
        return heart_rate