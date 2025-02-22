import pysrt
import whisper
import ssl
from whisper.audio import SAMPLE_RATE

# 解决 SSL 问题
ssl._create_default_https_context = ssl._create_unverified_context

def time_to_hms(seconds):
    hrs = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = int(seconds % 60)
    ms = int((seconds % 1) * 1000)  # 毫秒
    return hrs, minutes, sec, ms

def transcribe_audio_to_srt(audio_file, srt_output_path, model_name="base", max_segment_duration=30):
    # 加载 Whisper 模型
    model = whisper.load_model(model_name)

    # 加载音频文件
    audio = whisper.load_audio(audio_file)
    # 获取音频的总时长（秒）
    audio_duration = len(audio) / SAMPLE_RATE
    print(f"Audio duration: {audio_duration} seconds")

    # 创建一个 SRT 文件对象
    srt_file = pysrt.SubRipFile()

    for start_time in range(0, int(audio_duration), max_segment_duration):
        # 计算当前段的结束时间
        end_time = min(start_time + max_segment_duration, audio_duration)

        # 切割音频段
        segment = audio[int(start_time * SAMPLE_RATE):int(end_time * SAMPLE_RATE)]

        segment_audio = whisper.pad_or_trim(segment)
        # 获取当前段的文本
        result = model.transcribe(segment_audio)
        print(result['segments'])

        # 打印当前段的文本
        print(f"Transcription for {start_time}-{end_time} seconds:")
        for idx, segment in enumerate(result['segments']):
            print(segment['text'])
            start_time_sec = segment['start'] + start_time
            end_time_sec = segment['end'] + start_time

            # 转换为时:分:秒,毫秒格式
            start_hrs, start_min, start_sec, start_ms = time_to_hms(start_time_sec)
            end_hrs, end_min, end_sec, end_ms = time_to_hms(end_time_sec)

            # 创建时间戳
            start_time_srt = pysrt.SubRipTime(hours=start_hrs, minutes=start_min, seconds=start_sec, milliseconds=start_ms)
            end_time_srt = pysrt.SubRipTime(hours=end_hrs, minutes=end_min, seconds=end_sec, milliseconds=end_ms)

            # 创建字幕条目
            subtitle = pysrt.SubRipItem(
                index=len(srt_file) + 1,  # 字幕编号
                start=start_time_srt,
                end=end_time_srt,
                text=segment['text']
            )

            # 添加字幕条目到 SRT 文件
            srt_file.append(subtitle)

    # 保存生成的 SRT 文件
    srt_file.save(srt_output_path)
    print(f"SRT file has been saved as {srt_output_path}")
    return srt_output_path

# 示例调用
audio_file = "../VideoFetch/file/284abbe510e4697da7a2c7b11607767e.mp3"
srt_output_path = "c56a6a5a785f6789688c067d99e1e504.srt"
transcribe_audio_to_srt(audio_file, srt_output_path)