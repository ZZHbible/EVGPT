#!/usr/bin/env python
# author = 'ZZH'
# time = 2023/12/29
# project = youtube_crawl
import json
import os
import re
from pytube import YouTube
import shutil
import subprocess
import glob
from loguru import logger
from tqdm import tqdm

from common import retry

output_dir = "video_dataset"
with open('config/total_video.json','r') as f:
    video_list = json.load(f)

you_get_path = shutil.which("you-get")
if you_get_path is None:
    raise FileNotFoundError("you-get not found.")

@retry(3)
def get_video_info(video_path:str):
    search_command = f"{you_get_path} -i {video_path}"
    result = subprocess.run(search_command, shell=True, check=True, stdout=subprocess.PIPE)
    stdout_output = result.stdout.decode('utf-8')
    return stdout_output



@retry(3)
def crawl_video(itag:str,video_path:str,file_name:str):

    command = f"{you_get_path} --itag {itag} --no-caption --output-filename {file_name} --output-dir {output_dir} {video_path}"
    subprocess.run(command, shell=True, check=True)

for video_path in tqdm(video_list,desc="正在获取视频") :
    stdout_output = get_video_info(video_path)

    # 定义正则表达式模式
    pattern = r'- itag:\s+\x1b\[7m(\d+)\x1b\[0m\n\s+container:\s+mp4\n\s+quality:\s+.* \(720p\)'
    # 使用正则表达式匹配
    match = re.search(pattern, stdout_output)
    # 检查匹配结果
    if match:
        # 提取itag值
        itag_720p_mp4 = match.group(1)
        logger.info(f"The itag for 720p mp4 is: {itag_720p_mp4}")
    else:
        logger.warning("Pattern not found in the text.")
        continue

    # 定义正则表达式模式，匹配以"title:"开始的行，然后获取冒号后面的内容
    title_pattern = re.compile(r'title:\s*(.*)')

    # 在文本中搜索匹配的模式
    match = title_pattern.search(stdout_output)

    # 如果找到匹配项，获取标题名称
    if match:
        title = '_'.join(match.group(1).split())
        logger.info("Title:", title)
    else:
        logger.warning("Title not found.")

    crawl_video(itag_720p_mp4,video_path,title)

# video_url = "https://www.youtube.com/watch?v=3Kb0QS6z7WA"
# video = YouTube(video_url)
# if not os.path.exists(output_dir):
#     os.mkdir(output_dir)
#
# file_name = '_'.join(video.title.split())
# print("Video_title = " + file_name)
# print("Video_author = " + video.author)
# print("Video_length = " + str(video.length))
#

#
# current_res = 0
# stream_highest_itag = -1
# for everystream in video.streams.filter(type="video"):
#     if int(everystream.resolution[:-1]) > 720:
#         continue
#     if int(everystream.resolution[:-1]) > current_res and 'mp4' in everystream.mime_type:
#         current_res = int(everystream.resolution[:-1])
#         stream_highest_itag = everystream.itag
#
# command = f"{you_get_path} --itag {stream_highest_itag} --output-filename {file_name} --output-dir {output_dir} {video_url}"
# subprocess.run(command, shell=True, check=True)
