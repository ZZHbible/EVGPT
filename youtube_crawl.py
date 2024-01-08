#!/usr/bin/env python
# author = 'ZZH'
# time = 2023/12/29
# project = youtube_crawl
import json
import os
import subprocess
from tqdm import tqdm
from common import retry
import yt_dlp
import glob
from typing import  List

def get_youtube_title(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('title', None)

@retry(3)
def crawl_video(video_path: str,exist_mp4:List):
    title = get_youtube_title(video_path)
    if title not in exist_mp4:
        command = f'yt-dlp -f 22 --output "{output_dir}/{title}/%(title)s.%(ext)s" {video_path}'
        subprocess.run(command,shell=True,check=True)


if __name__ == '__main__':
    output_dir = "video_dataset"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    with open('config/total_video.json', 'r') as f:
        video_list = json.load(f)

    exist_mp4 = glob.glob(output_dir+'/*')

    for video_path in tqdm(video_list, desc="正在获取视频"):
        crawl_video(video_path,exist_mp4)
