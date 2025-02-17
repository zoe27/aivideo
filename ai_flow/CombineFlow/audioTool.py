import os
import queue
import json
import asyncio
import edge_tts
import sounddevice as sd
from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration

import vosk

# 加载 Vosk 中文模型（下载后替换路径）
model_path = "../Voice2Text/vosk-model-cn"  # 下载的模型文件夹
if not os.path.exists(model_path):
    print("请先下载 Vosk 中文模型")
    exit()

model = vosk.Model(model_path)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def transcribe_audio():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("请说话...")
        rec = vosk.KaldiRecognizer(model, 16000)
        result_text = ""
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                result_text = result["text"].replace(" ", "")
                print("识别结果:", result_text)
                break  # 只识别一句话
    return result_text

async def text_to_speech(text, output_file):
    voice = "zh-CN-XiaoyiNeural"  # 选择微软的中文女声
    tts = edge_tts.Communicate(text, voice)
    await tts.save(output_file)
    os.system(f"afplay {output_file}")  # macOS 播放音频

# def translate_text(text):
#     model_name = "t5-large"
#     tokenizer = T5Tokenizer.from_pretrained(model_name)
#     model = T5ForConditionalGeneration.from_pretrained(model_name)
#     input_text = f"translate Chinese to English: {text}"
#     input_ids = tokenizer.encode(input_text, return_tensors="pt")
#     outputs = model.generate(input_ids)
#     translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return translated_text

def translate_text(text):
    model_path = "../Translation/m2m100-local"
    tokenizer = M2M100Tokenizer.from_pretrained(model_path)
    model = M2M100ForConditionalGeneration.from_pretrained(model_path)
    tokenizer.src_lang = "zh"
    inputs = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.get_lang_id("en"))
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translated_text

async def main():
    # 1. 读取用户输入的语音
    chinese_text = transcribe_audio()

    # 2. 将语言转为文字并播放
    await text_to_speech(chinese_text, "chinese_output.wav")

    # 3. 将文字翻译成英文
    english_text = translate_text(chinese_text)
    print("翻译结果:", english_text)

    # 4. 播放英文
    await text_to_speech(english_text, "english_output.wav")

asyncio.run(main())