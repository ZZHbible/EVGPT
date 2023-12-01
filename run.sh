# 使用 whisper 命令处理视频文件
whisper "$1" --language Chinese --model medium

# 使用 process_mp4.py 处理视频文件
python video2frame.py --mp4file "$1"

# 使用 main.py 处理视频文件
python main.py --mp4file "$1"