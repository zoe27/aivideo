# 语音翻译，从中文翻译成英文语音

import os
import json
import asyncio
import edge_tts
from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration

from ai_flow.Translation.FacebookM2 import translate_text
from ai_flow.Voice2Text.WhisperTTS import transcribe_audio_to_srt

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

async def main():

    # 0. 从音频文件生成字幕文件
    audio_file_path  = "/Users/apple/Documents/AI/aivideo/ai_flow/Text2Voice/final_output.mp3"
    os.system(f"afplay {audio_file_path}")
    srt_file_path = transcribe_audio_to_srt(audio_file_path, './output.srt')

    # 1. 提取字幕文本
    extract_text = extract_subtitles(srt_file_path)
    print("提取的字幕文本:", extract_text)

    # 2. 翻译字幕文本
    translate_result_text = translate_text('en', 'zh', extract_text)
    print("翻译结果:", translate_result_text)

    # 3. 翻译后的字幕文本转为语音
    await text_to_speech(translate_result_text, "translated_output.wav")

asyncio.run(main())