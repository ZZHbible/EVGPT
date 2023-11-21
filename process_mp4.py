import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import argparse


def extract_key_frames_optical_flow(video_path, threshold=2.0, save_dir='key_frames', frame_interval=5):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return

    ret, prev_frame = cap.read()
    if not ret:
        print("Error reading the first frame.")
        return

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    frame_count = 0
    key_frame_count = 0
    skip_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        skip_count += 1

        # Skip frames based on the frame_interval parameter
        if skip_count < frame_interval:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        mean_magnitude = np.mean(magnitude)

        if mean_magnitude > threshold:
            key_frame_path = os.path.join(save_dir, f"key_frame_{key_frame_count}.jpg")
            cv2.imwrite(key_frame_path, prev_frame)
            key_frame_count += 1

        prev_frame = frame
        prev_gray = gray
        skip_count = 0  # Reset skip count after processing a frame

    cap.release()
    print(f"Extracted {key_frame_count} key frames from {frame_count} total frames.")


def extract_key_frames(video_path, threshold=0.8, save_dir='key_frames', frame_interval=5):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return

    ret, prev_frame = cap.read()
    if not ret:
        print("Error reading the first frame.")
        return

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    frame_count = 0
    key_frame_count = 0
    skip_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        skip_count += 1

        # Skip frames based on the frame_interval parameter
        if skip_count < frame_interval:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_similarity = ssim(prev_gray, gray)

        if frame_similarity < threshold:
            key_frame_path = os.path.join(save_dir, f"key_frame_{key_frame_count}.jpg")
            cv2.imwrite(key_frame_path, prev_frame)
            key_frame_count += 1

        prev_frame = frame
        prev_gray = gray
        skip_count = 0  # Reset skip count after processing a frame

    # Save the last frame if it's the end of a similar sequence
    if key_frame_count == 0 or frame_similarity >= threshold:
        key_frame_path = os.path.join(save_dir, f"key_frame_{key_frame_count}.jpg")
        cv2.imwrite(key_frame_path, prev_frame)

    cap.release()
    print(f"Extracted {key_frame_count + 1} key frames from {frame_count} total frames.")

def extract_key_frames_combined(video_path, ssim_threshold=0.8, flow_threshold=2.0, save_dir='key_frames', frame_interval=5):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return

    ret, prev_frame = cap.read()
    if not ret:
        print("Error reading the first frame.")
        return

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    frame_count = 0
    key_frame_count = 0
    skip_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        skip_count += 1

        if skip_count < frame_interval:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # SSIM calculation
        ssim_score = ssim(prev_gray, gray)

        # Optical Flow calculation
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        mean_magnitude = np.mean(magnitude)

        # Combined metric
        is_ssim_significant = (1 - ssim_score) > ssim_threshold
        is_flow_significant = mean_magnitude > flow_threshold
        if is_ssim_significant or is_flow_significant:
            key_frame_path = os.path.join(save_dir, f"key_frame_{key_frame_count}.jpg")
            cv2.imwrite(key_frame_path, prev_frame)
            key_frame_count += 1

        prev_frame = frame
        prev_gray = gray
        skip_count = 0

    cap.release()
    print(f"Extracted {key_frame_count} key frames from {frame_count} total frames.")

args = argparse.ArgumentParser()
args.add_argument("--mp4file",default="zzh_work.mp4")
args.add_argument("--save_dir",default="key_frames")
args = args.parse_args()
video_path = args.mp4file  # Replace with your video file path
import time
begin = time.time()
extract_key_frames(video_path,frame_interval=10,save_dir=args.save_dir)
end = time.time()
print(end - begin)

