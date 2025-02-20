import pysrt
import whisper
import ssl

# 解决 SSL 问题
ssl._create_default_https_context = ssl._create_unverified_context

# 加载 Whisper 模型
model = whisper.load_model("base")

# 加载音频文件
audio = whisper.load_audio("../VideoFetch/file/2.mp3")
audio = whisper.pad_or_trim(audio)

# 获取音频的语言（Whisper 会自动检测语言）
result = model.transcribe(audio)

# 创建一个 SRT 文件对象
srt_file = pysrt.SubRipFile()

def time_to_hms(seconds):
    hrs = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = int(seconds % 60)
    ms = int((seconds % 1) * 1000)  # 毫秒
    return hrs, minutes, sec, ms


# 遍历 Whisper 结果中的字幕段落，并将它们添加到 SRT 文件
for idx, segment in enumerate(result['segments']):
    # 将秒数转换为时:分:秒,毫秒格式
    start_time_sec = segment['start']
    end_time_sec = segment['end']

    # 调用辅助函数，转换为时:分:秒,毫秒
    start_hrs, start_min, start_sec, start_ms = time_to_hms(start_time_sec)
    end_hrs, end_min, end_sec, end_ms = time_to_hms(end_time_sec)

    # 使用 pysrt.SubRipTime 来创建时间戳
    start_time = pysrt.SubRipTime(hours=start_hrs, minutes=start_min, seconds=start_sec, milliseconds=start_ms)
    end_time = pysrt.SubRipTime(hours=end_hrs, minutes=end_min, seconds=end_sec, milliseconds=end_ms)

    # 创建字幕条目
    subtitle = pysrt.SubRipItem(
        index=idx + 1,  # 字幕的编号（从 1 开始）
        start=start_time,
        end=end_time,
        text=segment['text']
    )

    # 将字幕条目添加到 SRT 文件
    srt_file.append(subtitle)

# 保存生成的 SRT 文件
srt_file.save("output.srt")
print("SRT file has been saved as output.srt")


# 辅助函数：将秒数转换为时:分:秒,毫秒格式
