import asyncio
import logging
import os

import edge_tts
import pysrt
from pydub import AudioSegment

# 解析 SRT 文件
subtitles = pysrt.open('/Users/apple/Documents/AI/aivideo/Test/WhisperTTS/test_output.srt')  # 请替换为您的 SRT 文件路径


# 异步语音合成函数
# voice需要注意，如果选的不对，可能识别不了。比如选的英语，可能就识别不了中文
async def synthesize_speech(text, output_path, voice='zh-CN-XiaoxiaoNeural'):
    """调用 edgeTTs 来生成语音并保存为文件"""
    # 创建 Communicate 对象
    # print(f"Synthesizing speech for: {text}",output_path)
    communicate = edge_tts.Communicate(text, voice)
    print(communicate)

    # 创建音频输出文件
    with open(output_path, 'wb') as f:
        try:
            # 异步迭代获取音频数据流
            async for chunk in communicate.stream():
                if chunk['type'] == 'audio':  # 检查 type 是否为 'audio'
                    # print(f"Writing audio chunk of size {len(chunk['data'])}")
                    f.write(chunk['data'])  # 写入音频数据
                # else:
                #     print("Not an audio chunk.")
        except Exception as e:
            print(f"Error during streaming: {e}")


# 合成音频并按时间戳保存的异步处理函数
async def process_subtitles(subtitles):
    audio_segments = []
    # 遍历 SRT 文件中的每一行字幕
    for subtitle in subtitles:
        print(subtitle.index, subtitle.start, subtitle.end, subtitle.text)
        audio_path = f"audio_{subtitle.index}.mp3"
        print(f"Processing subtitle: {subtitle.index}, {subtitle.start} - {subtitle.end}")

        # 合成语音并保存为文件
        await synthesize_speech(subtitle.text, audio_path)

        # 使用 pydub 读取生成的音频文件
        audio = AudioSegment.from_mp3(audio_path)

        # 保存音频片段和其开始时间
        audio_segments.append((subtitle.start.seconds * 1000, audio))  # 转换为毫秒

    # 按时间戳顺序拼接音频片段
    final_audio = AudioSegment.silent(duration=0)
    for start_time, segment in sorted(audio_segments, key=lambda x: x[0]):
        final_audio += segment

    # 导出最终音频文件
    final_audio.export("final_output.mp3", format="mp3")
    os.system(f"afplay final_output.mp3")


# 主函数：启动异步任务
if __name__ == "__main__":
    asyncio.run(process_subtitles(subtitles))  # 使用 asyncio.run 来运行异步函数