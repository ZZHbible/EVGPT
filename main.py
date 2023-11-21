#!/usr/bin/env python
# author = 'ZZH'
# time = 2023/11/14
# project = main
import base64
# Function to encode the image
import glob
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


image_dir = "key_frames/*.jpg"
image_list = []
for image_path in glob.glob(image_dir):
    image_list.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(image_path)}"}})


# image_path = "key_frames/key_frame_0.jpg"
# base64_image = encode_image(image_path)

def main(args):
    txt_file = args.mp4file.split('.')[0]+'.txt'
    s=""
    with open(txt_file) as f:
        for row in f.readlines():
            s+=(row.strip()+',')
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        # model="gpt-4-0314",
        messages=[
            {
                "role": "system",
                "content": [
                    "你是一个专业的计算机程序员助教，请帮助学生解答问题"
                ],
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"你将观看一段视频，其中文字部分如下：\n{s}\n问题为：{args.query}"
                    },
                    *image_list
                ]
            }
        ],
        temperature=0.7,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        # api_base=os.getenv("OPENAI_API_BASE")
    )['choices'][0]['message']['content']
    print(response)

if __name__ == '__main__':
    import argparse
    args = argparse.ArgumentParser()
    args.add_argument("--mp4file",default="zzh_work.mp4")
    args.add_argument("--image_path",default="key_frames")
    args.add_argument("--query",default="能使用异步gather改写代码嘛")
    args=args.parse_args()
    main(args)


