import cv2
import pyramids
import heartrate
import preprocessing
import eulerian

# Frequency range for Fast-Fourier Transform
freq_min = 1#0.6
freq_max = 1.8#4

def get_heart_rate(video_path):
    # Preprocessing phase
    video_frames, frame_ct, fps = preprocessing.read_video(video_path)
    #video_frames2, frame_ct2, fps2 = preprocessing.read_video(video_path)

    '''for i in range(len(video_frames)):
        print(f"video_frames[{i}]==video_frames2[{i}]:{(video_frames[i]==video_frames2[i]).all()}")
        if not (video_frames[i]==video_frames2[i]).all():
            print(video_frames[i])
            print(type(video_frames[i]))
            print(len(video_frames[i]))
            print("===========================")
            print(video_frames2[i])
            print(len(video_frames2[i]))'''

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