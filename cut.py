import io
import os.path
import tempfile

from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.silence import split_on_silence


def find_silent_parts(audio_segment, min_silence_len=1500, silence_thresh=-50):
    """
    使用pydub寻找静默部分
    :param audio_segment: AudioSegment对象
    :param min_silence_len: 认为是静默的最短长度（毫秒）
    :param silence_thresh: 认为是静默的音量阈值（分贝）
    :return: 静默时间段的列表，每个元素是一个(开始时间, 结束时间)的元组
    """
    silent_parts = split_on_silence(
        audio_segment,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )

    # 转换为开始和结束时间
    silent_times = []
    current_time = 0
    for part in silent_parts:
        start_time = current_time
        end_time = start_time + len(part)
        silent_times.append((start_time, end_time))
        current_time = end_time

    return silent_times


Video_Path = "video_dataset/PyTorch Tutorial - RNN & LSTM & GRU - Recurrent Neural Nets.mp4"
# 读取原始视频
video = VideoFileClip(Video_Path)
os.makedirs(Video_Path.split('.')[0],exist_ok=True)

# 提取音频并保存到临时文件
audio = video.audio
with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
    audio.write_audiofile(temp_audio_file.name, codec='pcm_s16le')
    temp_audio_path = temp_audio_file.name

# 将临时文件转换为AudioSegment对象
audio_segment = AudioSegment.from_file(temp_audio_path, format="wav")

# 寻找静默部分
silent_times = find_silent_parts(audio_segment)

# 使用静默部分时间来剪辑视频
for i, (start, end) in enumerate(silent_times):
    # 剪辑视频
    clip = video.subclip(start / 1000.0, end / 1000.0)

    # 保存剪辑后的视频
    clip.write_videofile(f"{Video_Path.split('.')[0]}/clip_{i + 1}.mp4")
