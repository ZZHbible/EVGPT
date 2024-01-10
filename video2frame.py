#!/usr/bin/env python
# author = 'ZZH'
# time = 2023/12/1
# project = video2frame
import glob
import os
import os.path
import cv2
import sys
from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter
import multiprocessing
from skimage.metrics import structural_similarity as ssim
from skimage import io
import numpy as np
from itertools import combinations


class CustomDiskWriter(KeyFrameDiskWriter):
    """

    :param KeyFrameDiskWriter: Writer class to overwrite
    :type KeyFrameDiskWriter: Writer
    """

    def generate_output_filename(self, filepath, keyframe_number):
        """Custom output filename method

        :param filepath: [description]
        :type filepath: [type]
        """
        filename = super().generate_output_filename(filepath, keyframe_number)

        suffix = "keyframe"

        return "_".join([filename, suffix])


def resize_images(images, target_size=(512, 512)):
    # 调整所有图像的大小为目标大小
    resized_images = [cv2.resize(img, target_size) for img in images]
    return resized_images


def calculate_ssim(img1, img2):
    return ssim(img1, img2, data_range=img1.max() - img1.min())


def post_process(images_dir: str, threshold=0.9):
    image_paths = sorted(glob.glob(f'{images_dir}/*.jpeg'), key=lambda x: int(x.split('_')[-1].split('.')[0]))
    images = [io.imread(path, as_gray=True) for path in image_paths]

    # 调整图像的大小，使它们具有相同的形状（512x512像素）
    images = resize_images(images, target_size=(512, 512))

    image_indices = list(range(len(images)))
    similar_images = set()

    for idx1, idx2 in combinations(image_indices, 2):
        similarity = calculate_ssim(images[idx1], images[idx2])

        if similarity > threshold:
            # 删除内容较少的图片
            image1_content = np.sum(images[idx1] > 0)
            image2_content = np.sum(images[idx2] > 0)

            if image1_content < image2_content:
                similar_images.add(idx1)
            else:
                similar_images.add(idx2)

    unique_images_indices = list(set(image_indices) - similar_images)
    unique_images = [images[idx] for idx in unique_images_indices]

    # 删除结构相似性大的图片
    for idx in similar_images:
        try:
            os.remove(image_paths[idx])
            print(f"{image_paths[idx]} removed successfully.")
        except OSError as e:
            print(f"Error deleting {image_paths[idx]}: {e}")

    return unique_images


def main_dir(image_dir, no_of_frames_to_returned=12):
    if len(sys.argv) == 1:
        dir_path = os.path.join(".", "tests", "data")
    else:
        dir_path = sys.argv[1]

    vd = Video()

    diskwriter = KeyFrameDiskWriter(location=image_dir)

    vd.extract_keyframes_from_videos_dir(
        no_of_frames=no_of_frames_to_returned, dir_path=dir_path,
        writer=diskwriter
    )


def main(image_dir, video_file_path, no_of_frames_to_returned=12):
    # Extract specific number of key frames from video
    # if os.name == 'nt':
    #     multiprocessing.freeze_support()

    vd = Video()

    diskwriter = KeyFrameDiskWriter(location=image_dir)

    # VIdeo file path
    # video_file_path = os.path.join(".", "tests", "data", "pos_video.mp4")
    print(f"Input video file path = {video_file_path}")

    vd.extract_video_keyframes(
        no_of_frames=no_of_frames_to_returned, file_path=video_file_path,
        writer=diskwriter
    )


if __name__ == "__main__":
    import argparse

    args = argparse.ArgumentParser()
    args.add_argument("--mp4file", default="lol_demo.mp4")
    args.add_argument("--save_dir", default="key_frames")
    args.add_argument('--num_frames_to_returned', default=12)
    args = args.parse_args()

    multiprocessing.set_start_method("spawn")
    main(args.save_dir, args.mp4file, no_of_frames_to_returned=args.num_frames_to_returned)
    post_process(args.save_dir, threshold=0.95)

    # main_dir(image_dir)
