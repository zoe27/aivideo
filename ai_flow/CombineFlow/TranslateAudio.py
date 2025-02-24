# 语音翻译，从中文翻译成英文语音

import os
import json
import asyncio
import edge_tts
import pysrt
from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration

from ai_flow.Text2Voice.EdgeTTS_srt import process_subtitles
from ai_flow.Translation.FacebookM2 import translate_text, translate_srt_file
from ai_flow.Voice2Text.WhisperSTT import transcribe_audio_to_srt

"""
  Extracts subtitles from a given SRT file.

  Args:
      file_path (str): The path to the SRT file.

  Returns:
      str: The extracted subtitles as a single string.
"""


def extract_subtitles(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        subtitles = []
        for line in file:
            if '-->' not in line and line.strip() and not line.strip().isdigit():
                subtitles.append(line.strip())
    return ' '.join(subtitles)


async def text_to_speech(text, output_file, voice="zh-CN-XiaoyiNeural"):  # 默认选择微软的中文女声
    tts = edge_tts.Communicate(text, voice)
    await tts.save(output_file)
    os.system(f"afplay {output_file}")  # macOS 播放音频


async def generate_translated_srt(audio_file_path, srt_output_path, translated_srt_output_path):
    # 0. 从音频文件生成字幕文件
    os.system(f"afplay {audio_file_path}")
    srt_file_path = transcribe_audio_to_srt(audio_file_path, srt_output_path)

    # 1. 翻译字��文件
    translate_srt_file(srt_file_path, translated_srt_output_path, 'en', 'zh')
    print(f"字幕文件已翻译并��存至: {translated_srt_output_path}")

    await process_subtitles(pysrt.open(translated_srt_output_path))


async def generate_translated_audio(audio_file_path, srt_output_path, translated_audio_output_path,
                                    voice="zh-CN-XiaoxiaoNeural"):
    # 0. 从音频文件生成字幕文件
    os.system(f"afplay {audio_file_path}")
    srt_file_path = transcribe_audio_to_srt(audio_file_path, srt_output_path)

    # 1. 提取字幕文本
    extract_text = extract_subtitles(srt_file_path)
    print("提取的字幕文本:", extract_text)

    # 2. 翻译字幕文本
    translate_result_text = translate_text('en', 'zh', extract_text)
    print("翻译结果:", translate_result_text)

    # 3. 翻译后的字幕文本转为语音
    await text_to_speech(translate_result_text, translated_audio_output_path, voice)

if __name__ == "__main__":
    audio_file_path = "path/to/audio/file"
    srt_output_path = "path/to/output/srt"
    translated_srt_output_path = "path/to/translated/output/srt"
    translated_audio_output_path = "path/to/translated/output/audio"

    asyncio.run(generate_translated_srt(audio_file_path, srt_output_path, translated_srt_output_path))
    asyncio.run(generate_translated_audio(audio_file_path, srt_output_path, translated_audio_output_path))