#!/usr/bin/env python
# author = 'ZZH'
# time = 2023/12/29
# project = youtube_crawl
import json
import os
import subprocess
from tqdm import tqdm

from common import retry


@retry(3)
def crawl_video(video_path: str):
    command = f'yt-dlp -f 22 --output "{output_dir}/%(title)s.%(ext)s" {video_path}'
    subprocess.run(command, shell=True, check=True)


if __name__ == '__main__':
    output_dir = "video_dataset"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    with open('config/total_video.json', 'r') as f:
        video_list = json.load(f)

    for video_path in tqdm(video_list, desc="正在获取视频"):
        crawl_video(video_path)
