import asyncio
import logging
import os

import edge_tts
import pysrt
from pydub import AudioSegment


global_variable = 0
# 异步语音合成函数
# voice需要注意，如果选的不对，可能识别不了。比如选的英语，可能就识别不了中文
async def synthesize_speech(text, output_path, voice='zh-CN-XiaoxiaoNeural'):
    """调用 edgeTTs 来生成语音并保存为文件"""
    # 创建 Communicate 对象
    # print(f"Synthesizing speech for: {text}",output_path)
    communicate = edge_tts.Communicate(text, voice)
    print(communicate)

    # 创建音频输出文件
    for attempt in range(3):  # 尝试三次
        try:
            with open(output_path, 'wb') as f:
                # 异步迭代获取音频数据流
                async for chunk in communicate.stream():
                    if chunk['type'] == 'audio':  # 检查 type 是否为 'audio'
                        # print(f"Writing audio chunk of size {len(chunk['data'])}")
                        f.write(chunk['data'])  # 写入音频数据
                    # else:
                    #     print("Not an audio chunk.")
            break  # 成功则跳出循环
        except Exception as e:
            print(f"Error during streaming (attempt {attempt + 1}/3): {e}")
            if attempt == 2:  # 最后一次尝试失败后抛出异常
                raise e


# 合成音频并按时间戳保存的异步处理函数
async def process_subtitles(subtitles):
    audio_segments = []
    # 遍历 SRT 文件中的每一行字幕
    for subtitle in subtitles:
        try:
            print(subtitle.index, subtitle.start, subtitle.end, subtitle.text)
            audio_path = f"audio_{subtitle.index}.mp3"
            print(f"Processing subtitle: {subtitle.index}, {subtitle.start} - {subtitle.end}")

            milliseconds = (subtitle.start.hours * 3600 + subtitle.start.minutes * 60 + subtitle.start.seconds) * 1000 + subtitle.start.milliseconds

            # 合成语音并保存为文件
            await synthesize_speech(subtitle.text, audio_path)

            # 使用 pydub 读取生成的音频文件
            audio = AudioSegment.from_mp3(audio_path)
            # 保存音频片段和其开始时间
            audio_segments.append((milliseconds, audio))  # 转换为毫秒
            # print(f"Processed subtitle {subtitle.index}: {subtitle.start} - {subtitle.end}", audio_path)
            # 更新进度条
            progress = (subtitle.index / len(subtitles)) * 100
            print(f"Progress: {progress:.2f}%")
            global global_variable
            global_variable = progress
        except Exception as e:
            logging.error(f"Error processing subtitle {subtitle.index}: {e}")

    print(audio_segments)
    # 按时间戳顺序拼接音频片段
    final_audio = AudioSegment.silent(duration=0)
    for start_time, segment in sorted(audio_segments, key=lambda x: x[0]):
        print(f"Appending audio segment at {start_time} ms", segment)
        final_audio += segment
        # Update progress
        progress = (start_time / audio_segments[-1][0]) * 100
        print(f"Progress: {progress:.2f}%")
        # Call other functions with the progress data
        # update_progress_bar(progress)
        global_variable = progress
        # await notify_other_function(progress)
    # 导出最终音频文件
    final_audio.export("final_output.mp3", format="mp3")
    os.system(f"afplay final_output.mp3")


def notify_other_function():
    # print("get Progress:", global_variable)
    return global_variable
