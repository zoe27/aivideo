# 语音翻译，从中文翻译成英文语音

import os
import json
import asyncio
import edge_tts
from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration

def extract_subtitles(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        subtitles = []
        for line in file:
            if '-->' not in line and line.strip() and not line.strip().isdigit():
                subtitles.append(line.strip())
    return ' '.join(subtitles)

def translate_text(text):
    model_path = "../Translation/m2m100-local"
    tokenizer = M2M100Tokenizer.from_pretrained(model_path)
    model = M2M100ForConditionalGeneration.from_pretrained(model_path)
    tokenizer.src_lang = "en"
    inputs = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.get_lang_id("zh"))
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translated_text

async def text_to_speech(text, output_file, voice="zh-CN-XiaoyiNeural"):  # 默认选择微软的中文女声
    tts = edge_tts.Communicate(text, voice)
    await tts.save(output_file)
    os.system(f"afplay {output_file}")  # macOS 播放音频

async def main():
    # 1. 提取字幕文本
    chinese_text = extract_subtitles("../Voice2Text/c56a6a5a785f6789688c067d99e1e504.srt")
    print("提取的字幕文本:", chinese_text)

    # 2. 翻译字幕文本
    english_text = translate_text(chinese_text)
    print("翻译结果:", english_text)

    # 3. 翻译后的字幕文本转为语音
    await text_to_speech(english_text, "translated_output.wav")

asyncio.run(main())