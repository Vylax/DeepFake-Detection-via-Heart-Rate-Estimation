import cv2
import numpy as np
import gc
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt

def generate_heart_rate_signal(length, target_bpm, fps):
    t = np.arange(0, length / fps, 1 / fps)
    heart_rate_signal = np.sin(2 * np.pi * target_bpm / 60 * t)
    return heart_rate_signal

def create_skin_mask(face_roi):
    # Example: Implement a simple skin mask using color thresholds (adjust as needed)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    hsv_face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
    skin_mask = cv2.inRange(hsv_face_roi, lower_skin, upper_skin)

    return skin_mask

def calculate_luminance(frame):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Calculate average luminance
    luminance = np.mean(gray_frame)
    
    return luminance

def inject_heart_rate(video_path, output_path, target_heart_rate, amplitude_factor=1.7222, texture_factor=0.2):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    modified_frames = []
    
    signal_values = []
    original_values = []
    result_values = []
    
    signal_frames = []
    original_frames = []
    result_frames = []
    
    t = np.arange(0, frame_count / fps, 1 / fps)
    sinusoidal_signal = 0.02 * np.sin(2 * np.pi * target_heart_rate / 60 * t)  # 0.02 works great but is a bit noticeable

    face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")

    temp = False

    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break

        if temp:
            luminance = calculate_luminance(frame) / 255.0
            print("luminance", luminance)
            sinusoidal_signal = sinusoidal_signal = (0.02 + 0.1 * (0.45 - luminance)) * np.sin(2 * np.pi * target_heart_rate / 60 * t)
            temp = False

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray_frame, 1.1, 4)

        if len(face_rects) > 0:
            x, y, w, h = face_rects[0]
            roi = frame[y:y + h, x:x + w]

            # Create a skin mask
            skin_mask = create_skin_mask(roi)

            # Inject the synthetic heart rate signal only in the skin region
            roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            signal = np.clip(sinusoidal_signal[i] * skin_mask, 0, 255)
            original = roi_hsv[:, :, 2]#np.clip(roi_hsv[:, :, 2] * skin_mask, 0, 255)

            roi_hsv[:, :, 2] = np.clip(roi_hsv[:, :, 2] + signal, 0, 255)
            modified_roi = cv2.cvtColor(roi_hsv, cv2.COLOR_HSV2BGR)
            
            result = np.clip(original+signal, 0, 255)

            # Replace the original face region with the modified one
            frame[y:y + h, x:x + w] = modified_roi

            # Append the average V channel value of the signal to signal_values
            signal_values.append(np.mean(signal))

            # Convert and scale images for visibility
            signal_scaled = (np.clip(8*signal / 255 * 255,0,255)).astype(np.uint8)
            original_scaled = (original / 255 * 255).astype(np.uint8)
            result_scaled = (result / 255 * 255).astype(np.uint8)

            # Append the scaled images to the respective lists
            signal_frames.append(cv2.cvtColor(signal_scaled, cv2.COLOR_GRAY2BGR))
            original_frames.append(cv2.cvtColor(original_scaled, cv2.COLOR_GRAY2BGR))
            result_frames.append(cv2.cvtColor(result_scaled, cv2.COLOR_GRAY2BGR))

            

            # Append the average V channel value of the original to original_values
            original_values.append(np.mean(original_scaled))

            # Append the average V channel value of the result to result_values
            result_values.append(np.mean(result_scaled))

        modified_frames.append(frame)

    # Display plots
    plt.plot(signal_values, label='Signal')
    plt.title('Heart Rate Signal')
    plt.legend()
    plt.savefig('oral/signal_plot.png')
    plt.close()

    plt.plot(original_values, label='Original')
    plt.title('Original Signal with Skin Mask')
    plt.legend()
    plt.savefig('oral/original_plot.png')
    plt.close()

    plt.plot(result_values, label='Result')
    plt.title('Result Signal')
    plt.legend()
    plt.savefig('oral/result_plot.png')
    plt.close()
    
    # Display plots
    plt.plot(original_values, label='Original')
    plt.plot(result_values, label='Result')

    plt.title('Heart Rate Signal')
    plt.legend()
    plt.show()

    # Save videos
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (modified_frames[0].shape[1], modified_frames[0].shape[0]))

    for frame in modified_frames:
        out.write(frame)

    out.release()

    # Save signals as videos
    save_as_video(signal_frames, 'oral/signal.mp4', fps)
    save_as_video(original_frames, 'oral/original_with_mask.mp4', fps)
    save_as_video(result_frames, 'oral/result.mp4', fps)

    cap.release()
    gc.collect()

def save_as_video(frames, output_path, fps):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps/6, (frames[0].shape[1], frames[0].shape[0]))

    for frame in frames:
        out.write(frame)

    out.release()


# Example usage
amplitude_factor = 4
video_path = 'oral/video.mp4'
output_path = 'oral/video_hacked.mp4'
target_heart_rate = 65  # Set your target heart rate here

inject_heart_rate(video_path, output_path, target_heart_rate, amplitude_factor)
