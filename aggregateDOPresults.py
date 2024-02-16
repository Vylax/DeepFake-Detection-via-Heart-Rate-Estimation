import os
from collections import defaultdict
import statistics
import pandas as pd
from datetime import datetime

# Set the minimum score threshold
min_score = 0.579

# Define lists to store results
medians = []
averages = []
frames_above = []
frames_count = []
successive_frames_above = []
ratio_frames_above = []
ratio_successive_frames_above = []
video_names = []

# Dictionary to store scores for each video
video_scores = defaultdict(list)

# Read the input file
with open('deepfake_scores.txt2549651', 'r') as file:
    for line in file:
        if "img;score" in line:
            continue
        line = line.strip().split(';')
        video_path = line[0].split('/RawFrames/')[1].split('/')[0]
        score = float(line[1].strip('[]'))

        video_scores[video_path].append(score)

# Process scores for each video
for video, scores in video_scores.items():
    # Extract video name without extension or parent path
    video_name = os.path.splitext(os.path.basename(video))[0]

    # Calculate median and average
    median = statistics.median(scores)
    average = sum(scores) / len(scores)

    # Count frames above the threshold
    above_threshold = sum(1 for s in scores if s > min_score)

    # Count total frames
    total_frames = len(scores)

    # Count successive frames above threshold
    successive_above = 0
    current_successive = 0
    for s in scores:
        if s > min_score:
            current_successive += 1
        else:
            successive_above += current_successive
            current_successive = 0

    # Calculate the ratio of frames_above by frames_count
    ratio = above_threshold / total_frames
    ratio_successive = successive_above / total_frames

    # Append results to lists
    medians.append(median)
    averages.append(average)
    frames_above.append(above_threshold)
    frames_count.append(total_frames)
    successive_frames_above.append(successive_above)
    ratio_frames_above.append(ratio)
    ratio_successive_frames_above.append(ratio_successive)
    video_names.append(video_name)

# Create a DataFrame
data = {
    'Names': video_names,
    'Average': averages,
    'Medians': medians,
    'Frames Above Threshold': frames_above,
    'Frames Count': frames_count,
    'Successive Frames Above Threshold': successive_frames_above,
    'Ratio Frames Above Threshold': ratio_frames_above,
    'Ratio Successive Frames Above Threshold': ratio_successive_frames_above
}

df = pd.DataFrame(data)

# Generate Excel filename with current date and time
current_time = datetime.now().strftime("%Y-%m-%d-%Hh%Mm%Ss")
excel_filename = f"results_{current_time}.xlsx"

# Write DataFrame to Excel
df.to_excel(excel_filename, index=False)
print(f"Results written to {excel_filename}")
